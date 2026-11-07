# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.


# Define a predictable stand-in so tests do not need Ollama or network access.
class MockModel:
    # Describe why this model is suitable for repeatable offline tests.
    """A stand-in for an AI model. It gives the same simple replies every time."""

    # Match the same method signature used by the real model adapter.
    def reply(self, instructions, history):
        # State that the most recent user message controls this fixed response.
        """Return a fixed reply based on the last message in the history."""
        # Normalize the latest content so greeting detection ignores capitalization.
        last_message = history[-1]["content"].lower()
        # Check for the one greeting behavior required by the lab's tests.
        if "hello" in last_message:
            # Return a stable greeting so an exact test assertion is reliable.
            return "Hello! How can I help you today?"
        # Return a stable limitation for every other message instead of inventing facts.
        return "I'm not sure how to help with that. I can check an order or stock."
