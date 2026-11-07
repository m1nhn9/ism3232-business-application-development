# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.

HANDOFF_WORDS = ["refund", "cancel", "payment", "card", "complaint"]


# Define a separate conversation class that receives the shop's FAQ tool.
class PrintShopAssistant:
    # Explain that verified shop rules run before the model writes other replies.
    """A print-shop assistant. Rules handle facts and a model handles the rest."""

    # Accept an existing tool and model to build the assistant through composition.
    def __init__(self, name, instructions, faq_tool, model):
        # Describe the state stored separately for each assistant instance.
        """Store the assistant's identity, instructions, tool, and history."""
        # Keep a display name so callers can label the assistant's replies.
        self.name = name
        # Store the verified facts and behavior sent with each model request.
        self.instructions = instructions
        # Hold the supplied tool so shop answers remain in a separate object.
        self.faq_tool = faq_tool
        # Keep the supplied model replaceable so offline tests can use a mock.
        self.model = model
        # Allocate a fresh list for each assistant's own conversation.
        self.history = []

    # Expose a conversation method that records both sides of every turn.
    def respond(self, user_message):
        # Document the recording order and returned result.
        """Record the message, choose and record a reply, then return it."""
        # Save the exact user text and its role before selecting a response.
        self.history.append({"role": "user", "content": user_message})
        # Delegate reply selection so the recording logic stays simple.
        reply = self.choose_reply(user_message)
        # Record the actual assistant reply to complete the conversation turn.
        self.history.append({"role": "assistant", "content": reply})
        # Return the response to the interface without doing terminal I/O here.
        return reply

    # Separate request routing from transcript management.
    def choose_reply(self, user_message):
        # Explain that handoffs and verified FAQs take priority over model text.
        """Route handoffs and tool-backed FAQs first, then ask the model."""
        # Normalize matching text while retaining the original text in history.
        text = user_message.lower()
        # Give every configured human-only topic priority over automated answers.
        for word in HANDOFF_WORDS:
            # Detect an issue the read-only FAQ tool cannot resolve.
            if word in text:
                # Direct the user to staff without claiming a ticket was created.
                return "Please contact the print desk staff to handle that request."
        # Ask the tool to identify whether this message concerns a verified FAQ.
        topic = self.faq_tool.find_topic(user_message)
        # Keep known topics and explicit FAQ requests on the deterministic path.
        if topic is not None or "faq" in text:
            # Let the FAQ method distinguish known, missing, and vague questions.
            return self.faq_reply(user_message)
        # Send all remaining language tasks to the interchangeable model component.
        return self.model_reply()

    # Isolate model failure handling so the assistant never records a None reply.
    def model_reply(self):
        # Describe the safe response returned when the model cannot answer.
        """Ask the model for a reply. Give a safe answer if the model has none."""
        # Send the instructions and full history, including the latest user message.
        reply = self.model.reply(self.instructions, self.history)
        # Interpret None as model unavailability instead of fabricated shop facts.
        if reply is None:
            # Offer a retry without implying that staff or a tool handled the request.
            return "Sorry, I can't answer that right now. Please try again in a moment."
        # Return the model's text so respond can record it as the assistant message.
        return reply

    # Keep FAQ response formatting separate from keyword routing.
    def faq_reply(self, user_message):
        # State that the composed tool, not this assistant, supplies shop answers.
        """Return a stored FAQ answer or a helpful limitation message."""
        # Ask the tool to identify the known topic mentioned by the user.
        topic = self.faq_tool.find_topic(user_message)
        # Handle messages that do not identify one of the stored topics.
        if topic is None:
            # Distinguish a vague FAQ lookup from a completely unsupported request.
            if "faq" in user_message.lower():
                # Offer the available topics so the user can clarify the lookup.
                return "Which topic? I can check hours, pricing, or pickup."
            # Admit unsupported requests instead of inventing shop information.
            return "I'm not sure how to help. I can answer hours, pricing, or pickup."
        # Read the actual answer from the tool once it recognizes a topic.
        answer = self.faq_tool.answer_for(topic)
        # Treat missing data as a failed lookup rather than displaying None.
        if answer is None:
            # Refer the user to staff because an answer cannot be verified here.
            return "I don't have that answer. Please ask the print desk staff."
        # Return the stored shop answer without changing or embellishing it.
        return answer
