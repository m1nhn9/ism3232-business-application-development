# keyword_model.py
# Author: Minh Nguyen


# Provide simple keyword decisions when Ollama is unavailable.
class KeywordModel:
    # Describe this class or method for callers.
    """A stand-in model that decides with keyword rules. It needs no AI."""

    # Return either reply text or a tool request.
    def decide(self, instructions, history, tools):
        # Describe this class or method for callers.
        """Return a reply or a tool request, based on the last message."""
        # Read the latest message or tool result.
        last = history[-1]
        # After a tool call, use its result as the reply.
        if last["role"] == "tool":
            # Return the checked result or the message the caller should display.
            return {"text": last["content"]}
        # Ignore capitalization when matching keywords.
        text = last["content"].lower()
        # Use the order lookup for messages containing order.
        if "order" in text:
            # Return the checked result or the message the caller should display.
            return {"tool": "look_up_order", "arguments": {"order_id": last["content"]}}
        # Use the stock tool for messages containing stock.
        if "stock" in text:
            # Return the checked result or the message the caller should display.
            return {"tool": "check_stock", "arguments": {"item": last["content"]}}
        # Recognize the fallback model's greeting.
        if "hello" in text:
            # Return the checked result or the message the caller should display.
            return {"text": "Hello! How can I help you today?"}
        # Return the checked result or the message the caller should display.
        return {
            "text": "I'm not sure how to help with that. I can check an order or stock."
        }
