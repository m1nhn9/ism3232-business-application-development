# ollama_model.py
# Author: Minh Nguyen

from ollama import ResponseError, chat


# Group this component’s state and behavior behind one interface.
class OllamaModel:
    # Document the interface for readers and tool-description generation.
    """A real AI model that runs on this computer through Ollama."""

    # Store the components and start fresh state for this instance.
    def __init__(self, model_name):
        # Document the interface for readers and tool-description generation.
        """Remember which model to ask."""
        # Save model_name in self.model_name for the following steps.
        self.model_name = model_name

    # Send the instructions and the conversation to the model. Return its reply.
    def reply(self, instructions, history):
        # Document the interface for readers and tool-description generation.
        """Send the instructions and the conversation to the model. Return its reply."""
        # Save [{'role': 'system', 'content': instructions}] in messages for the following steps.
        messages = [{"role": "system", "content": instructions}]
        # Save messages + history in messages for the following steps.
        messages = messages + history
        # Handle the expected model connection and response failures.
        try:
            # Save chat(model=self.model_name, messages=messages) in response for the following steps.
            response = chat(model=self.model_name, messages=messages)
        except ConnectionError:
            # Send None back to the caller.
            return None
        except ResponseError:
            # Send None back to the caller.
            return None
        # Send response.message.content back to the caller.
        return response.message.content

    # Send the conversation and the tools. Return a reply or a tool request.
    def decide(self, instructions, history, tools):
        # Document the interface for readers and tool-description generation.
        """Send the conversation and the tools. Return a reply or a tool request."""
        # Save [{'role': 'system', 'content': instructions}] in messages for the following steps.
        messages = [{"role": "system", "content": instructions}]
        # Check each message in history.
        for message in history:
            # Check message['role'] == 'tool' before choosing the next action.
            if message["role"] == "tool":
                # Save messages + self.tool_messages(message) in messages for the following steps.
                messages = messages + self.tool_messages(message)
            else:
                # Run messages.append(message) to record or apply this step.
                messages.append(message)
        # Handle the expected model connection and response failures.
        try:
            # Save chat(model=self.model_name, messages=messages, tools=tools) in response for the following steps.
            response = chat(model=self.model_name, messages=messages, tools=tools)
        except ConnectionError:
            # Send None back to the caller.
            return None
        except ResponseError:
            # Send None back to the caller.
            return None
        # Check response.message.tool_calls before choosing the next action.
        if response.message.tool_calls:
            # Save response.message.tool_calls[0] in call for the following steps.
            call = response.message.tool_calls[0]
            # Send {'tool': call.function.name, 'arguments': call.function.arguments} back to the caller.
            return {"tool": call.function.name, "arguments": call.function.arguments}
        # Send {'text': response.message.content} back to the caller.
        return {"text": response.message.content}

    # Turn one tool entry into the two messages Ollama expects.
    def tool_messages(self, message):
        # Document the interface for readers and tool-description generation.
        """Turn one tool entry into the two messages Ollama expects."""
        # Save message['tool_name'] in name for the following steps.
        name = message["tool_name"]
        # Save {'function': {'name': name, 'arguments': message['arguments']}} in request for the following steps.
        request = {"function": {"name": name, "arguments": message["arguments"]}}
        # Send [{'role': 'assistant', 'content': '', 'tool_calls': [request]}, {'role': 'tool', 'tool_name': name, 'content': message['content']}] back to the caller.
        return [
            {"role": "assistant", "content": "", "tool_calls": [request]},
            {"role": "tool", "tool_name": name, "content": message["content"]},
        ]
