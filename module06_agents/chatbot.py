# chatbot.py
# Author: Minh Nguyen

HANDOFF_WORDS = ["payment", "card"]
MAX_TOOL_ROUNDS = 3


# Group this component’s state and behavior behind one interface.
class SupportChatbot:
    # Document the interface for readers and tool-description generation.
    """A support chatbot. The model decides. The toolbox checks every tool request."""

    # Store the components and start fresh state for this instance.
    def __init__(self, name, instructions, tools, model):
        # Document the interface for readers and tool-description generation.
        """Set up one chatbot with its own name, instructions, tools, model, and history."""
        # Save name in self.name for the following steps.
        self.name = name
        # Save instructions in self.instructions for the following steps.
        self.instructions = instructions
        # Save tools in self.tools for the following steps.
        self.tools = tools
        # Save model in self.model for the following steps.
        self.model = model
        # Save [] in self.history for the following steps.
        self.history = []

    # Record the user's message, choose a reply, record it, and return it.
    def respond(self, user_message):
        # Document the interface for readers and tool-description generation.
        """Record the user's message, choose a reply, record it, and return it."""
        # Run self.history.append({'role': 'user', 'content': user_message}) to record or apply this step.
        self.history.append({"role": "user", "content": user_message})
        # Save self.choose_reply(user_message) in reply for the following steps.
        reply = self.choose_reply(user_message)
        # Run self.history.append({'role': 'assistant', 'content': reply}) to record or apply this step.
        self.history.append({"role": "assistant", "content": reply})
        # Send reply back to the caller.
        return reply

    # Pass payment questions to a person. Send everything else to the model.
    def choose_reply(self, user_message):
        # Document the interface for readers and tool-description generation.
        """Pass payment questions to a person. Send everything else to the model."""
        # Check self.needs_human(user_message.lower()) before choosing the next action.
        if self.needs_human(user_message.lower()):
            # Send "I can't help with that here. I'm passing you to a human agent." back to the caller.
            return "I can't help with that here. I'm passing you to a human agent."
        # Send self.model_reply() back to the caller.
        return self.model_reply()

    # Catch sensitive requests before asking the model.
    def needs_human(self, text):
        # Document the interface for readers and tool-description generation.
        """Return True if the message is about something a person must handle."""
        # Check each word in HANDOFF_WORDS.
        for word in HANDOFF_WORDS:
            # Check word in text before choosing the next action.
            if word in text:
                # Send True back to the caller.
                return True
        # Send False back to the caller.
        return False

    # Ask the model. Run each tool it asks for, then ask again, up to a limit.
    def model_reply(self):
        # Document the interface for readers and tool-description generation.
        """Ask the model. Run each tool it asks for, then ask again, up to a limit."""
        # Save 0 in rounds for the following steps.
        rounds = 0
        # Limit tool rounds with rounds < MAX_TOOL_ROUNDS to prevent an endless loop.
        while rounds < MAX_TOOL_ROUNDS:
            # Save self.tools.tool_list() in tool_list for the following steps.
            tool_list = self.tools.tool_list()
            # Save self.model.decide(self.instructions, self.history, tool_list) in decision for the following steps.
            decision = self.model.decide(self.instructions, self.history, tool_list)
            # Check decision is None before choosing the next action.
            if decision is None:
                # Send "Sorry, I can't answer that right now. Please try again in a moment." back to the caller.
                return "Sorry, I can't answer that right now. Please try again in a moment."
            # Check 'text' in decision before choosing the next action.
            if "text" in decision:
                # Send decision['text'] back to the caller.
                return decision["text"]
            # Save decision['tool'] in name for the following steps.
            name = decision["tool"]
            # Save decision['arguments'] in arguments for the following steps.
            arguments = decision["arguments"]
            # Save self.tools.run(name, arguments, self.history) in result for the following steps.
            result = self.tools.run(name, arguments, self.history)
            # Run self.history.append({'role': 'tool', 'tool_name': name, 'arguments': arguments, 'content': result}) to record or apply this step.
            self.history.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "arguments": arguments,
                    "content": result,
                }
            )
            # Count this completed step with rounds += 1.
            rounds += 1
        # Send "Sorry, I couldn't finish that. I'm passing you to a human agent." back to the caller.
        return "Sorry, I couldn't finish that. I'm passing you to a human agent."

    # Return how many messages the user has sent so far.
    def count_user_messages(self):
        # Document the interface for readers and tool-description generation.
        """Return how many messages the user has sent so far."""
        # Save 0 in count for the following steps.
        count = 0
        # Check each message in self.history.
        for message in self.history:
            # Check message['role'] == 'user' before choosing the next action.
            if message["role"] == "user":
                # Count this completed step with count += 1.
                count += 1
        # Send count back to the caller.
        return count
