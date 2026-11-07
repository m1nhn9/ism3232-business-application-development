# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.


# Define a second simple model to prove the chatbot accepts interchangeable objects.
class EchoModel:
    # Explain that this model repeats input and does not call an AI service.
    """A model that repeats the last message. It needs no AI and no internet."""

    # Keep the same two inputs expected by every model used by the chatbot.
    def reply(self, instructions, history):
        # Describe the prefix added to the newest conversation message.
        """Return the last message with a few words in front of it."""
        # Read the original content without lowercasing so the echo remains exact.
        last_message = history[-1]["content"]
        # Build and return the deterministic reply required by Exercise 2.
        return f"You said: {last_message}"
