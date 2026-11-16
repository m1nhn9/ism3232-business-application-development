"""Campus Print Desk assistant with checked tools."""

try:
    from .chatbot import SupportChatbot
except ImportError:
    from chatbot import SupportChatbot


# Use the shared conversation loop with print-desk handoff rules.
class PrintShopAssistant(SupportChatbot):
    # Describe this class or method for callers.
    """Reuse the bounded tool loop with print-shop handoff rules."""

    # Catch sensitive requests before asking the model.
    def needs_human(self, text):
        # Return the checked result or the message the caller should display.
        return any(
            word in text
            for word in ["refund", "cancel", "payment", "card", "complaint"]
        )
