# ollama_model.py
# Author: Minh Nguyen

from ollama import ResponseError, chat


# Group this component’s state and behavior behind one interface.
class OllamaModel:
    # Document the interface for readers and tool-description generation.
    """A real AI model that runs on this computer through Ollama."""

    # Define __init__ so callers can Remember which model to ask.
    def __init__(self, model_name):
        # Document the interface for readers and tool-description generation.
        """Remember which model to ask."""
        # Store this value for subsequent validation or processing.
        self.model_name = model_name

    # Define reply so callers can Send the instructions and the conversation to the model. Return its reply.
    def reply(self, instructions, history):
        # Document the interface for readers and tool-description generation.
        """Send the instructions and the conversation to the model. Return its reply."""
        # Store this value for subsequent validation or processing.
        messages = [{"role": "system", "content": instructions}]
        # Store this value for subsequent validation or processing.
        messages = messages + history
        # Handle the expected model connection and response failures.
        try:
            # Store this value for subsequent validation or processing.
            response = chat(model=self.model_name, messages=messages)
        except ConnectionError:
            # Return the result to the caller without performing terminal I/O.
            return None
        except ResponseError:
            # Return the result to the caller without performing terminal I/O.
            return None
        # Return the result to the caller without performing terminal I/O.
        return response.message.content

    # Define decide so callers can Send the conversation and the tools. Return a reply or a tool request.
    def decide(self, instructions, history, tools):
        # Document the interface for readers and tool-description generation.
        """Send the conversation and the tools. Return a reply or a tool request."""
        # Store this value for subsequent validation or processing.
        messages = [{"role": "system", "content": instructions}]
        # Process the collection or bounded loop in a controlled order.
        for message in history:
            # Check this condition before allowing the next operation.
            if message["role"] == "tool":
                # Store this value for subsequent validation or processing.
                messages = messages + self.tool_messages(message)
            else:
                # Record or delegate this operation through the component’s interface.
                messages.append(message)
        # Handle the expected model connection and response failures.
        try:
            # Store this value for subsequent validation or processing.
            response = chat(model=self.model_name, messages=messages, tools=tools)
        except ConnectionError:
            # Return the result to the caller without performing terminal I/O.
            return None
        except ResponseError:
            # Return the result to the caller without performing terminal I/O.
            return None
        # Check this condition before allowing the next operation.
        if response.message.tool_calls:
            # Store this value for subsequent validation or processing.
            call = response.message.tool_calls[0]
            # Return the result to the caller without performing terminal I/O.
            return {"tool": call.function.name, "arguments": call.function.arguments}
        # Return the result to the caller without performing terminal I/O.
        return {"text": response.message.content}

    # Define tool_messages so callers can Turn one tool entry into the two messages Ollama expects.
    def tool_messages(self, message):
        # Document the interface for readers and tool-description generation.
        """Turn one tool entry into the two messages Ollama expects."""
        # Store this value for subsequent validation or processing.
        name = message["tool_name"]
        # Store this value for subsequent validation or processing.
        request = {"function": {"name": name, "arguments": message["arguments"]}}
        # Return the result to the caller without performing terminal I/O.
        return [
            {"role": "assistant", "content": "", "tool_calls": [request]},
            {"role": "tool", "tool_name": name, "content": message["content"]},
        ]
