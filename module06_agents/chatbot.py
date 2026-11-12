# chatbot.py
# Author: Minh Nguyen

HANDOFF_WORDS = ["payment", "card"]
MAX_TOOL_ROUNDS = 3


# Group this component’s state and behavior behind one interface.
class SupportChatbot:
    # Document the interface for readers and tool-description generation.
    """A support chatbot. The model decides. The toolbox checks every tool request."""

    # Define __init__ so callers can Set up one chatbot with its own name, instructions, tools, model, and history.
    def __init__(self, name, instructions, tools, model):
        # Document the interface for readers and tool-description generation.
        """Set up one chatbot with its own name, instructions, tools, model, and history."""
        # Store this value for subsequent validation or processing.
        self.name = name
        # Store this value for subsequent validation or processing.
        self.instructions = instructions
        # Store this value for subsequent validation or processing.
        self.tools = tools
        # Store this value for subsequent validation or processing.
        self.model = model
        # Store this value for subsequent validation or processing.
        self.history = []

    # Define respond so callers can Record the user's message, choose a reply, record it, and return it.
    def respond(self, user_message):
        # Document the interface for readers and tool-description generation.
        """Record the user's message, choose a reply, record it, and return it."""
        # Record or delegate this operation through the component’s interface.
        self.history.append({"role": "user", "content": user_message})
        # Store this value for subsequent validation or processing.
        reply = self.choose_reply(user_message)
        # Record or delegate this operation through the component’s interface.
        self.history.append({"role": "assistant", "content": reply})
        # Return the result to the caller without performing terminal I/O.
        return reply

    # Define choose_reply so callers can Pass payment questions to a person. Send everything else to the model.
    def choose_reply(self, user_message):
        # Document the interface for readers and tool-description generation.
        """Pass payment questions to a person. Send everything else to the model."""
        # Check this condition before allowing the next operation.
        if self.needs_human(user_message.lower()):
            # Return the result to the caller without performing terminal I/O.
            return "I can't help with that here. I'm passing you to a human agent."
        # Return the result to the caller without performing terminal I/O.
        return self.model_reply()

    # Define needs_human so callers can Return True if the message is about something a person must handle.
    def needs_human(self, text):
        # Document the interface for readers and tool-description generation.
        """Return True if the message is about something a person must handle."""
        # Process the collection or bounded loop in a controlled order.
        for word in HANDOFF_WORDS:
            # Check this condition before allowing the next operation.
            if word in text:
                # Return the result to the caller without performing terminal I/O.
                return True
        # Return the result to the caller without performing terminal I/O.
        return False

    # Define model_reply so callers can Ask the model. Run each tool it asks for, then ask again, up to a limit.
    def model_reply(self):
        # Document the interface for readers and tool-description generation.
        """Ask the model. Run each tool it asks for, then ask again, up to a limit."""
        # Store this value for subsequent validation or processing.
        rounds = 0
        # Process the collection or bounded loop in a controlled order.
        while rounds < MAX_TOOL_ROUNDS:
            # Store this value for subsequent validation or processing.
            tool_list = self.tools.tool_list()
            # Store this value for subsequent validation or processing.
            decision = self.model.decide(self.instructions, self.history, tool_list)
            # Check this condition before allowing the next operation.
            if decision is None:
                # Return the result to the caller without performing terminal I/O.
                return "Sorry, I can't answer that right now. Please try again in a moment."
            # Check this condition before allowing the next operation.
            if "text" in decision:
                # Return the result to the caller without performing terminal I/O.
                return decision["text"]
            # Store this value for subsequent validation or processing.
            name = decision["tool"]
            # Store this value for subsequent validation or processing.
            arguments = decision["arguments"]
            # Store this value for subsequent validation or processing.
            result = self.tools.run(name, arguments, self.history)
            # Record or delegate this operation through the component’s interface.
            self.history.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "arguments": arguments,
                    "content": result,
                }
            )
            # Advance the running count to track progress.
            rounds += 1
        # Return the result to the caller without performing terminal I/O.
        return "Sorry, I couldn't finish that. I'm passing you to a human agent."

    # Define count_user_messages so callers can Return how many messages the user has sent so far.
    def count_user_messages(self):
        # Document the interface for readers and tool-description generation.
        """Return how many messages the user has sent so far."""
        # Store this value for subsequent validation or processing.
        count = 0
        # Process the collection or bounded loop in a controlled order.
        for message in self.history:
            # Check this condition before allowing the next operation.
            if message["role"] == "user":
                # Advance the running count to track progress.
                count += 1
        # Return the result to the caller without performing terminal I/O.
        return count
