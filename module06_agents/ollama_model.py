# ollama_model.py
# Author: Minh Nguyen

from ollama import ResponseError, chat


# Translate between the chatbot and Ollama.
class OllamaModel:
    # Describe this class or method for callers.
    """A real AI model that runs on this computer through Ollama."""

    # Keep the supplied data and start fresh state.
    def __init__(self, model_name):
        # Describe this class or method for callers.
        """Remember which model to ask."""
        # Remember which downloaded Ollama model to call.
        self.model_name = model_name

    # Send the instructions and the conversation to the model. Return its reply.
    def reply(self, instructions, history):
        # Describe this class or method for callers.
        """Send the instructions and the conversation to the model. Return its reply."""
        # Put the instructions first as a system message.
        messages = [{"role": "system", "content": instructions}]
        # Include earlier turns because the model has no memory between calls.
        messages = messages + history
        # Handle the expected model connection and response failures.
        try:
            # Ask Ollama for a text reply.
            response = chat(model=self.model_name, messages=messages)
        except ConnectionError:
            # Signal that no result is available.
            return None
        except ResponseError:
            # Signal that no result is available.
            return None
        # Extract the text from Ollama's response.
        return response.message.content

    # Send the conversation and the tools. Return a reply or a tool request.
    def decide(self, instructions, history, tools):
        # Describe this class or method for callers.
        """Send the conversation and the tools. Return a reply or a tool request."""
        # Put the instructions first as a system message.
        messages = [{"role": "system", "content": instructions}]
        # Read the conversation in order.
        for message in history:
            # Expand stored tool entries into Ollama's request/result format.
            if message["role"] == "tool":
                # Add both the tool request and its result.
                messages = messages + self.tool_messages(message)
            else:
                # Copy user and assistant messages into the request.
                messages.append(message)
        # Handle the expected model connection and response failures.
        try:
            # Send the tool descriptions with the conversation.
            response = chat(model=self.model_name, messages=messages, tools=tools)
        except ConnectionError:
            # Signal that no result is available.
            return None
        except ResponseError:
            # Signal that no result is available.
            return None
        # Check whether the model requested a tool instead of text.
        if response.message.tool_calls:
            # Handle the first requested tool; the loop can ask again.
            call = response.message.tool_calls[0]
            # Return the requested name and arguments for toolbox validation.
            return {"tool": call.function.name, "arguments": call.function.arguments}
        # Return a text decision when no tool was requested.
        return {"text": response.message.content}

    # Turn one tool entry into the two messages Ollama expects.
    def tool_messages(self, message):
        # Describe this class or method for callers.
        """Turn one tool entry into the two messages Ollama expects."""
        # Read the name recorded with the tool result.
        name = message["tool_name"]
        # Rebuild the model's tool request so Ollama sees what it asked for.
        request = {"function": {"name": name, "arguments": message["arguments"]}}
        # Send the original tool request followed by its result.
        return [
            {"role": "assistant", "content": "", "tool_calls": [request]},
            {"role": "tool", "tool_name": name, "content": message["content"]},
        ]
