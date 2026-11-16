# fallback_model.py
# Author: Minh Nguyen


# Group this component’s state and behavior behind one interface.
class FallbackModel:
    # Document the interface for readers and tool-description generation.
    """Ask the first model. If it has no answer, ask the second one."""

    # Store the components and start fresh state for this instance.
    def __init__(self, first, second):
        # Document the interface for readers and tool-description generation.
        """Store the two models, in the order they are asked."""
        # Save first in self.first for the following steps.
        self.first = first
        # Save second in self.second for the following steps.
        self.second = second

    # Return the first model's decision, or the second's if the first has none.
    def decide(self, instructions, history, tools):
        # Document the interface for readers and tool-description generation.
        """Return the first model's decision, or the second's if the first has none."""
        # Save self.first.decide(instructions, history, tools) in decision for the following steps.
        decision = self.first.decide(instructions, history, tools)
        # Check decision is None before choosing the next action.
        if decision is None:
            # Send self.second.decide(instructions, history, tools) back to the caller.
            return self.second.decide(instructions, history, tools)
        # Send decision back to the caller.
        return decision
