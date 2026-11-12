# fake_model.py
# Author: Minh Nguyen


# Group this component’s state and behavior behind one interface.
class FakeModel:
    # Document the interface for readers and tool-description generation.
    """A model for tests. It plays back a list of decisions, one per call."""

    # Define __init__ so callers can Store the decisions to play back, in order.
    def __init__(self, decisions):
        # Document the interface for readers and tool-description generation.
        """Store the decisions to play back, in order."""
        # Store this value for subsequent validation or processing.
        self.decisions = decisions
        # Store this value for subsequent validation or processing.
        self.calls = 0

    # Define decide so callers can Return the next decision in the list.
    def decide(self, instructions, history, tools):
        # Document the interface for readers and tool-description generation.
        """Return the next decision in the list."""
        # Store this value for subsequent validation or processing.
        decision = self.decisions[self.calls]
        # Advance the running count to track progress.
        self.calls += 1
        # Return the result to the caller without performing terminal I/O.
        return decision
