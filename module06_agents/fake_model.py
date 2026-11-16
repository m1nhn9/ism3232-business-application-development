# fake_model.py
# Author: Minh Nguyen


# Group this component’s state and behavior behind one interface.
class FakeModel:
    # Document the interface for readers and tool-description generation.
    """A model for tests. It plays back a list of decisions, one per call."""

    # Store the components and start fresh state for this instance.
    def __init__(self, decisions):
        # Document the interface for readers and tool-description generation.
        """Store the decisions to play back, in order."""
        # Save decisions in self.decisions for the following steps.
        self.decisions = decisions
        # Save 0 in self.calls for the following steps.
        self.calls = 0

    # Return the next decision in the list.
    def decide(self, instructions, history, tools):
        # Document the interface for readers and tool-description generation.
        """Return the next decision in the list."""
        # Save self.decisions[self.calls] in decision for the following steps.
        decision = self.decisions[self.calls]
        # Count this completed step with self.calls += 1.
        self.calls += 1
        # Send decision back to the caller.
        return decision
