"""Campus Print Desk assistant with checked tools."""

try:
    from .chatbot import SupportChatbot
except ImportError:
    from chatbot import SupportChatbot


# Group this component’s state and behavior behind one interface.
class PrintShopAssistant(SupportChatbot):
    # Document the interface for readers and tool-description generation.
    """Reuse the bounded tool loop with print-shop handoff rules."""

    # Define needs_human so callers can needs human.
    def needs_human(self, text):
        # Return the result to the caller without performing terminal I/O.
        return any(
            word in text
            for word in ["refund", "cancel", "payment", "card", "complaint"]
        )
