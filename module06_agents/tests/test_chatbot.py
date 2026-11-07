from module06_agents.chatbot import SupportChatbot
from module06_agents.echo_model import EchoModel
from module06_agents.mock_model import MockModel
from module06_agents.order_tool import OrderLookup
from module06_agents.stock_tool import StockLookup


# Define an unavailable stand-in so the chatbot's own fallback can be tested.
class SilentModel:
    # Explain that this object deliberately provides no answer.
    """A model that never has an answer, like Ollama when it is switched off."""

    # Match the reply interface used by every model component in the lab.
    def reply(self, instructions, history):
        # Signal unavailability exactly as the real adapter does on expected errors.
        return None


def make_bot():
    """Give each test a fresh chatbot, tools, and conversation history."""
    order_tool = OrderLookup({"A100": "shipped", "A101": "processing"})
    stock_tool = StockLookup({"rain jacket": 12, "day pack": 0})
    return SupportChatbot("Sunny", "Be friendly.", order_tool, stock_tool, MockModel())


def make_bot_with_silent_model():
    """Build a chatbot whose model never answers."""
    order_tool = OrderLookup({"A100": "shipped", "A101": "processing"})
    stock_tool = StockLookup({"rain jacket": 12, "day pack": 0})
    return SupportChatbot(
        "Sunny", "Be friendly.", order_tool, stock_tool, SilentModel()
    )


def test_tool_finds_known_status():
    tool = OrderLookup({"A100": "shipped"})
    assert tool.find_status("A100") == "shipped"


def test_tool_returns_none_for_unknown_order():
    tool = OrderLookup({"A100": "shipped"})
    assert tool.find_status("A999") is None


def test_respond_records_both_messages():
    bot = make_bot()
    reply = bot.respond("hello")
    assert bot.history == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": reply},
    ]


def test_order_question_uses_the_tool():
    bot = make_bot()
    assert bot.respond("Where is order A100?") == "Order A100 is shipped."


def test_order_question_without_an_id_asks_for_one():
    bot = make_bot()
    assert "order ID" in bot.respond("Where is my order?")


def test_address_change_goes_to_a_human():
    bot = make_bot()
    assert "human" in bot.respond("Please change my shipping address")


def test_unknown_request_gets_a_safe_reply():
    bot = make_bot()
    assert "not sure" in bot.respond("What is the weather today?")


def test_other_messages_go_to_the_model():
    bot = make_bot()
    assert bot.respond("hello") == "Hello! How can I help you today?"


def test_safe_reply_when_the_model_has_no_answer():
    bot = make_bot_with_silent_model()
    assert "try again" in bot.respond("hello")


def test_order_rule_does_not_need_the_model():
    bot = make_bot_with_silent_model()
    assert bot.respond("Where is order A100?") == "Order A100 is shipped."


def test_handoff_rule_does_not_need_the_model():
    bot = make_bot_with_silent_model()
    assert "human" in bot.respond("Please change my shipping address")


def test_two_chatbots_keep_separate_histories():
    first = make_bot()
    second = make_bot()
    first.respond("hello")
    assert len(first.history) == 2
    assert len(second.history) == 0


def test_count_user_messages():
    bot = make_bot()
    assert bot.count_user_messages() == 0
    bot.respond("hello")
    bot.respond("Where is order A100?")
    assert bot.count_user_messages() == 2
    assert len(bot.history) == 4


def test_stock_question_uses_the_stock_tool():
    bot = make_bot()
    assert bot.respond("Is the rain jacket in stock?") == (
        "We have 12 of the rain jacket in stock."
    )


def test_order_id_matching_ignores_message_case():
    tool = OrderLookup({"A100": "shipped"})
    assert tool.find_order_id("where is a100?") == "A100"
    assert tool.find_order_id("Where is A999?") is None


def test_unknown_product_requests_clarification():
    bot = make_bot()
    assert "Which product?" in bot.respond("Do you have it in stock?")


def test_stock_tool_distinguishes_zero_from_unknown():
    tool = StockLookup({"day pack": 0})
    assert tool.find_product("Is the DAY PACK in stock?") == "day pack"
    assert tool.count_for("day pack") == 0
    assert tool.count_for("unknown") is None
    assert tool.find_product("unknown") is None
    assert "0 of the day pack" in make_bot().respond("Is the day pack in stock?")


def test_handoff_takes_priority_over_order_lookup():
    bot = make_bot()
    assert "human" in bot.respond("Change the payment card for order A100")


def test_shared_tools_do_not_share_chatbot_history():
    order_tool = OrderLookup({"A100": "shipped"})
    stock_tool = StockLookup({"rain jacket": 12})
    model = MockModel()
    sunny = SupportChatbot("Sunny", "Be cheerful.", order_tool, stock_tool, model)
    river = SupportChatbot("River", "Be formal.", order_tool, stock_tool, model)
    sunny.respond("hello")
    sunny.respond("Where is order A100?")
    river.respond("hello")
    assert sunny.order_tool is river.order_tool
    assert sunny.stock_tool is river.stock_tool
    assert sunny.history is not river.history
    assert len(sunny.history) == 4
    assert len(river.history) == 2
    assert river.history[1]["content"] == "Hello! How can I help you today?"


def test_chatbot_works_with_any_model_that_has_a_reply_method():
    order_tool = OrderLookup({"A100": "shipped"})
    stock_tool = StockLookup({"rain jacket": 12})
    bot = SupportChatbot("Sunny", "Be friendly.", order_tool, stock_tool, EchoModel())
    assert bot.respond("good morning") == "You said: good morning"
