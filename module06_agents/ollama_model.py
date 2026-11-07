# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.

from ollama import ResponseError, chat


# Wrap Ollama behind the same reply method used by the mock and echo models.
class OllamaModel:
    # Describe that this adapter talks to a model running on the local computer.
    """A real AI model that runs on this computer through Ollama."""

    # Accept a model name so callers decide which downloaded model to use.
    def __init__(self, model_name):
        # Explain the one setting retained by this adapter instance.
        """Remember which model to ask."""
        # Store the requested Ollama model identifier for every later reply.
        self.model_name = model_name

    # Present the common model interface expected by both chatbot classes.
    def reply(self, instructions, history):
        # Describe the successful reply and the safe failure signal.
        """Send instructions and history to the model, or return None on failure."""
        # Put private behavioral instructions first with the system role.
        messages = [{"role": "system", "content": instructions}]
        # Add all user and assistant messages so the stateless model has context.
        messages = messages + history
        # Mark the external model call as the operation that may be unavailable.
        try:
            # Ask the configured local model to continue the supplied conversation.
            response = chat(model=self.model_name, messages=messages)
        # Catch a stopped or unreachable Ollama server without hiding other bugs.
        except ConnectionError:
            # Signal model unavailability so the chatbot can choose safe wording.
            return None
        # Catch Ollama errors such as a requested model that was not downloaded.
        except ResponseError:
            # Use the same missing-answer signal for every expected Ollama failure.
            return None
        # Extract only the assistant text from Ollama's structured response object.
        return response.message.content
