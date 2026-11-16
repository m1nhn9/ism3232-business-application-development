"""Campus Print Desk assistant with checked tools."""

try:
    from .chatbot import SupportChatbot
except ImportError:
    from chatbot import SupportChatbot


# Group this component’s state and behavior behind one interface.
class PrintShopAssistant(SupportChatbot):
    # Document the interface for readers and tool-description generation.
    """Reuse the bounded tool loop with print-shop handoff rules."""

    # Catch sensitive requests before asking the model.
    def needs_human(self, text):
        # Send any((word in text for word in ['refund', 'cancel', 'payment', 'card', 'complaint'])) back to the caller.
        return any(
            word in text
            for word in ["refund", "cancel", "payment", "card", "complaint"]
        )
