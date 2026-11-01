from module06_agents.my_assistant import PrintShopAssistant
from module06_agents.my_tool import FAQBook


def make_assistant():
    tool = FAQBook(
        {
            "hours": "Open Monday-Friday, 8:00 am-6:00 pm.",
            "pricing": "Black-and-white pages cost $0.10 each.",
            "pickup": "Bring your order number to the print desk.",
        }
    )
    return PrintShopAssistant("Piper", "Be clear and helpful.", tool)


def test_faq_question_uses_the_supplied_tool():
    assistant = make_assistant()
    assert assistant.respond("What are your HOURS?") == (
        "Open Monday-Friday, 8:00 am-6:00 pm."
    )
    assert assistant.respond("Tell me about pickup") == (
        "Bring your order number to the print desk."
    )


def test_failed_topic_lookup_asks_for_clarification():
    assistant = make_assistant()
    assert assistant.respond("FAQ: delivery?") == (
        "Which topic? I can check hours, pricing, or pickup."
    )
    assert assistant.faq_tool.answer_for("delivery") is None


def test_refund_request_goes_to_staff_before_faq_lookup():
    assistant = make_assistant()
    assert "staff" in assistant.respond("I want a refund for that pricing")
    assert "staff" in assistant.respond("Please cancel my order")
    assert "staff" in assistant.respond("Change my payment card")


def test_unsupported_request_gets_a_safe_reply():
    assistant = make_assistant()
    assert "not sure" in assistant.respond("What is the weather tomorrow?")


def test_history_records_exact_roles_and_content():
    assistant = make_assistant()
    greeting = assistant.respond("hello")
    reply = assistant.respond("What is the pricing?")
    assert assistant.history == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": greeting},
        {"role": "user", "content": "What is the pricing?"},
        {"role": "assistant", "content": reply},
    ]


def test_missing_answer_is_not_invented():
    tool = FAQBook({"hours": None})
    assistant = PrintShopAssistant("Piper", "Be clear.", tool)
    assert assistant.respond("What are your hours?") == (
        "I don't have that answer. Please ask the print desk staff."
    )


def test_two_assistants_keep_independent_histories():
    first = make_assistant()
    second = make_assistant()
    first.respond("hello")
    assert len(first.history) == 2
    assert second.history == []
