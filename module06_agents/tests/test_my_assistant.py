from module06_agents.fake_model import FakeModel
from module06_agents.my_assistant import PrintShopAssistant
from module06_agents.my_tool import FAQBook
from module06_agents.print_queue import PrintQueue
from module06_agents.print_toolbox import PrintToolbox


def make_bot(decisions):
    tools = PrintToolbox(FAQBook({"hours": "Open weekdays."}), PrintQueue())
    return PrintShopAssistant("Piper", "Be helpful.", tools, FakeModel(decisions))


def request(document="essay.pdf", customer="Dana Cruz"):
    return {
        "tool": "request_print_job",
        "arguments": {"document": document, "customer": customer},
    }


def test_job_waits_for_staff_and_approval_applies_once():
    bot = make_bot([request(), {"text": "Sent."}])
    bot.respond("Print essay.pdf for Dana Cruz")
    queue = bot.tools.queue
    assert len(queue.waiting()) == 1
    assert queue.jobs == []
    queue.approve(1)
    queue.approve(1)
    assert len(queue.jobs) == 1


def test_fabricated_name_is_refused():
    bot = make_bot([request(), {"text": "Your name?"}])
    bot.respond("Print essay.pdf")
    assert "has not given that customer" in bot.history[1]["content"]
    assert bot.tools.queue.waiting() == []


def test_rejection_never_accepts_job():
    bot = make_bot([request(), {"text": "Sent."}])
    bot.respond("Print essay.pdf for Dana Cruz")
    bot.tools.queue.reject(1)
    bot.tools.queue.approve(1)
    assert bot.tools.queue.jobs == []


def test_handoff_precedes_model():
    bot = make_bot([])
    assert "human" in bot.respond("Cancel my print job")
    assert bot.model.calls == 0


def test_faq_is_selected_by_model():
    bot = make_bot(
        [
            {"tool": "check_faq", "arguments": {"topic": "hours"}},
            {"text": "Open weekdays."},
        ]
    )
    assert bot.respond("What are your hours?") == "Open weekdays."
    assert bot.history[1]["role"] == "tool"


def test_missing_unknown_and_fabricated_tools_are_refused():
    bot = make_bot([])
    assert "no tool" in bot.tools.run("approve", {}, [])
    assert "missing" in bot.tools.run("request_print_job", {}, [])
    assert "has not given" in bot.tools.run("check_faq", {"topic": "hours"}, [])
