# Week 11 AI-Generated Class Output

This file preserves the class code generated for Lab 11. Each executable class
line has an adjacent comment explaining what it does and why, as required by
the lab. The unchanged Week 10 class code remains archived in
`ai_output.md`; the output below records every class addition or replacement
made for Week 11.

The student's task prompt was:

> https://markumreed.github.io/ism3232/docs/week11_reading.html
>
> read this lab requirements for this week then proceed, come to me if theres
> any problems

## `SupportChatbot` Week 11 additions and replacements

```python
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
```

## `PrintShopAssistant` Week 11 additions and replacements

```python
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
```

## New model classes

```python
# Define a predictable stand-in so tests do not need Ollama or network access.
class MockModel:
    # Describe why this model is suitable for repeatable offline tests.
    """A stand-in for an AI model. It gives the same simple replies every time."""

    # Match the same method signature used by the real model adapter.
    def reply(self, instructions, history):
        # State that the most recent user message controls this fixed response.
        """Return a fixed reply based on the last message in the history."""
        # Normalize the latest content so greeting detection ignores capitalization.
        last_message = history[-1]["content"].lower()
        # Check for the one greeting behavior required by the lab's tests.
        if "hello" in last_message:
            # Return a stable greeting so an exact test assertion is reliable.
            return "Hello! How can I help you today?"
        # Return a stable limitation for every other message instead of inventing facts.
        return "I'm not sure how to help with that. I can check an order or stock."


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
```

## Offline failure test doubles

```python
# Define an unavailable stand-in so the chatbot's own fallback can be tested.
class SilentModel:
    # Explain that this object deliberately provides no answer.
    """A model that never has an answer, like Ollama when it is switched off."""

    # Match the reply interface used by every model component in the lab.
    def reply(self, instructions, history):
        # Signal unavailability exactly as the real adapter does on expected errors.
        return None


# Define an unavailable model so the assistant's safe fallback is tested directly.
class SilentModel:
    # Explain that None represents an expected model outage.
    """A model that never has an answer, like Ollama when it is switched off."""

    # Keep the common model signature even though this stand-in ignores its inputs.
    def reply(self, instructions, history):
        # Return the same failure signal produced by OllamaModel on expected errors.
        return None
```
