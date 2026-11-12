# keyword_model.py
# Author: Minh Nguyen


# Group this component’s state and behavior behind one interface.
class KeywordModel:
    # Document the interface for readers and tool-description generation.
    """A stand-in model that decides with keyword rules. It needs no AI."""

    # Define decide so callers can Return a reply or a tool request, based on the last message.
    def decide(self, instructions, history, tools):
        # Document the interface for readers and tool-description generation.
        """Return a reply or a tool request, based on the last message."""
        # Store this value for subsequent validation or processing.
        last = history[-1]
        # Check this condition before allowing the next operation.
        if last["role"] == "tool":
            # Return the result to the caller without performing terminal I/O.
            return {"text": last["content"]}
        # Store this value for subsequent validation or processing.
        text = last["content"].lower()
        # Check this condition before allowing the next operation.
        if "order" in text:
            # Return the result to the caller without performing terminal I/O.
            return {"tool": "look_up_order", "arguments": {"order_id": last["content"]}}
        # Check this condition before allowing the next operation.
        if "stock" in text:
            # Return the result to the caller without performing terminal I/O.
            return {"tool": "check_stock", "arguments": {"item": last["content"]}}
        # Check this condition before allowing the next operation.
        if "hello" in text:
            # Return the result to the caller without performing terminal I/O.
            return {"text": "Hello! How can I help you today?"}
        # Return the result to the caller without performing terminal I/O.
        return {
            "text": "I'm not sure how to help with that. I can check an order or stock."
        }
