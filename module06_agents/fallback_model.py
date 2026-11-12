# fallback_model.py
# Author: Minh Nguyen


# Group this component’s state and behavior behind one interface.
class FallbackModel:
    # Document the interface for readers and tool-description generation.
    """Ask the first model. If it has no answer, ask the second one."""

    # Define __init__ so callers can Store the two models, in the order they are asked.
    def __init__(self, first, second):
        # Document the interface for readers and tool-description generation.
        """Store the two models, in the order they are asked."""
        # Store this value for subsequent validation or processing.
        self.first = first
        # Store this value for subsequent validation or processing.
        self.second = second

    # Define decide so callers can Return the first model's decision, or the second's if the first has none.
    def decide(self, instructions, history, tools):
        # Document the interface for readers and tool-description generation.
        """Return the first model's decision, or the second's if the first has none."""
        # Store this value for subsequent validation or processing.
        decision = self.first.decide(instructions, history, tools)
        # Check this condition before allowing the next operation.
        if decision is None:
            # Return the result to the caller without performing terminal I/O.
            return self.second.decide(instructions, history, tools)
        # Return the result to the caller without performing terminal I/O.
        return decision
