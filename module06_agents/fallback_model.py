# fallback_model.py
# Author: Minh Nguyen


# Use a second model only when the first is unavailable.
class FallbackModel:
    # Describe this class or method for callers.
    """Ask the first model. If it has no answer, ask the second one."""

    # Keep the supplied data and start fresh state.
    def __init__(self, first, second):
        # Describe this class or method for callers.
        """Store the two models, in the order they are asked."""
        # Try this model first.
        self.first = first
        # Use this model only when the first returns None.
        self.second = second

    # Return the first model's decision, or the second's if the first has none.
    def decide(self, instructions, history, tools):
        # Describe this class or method for callers.
        """Return the first model's decision, or the second's if the first has none."""
        # Try the primary model before considering the fallback.
        decision = self.first.decide(instructions, history, tools)
        # Handle an unavailable model without crashing the conversation.
        if decision is None:
            # Ask the fallback model because the primary model is unavailable.
            return self.second.decide(instructions, history, tools)
        # Keep the primary model's answer when it is available.
        return decision
