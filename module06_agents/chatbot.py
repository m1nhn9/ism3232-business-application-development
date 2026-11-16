# chatbot.py
# Author: Minh Nguyen

HANDOFF_WORDS = ["payment", "card"]
MAX_TOOL_ROUNDS = 3


# Keep conversation history and run the model/tool loop.
class SupportChatbot:
    # Describe this class or method for callers.
    """A support chatbot. The model decides. The toolbox checks every tool request."""

    # Keep the supplied data and start fresh state.
    def __init__(self, name, instructions, tools, model):
        # Describe this class or method for callers.
        """Set up one chatbot with its own name, instructions, tools, model, and history."""
        # Keep the name used when displaying replies.
        self.name = name
        # Keep the instructions sent to the model on every call.
        self.instructions = instructions
        # Use the supplied toolbox to check every tool request.
        self.tools = tools
        # Keep the supplied model so tests can substitute a fake.
        self.model = model
        # Start a separate conversation history for this bot.
        self.history = []

    # Record the user's message, choose a reply, record it, and return it.
    def respond(self, user_message):
        # Describe this class or method for callers.
        """Record the user's message, choose a reply, record it, and return it."""
        # Record the customer's words before asking the model.
        self.history.append({"role": "user", "content": user_message})
        # Choose a response after recording the user's message.
        reply = self.choose_reply(user_message)
        # Keep the final reply so the next call can see it.
        self.history.append({"role": "assistant", "content": reply})
        # Return the reply for display.
        return reply

    # Pass payment questions to a person. Send everything else to the model.
    def choose_reply(self, user_message):
        # Describe this class or method for callers.
        """Pass payment questions to a person. Send everything else to the model."""
        # Send sensitive questions to a person before calling the model.
        if self.needs_human(user_message.lower()):
            # Send the customer to a person.
            return "I can't help with that here. I'm passing you to a human agent."
        # Ask the model about messages that do not need a handoff.
        return self.model_reply()

    # Catch sensitive requests before asking the model.
    def needs_human(self, text):
        # Describe this class or method for callers.
        """Return True if the message is about something a person must handle."""
        # Check each payment keyword.
        for word in HANDOFF_WORDS:
            # One sensitive keyword is enough for a handoff.
            if word in text:
                # Report a match.
                return True
        # Report that no match was found.
        return False

    # Ask the model. Run each tool it asks for, then ask again, up to a limit.
    def model_reply(self):
        # Describe this class or method for callers.
        """Ask the model. Run each tool it asks for, then ask again, up to a limit."""
        # Start counting tool rounds for this user message.
        rounds = 0
        # Stop after three rounds if the model keeps asking for tools.
        while rounds < MAX_TOOL_ROUNDS:
            # Give the model the methods it is allowed to request.
            tool_list = self.tools.tool_list()
            # Ask for either a reply or a tool request using the full history.
            decision = self.model.decide(self.instructions, self.history, tool_list)
            # Handle an unavailable model without crashing the conversation.
            if decision is None:
                # Give a safe retry message when the model is unavailable.
                return "Sorry, I can't answer that right now. Please try again in a moment."
            # Finish the turn when the model returns text.
            if "text" in decision:
                # Use the model's final text as the reply.
                return decision["text"]
            # Read which tool the model wants to use.
            name = decision["tool"]
            # Read the values the model supplied for that tool.
            arguments = decision["arguments"]
            # Check the request before running the tool.
            result = self.tools.run(name, arguments, self.history)
            # Record the tool name, arguments, and result for the next model call.
            self.history.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "arguments": arguments,
                    "content": result,
                }
            )
            # Count this tool round toward the limit.
            rounds += 1
        # Send the customer to a person.
        return "Sorry, I couldn't finish that. I'm passing you to a human agent."

    # Return how many messages the user has sent so far.
    def count_user_messages(self):
        # Describe this class or method for callers.
        """Return how many messages the user has sent so far."""
        # Start counting user turns, excluding tools and assistant replies.
        count = 0
        # Check each message in self.history.
        for message in self.history:
            # Count only messages typed by the customer.
            if message["role"] == "user":
                # Count this user message.
                count += 1
        # Return the number of user turns.
        return count
