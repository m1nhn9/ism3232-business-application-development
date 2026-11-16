# fake_model.py
# Author: Minh Nguyen


# Play back fixed decisions for repeatable tests.
class FakeModel:
    # Describe this class or method for callers.
    """A model for tests. It plays back a list of decisions, one per call."""

    # Keep the supplied data and start fresh state.
    def __init__(self, decisions):
        # Describe this class or method for callers.
        """Store the decisions to play back, in order."""
        # Keep the scripted decisions in their playback order.
        self.decisions = decisions
        # Start playback at the first decision.
        self.calls = 0

    # Return the next decision in the list.
    def decide(self, instructions, history, tools):
        # Describe this class or method for callers.
        """Return the next decision in the list."""
        # Read the decision for this test call.
        decision = self.decisions[self.calls]
        # Move to the next scripted decision.
        self.calls += 1
        # Keep the primary model's answer when it is available.
        return decision
