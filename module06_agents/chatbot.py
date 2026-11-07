# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.

HANDOFF_WORDS = ["address", "payment", "card"]


# Define the conversation object separately from its order and stock tools.
class SupportChatbot:
    # Clarify that exact rules protect important paths while a model writes the rest.
    """A support chatbot. Rules handle what must be right. A model handles the rest."""

    # Receive both tools and a model so each ability remains a separate component.
    def __init__(self, name, instructions, order_tool, stock_tool, model):
        # Explain which state belongs to each newly created chatbot.
        """Store identity, instructions, tools, and a separate history."""
        # Store this object's display name for personalized greetings.
        self.name = name
        # Save the system instructions that will be sent with each model request.
        self.instructions = instructions
        # Compose the chatbot with an existing tool rather than copying orders.
        self.order_tool = order_tool
        # Store the second tool so inventory stays in a separate object.
        self.stock_tool = stock_tool
        # Store the supplied model so tests can replace the real model with a mock.
        self.model = model
        # Create a new list per object so two chatbots do not share history.
        self.history = []

    # Offer one public entry point that records each conversation turn.
    def respond(self, user_message):
        # Describe the recording and return contract for callers and tests.
        """Record the user message and reply, then return the reply."""
        # Keep the original message and role so the transcript is complete.
        self.history.append({"role": "user", "content": user_message})
        # Choose the response before saving it as the assistant's next message.
        reply = self.choose_reply(user_message)
        # Record the assistant role and exact response to complete the turn.
        self.history.append({"role": "assistant", "content": reply})
        # Give the response to the CLI or test without printing inside the class.
        return reply

    # Keep routing separate so exact rules visibly run before model-generated text.
    def choose_reply(self, user_message):
        # Describe the safety boundary between deterministic rules and the model.
        """Use a rule when one applies. Otherwise ask the model."""
        # Normalize only the matching text while preserving original history.
        text = user_message.lower()
        # Check sensitive requests first even if they also mention an order.
        if self.needs_human(text):
            # Request human handling because this tool cannot change accounts.
            return "I can't help with that here. I'm passing you to a human agent."
        # Route order questions to the tool-backed order response method.
        if "order" in text:
            # Pass the original message to preserve its ID for tool matching.
            return self.order_reply(user_message)
        # Route stock questions separately to keep the data sources distinct.
        if "stock" in text:
            # Let the stock response method identify the product and its count.
            return self.stock_reply(user_message)
        # Send all remaining language tasks to the interchangeable model component.
        return self.model_reply()

    # Isolate model failure handling so every caller receives a usable string.
    def model_reply(self):
        # Explain that a missing model answer is converted into a safe response.
        """Ask the model for a reply. Give a safe answer if the model has none."""
        # Give the model its instructions and the history containing the new message.
        reply = self.model.reply(self.instructions, self.history)
        # Treat None as an unavailable model rather than recording None in history.
        if reply is None:
            # Ask the customer to retry without claiming that a request was handled.
            return "Sorry, I can't answer that right now. Please try again in a moment."
        # Return model text unchanged so the caller can record and display it.
        return reply

    # Keep escalation checks in a method so routing can prioritize them.
    def needs_human(self, text):
        # Explain what True means to the response router.
        """Return True when the message contains a handoff keyword."""
        # Examine each configured keyword so one match is enough to escalate.
        for word in HANDOFF_WORDS:
            # Test whether the normalized message contains this sensitive topic.
            if word in text:
                # Stop searching because the request needs a person.
                return True
        # Allow ordinary automated handling when no handoff word matched.
        return False

    # Separate order replies from routing so the tool owns order knowledge.
    def order_reply(self, user_message):
        # Describe that this method delegates order lookup to the composed tool.
        """Use the order tool to answer an order question."""
        # Ask the tool to locate a known ID instead of parsing orders here.
        order_id = self.order_tool.find_order_id(user_message)
        # Treat a missing known ID as incomplete input rather than guessing.
        if order_id is None:
            # Ask for clarification so unknown IDs do not cause a crash.
            return "Which order? Please send an order ID like A100."
        # Read the actual stored status from the tool after finding the ID.
        status = self.order_tool.find_status(order_id)
        # Present the tool's result in the format required by the lab.
        return f"Order {order_id} is {status}."

    # Add stock behavior through a method and a tool rather than stock data here.
    def stock_reply(self, user_message):
        # Describe the inventory lookup performed for the response router.
        """Use the stock tool to answer a product availability question."""
        # Delegate product recognition to the object that owns inventory data.
        product = self.stock_tool.find_product(user_message)
        # Stop when the question does not mention a known product.
        if product is None:
            # Ask for a product instead of fabricating availability.
            return "Which product? Please name the item you want me to check."
        # Fetch the inventory count, including zero for an out-of-stock item.
        count = self.stock_tool.count_for(product)
        # Return the actual inventory count in the exercise's expected format.
        return f"We have {count} of the {product} in stock."

    # Implement Exercise 2 without counting assistant replies as user messages.
    def count_user_messages(self):
        # Explain the distinction between user count and total history length.
        """Return the number of user-role entries in this bot's history."""
        # Begin a new accumulator each time the count is requested.
        count = 0
        # Examine only this object's history so conversations stay independent.
        for message in self.history:
            # Count user turns while skipping assistant-role entries.
            if message["role"] == "user":
                # Add one for the matching history entry.
                count += 1
        # Return the finished count so callers and tests can use it.
        return count
