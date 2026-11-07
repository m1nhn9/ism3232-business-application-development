from module06_agents.mock_model import MockModel
from module06_agents.my_assistant import PrintShopAssistant
from module06_agents.my_tool import FAQBook


# Define an unavailable model so the assistant's safe fallback is tested directly.
class SilentModel:
    # Explain that None represents an expected model outage.
    """A model that never has an answer, like Ollama when it is switched off."""

    # Keep the common model signature even though this stand-in ignores its inputs.
    def reply(self, instructions, history):
        # Return the same failure signal produced by OllamaModel on expected errors.
        return None


def make_assistant():
    tool = FAQBook(
        {
            "hours": "Open Monday-Friday, 8:00 am-6:00 pm.",
            "pricing": "Black-and-white pages cost $0.10 each.",
            "pickup": "Bring your order number to the print desk.",
        }
    )
    return PrintShopAssistant("Piper", "Be clear and helpful.", tool, MockModel())


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


def test_other_messages_go_to_the_model():
    assistant = make_assistant()
    assert assistant.respond("hello") == "Hello! How can I help you today?"


def test_model_failure_gets_the_assistants_safe_reply():
    tool = FAQBook({"hours": "Open weekdays."})
    assistant = PrintShopAssistant("Piper", "Be clear.", tool, SilentModel())
    assert "try again" in assistant.respond("What is your favorite color?")


def test_tool_rule_does_not_need_the_model():
    tool = FAQBook({"hours": "Open weekdays."})
    assistant = PrintShopAssistant("Piper", "Be clear.", tool, SilentModel())
    assert assistant.respond("What are your hours?") == "Open weekdays."


def test_handoff_rule_does_not_need_the_model():
    tool = FAQBook({"hours": "Open weekdays."})
    assistant = PrintShopAssistant("Piper", "Be clear.", tool, SilentModel())
    assert "staff" in assistant.respond("Please cancel my order")


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
    assistant = PrintShopAssistant("Piper", "Be clear.", tool, MockModel())
    assert assistant.respond("What are your hours?") == (
        "I don't have that answer. Please ask the print desk staff."
    )


def test_two_assistants_keep_independent_histories():
    first = make_assistant()
    second = make_assistant()
    first.respond("hello")
    assert len(first.history) == 2
    assert second.history == []
