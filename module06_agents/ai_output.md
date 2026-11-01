# AI-Generated Class Output

The following is the complete AI-generated class source delivered for Lab 10,
after formatting. Each nonblank line within a class has a preceding comment
explaining what it does and why it is present. The executable files contain the
same annotations; this document preserves their output together for the lab's
AI-use requirement.

The student's task prompt was:

> https://markumreed.github.io/ism3232/docs/week10_lab.html
>
> read the requirements for this lab then proceed to finish, is there is any problem bring back to me before proceed next step

`OrderLookup`, `SupportChatbot`, and `StockLookup` adapt the lab's templates and
exercises. `FAQBook` and `PrintShopAssistant` implement a separate print-shop FAQ
mini-project. No model is called by either program: the classes use dictionaries
and keyword rules. These comments document AI assistance and the reasoning;
they do not certify the student's ability to explain the code independently.

## order_tool.py

```python
# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.


# Define a separate tool so order data stays outside the conversation class.
class OrderLookup:
    # Describe the tool's single responsibility for readers and help().
    """Look up order IDs and statuses without holding a conversation."""

    # Accept the order dictionary when creating a tool so tests can supply data.
    def __init__(self, orders):
        # Document the constructor's purpose so its input is clear.
        """Store the orders this tool can look up."""
        # Keep the supplied dictionary on this object for later lookups.
        self.orders = orders

    # Accept message text so callers do not need to parse order IDs themselves.
    def find_order_id(self, text):
        # Describe the success and missing-ID results for callers.
        """Return the first known ID mentioned in text, or None."""
        # Visit the stored IDs in dictionary order to find the first match.
        for order_id in self.orders:
            # Normalize the message so lowercase IDs match uppercase keys.
            if order_id in text.upper():
                # Return the matching key so the caller can look up its status.
                return order_id
        # Signal a missing match without inventing an order ID.
        return None

    # Expose status lookup separately so finding an ID and reading data differ.
    def find_status(self, order_id):
        # State that an unknown order produces None instead of an exception.
        """Return an order's status, or None if the order is unknown."""
        # Check membership before indexing to avoid a KeyError.
        if order_id in self.orders:
            # Return the stored status rather than creating a fictional one.
            return self.orders[order_id]
        # Let the caller handle missing data with a helpful reply.
        return None
```

## chatbot.py

```python
# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.

HANDOFF_WORDS = ["address", "payment", "card"]


# Define the conversation object separately from its order and stock tools.
class SupportChatbot:
    # Identify the rule-based behavior so it is not mistaken for a real model.
    """A mock support chatbot whose replies come from keyword rules."""

    # Receive both tools so the chatbot gains abilities through composition.
    def __init__(self, name, instructions, order_tool, stock_tool):
        # Explain which state belongs to each newly created chatbot.
        """Store identity, instructions, tools, and a separate history."""
        # Store this object's display name for personalized greetings.
        self.name = name
        # Save instructions for future model work; this mock does not use them.
        self.instructions = instructions
        # Compose the chatbot with an existing tool rather than copying orders.
        self.order_tool = order_tool
        # Store the second tool so inventory stays in a separate object.
        self.stock_tool = stock_tool
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

    # Keep routing separate from history recording to make rule order readable.
    def choose_reply(self, user_message):
        # State that these rules, not a model, determine the response.
        """Choose a mock reply with handoff rules taking priority."""
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
        # Recognize the lab's greeting after checking more specific requests.
        if "hello" in text:
            # Use this object's name so shared class code greets as each bot.
            return f"Hello! I'm {self.name}. I can check an order status for you."
        # Admit the limited capability instead of inventing an unsupported answer.
        return "I'm not sure how to help with that. I can check an order status."

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
```

## stock_tool.py

```python
# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.


# Define an independent stock tool so the chatbot does not own inventory data.
class StockLookup:
    # Explain the tool's responsibility for readers and help().
    """Find known products and read their stock counts."""

    # Accept inventory during construction so different callers can supply it.
    def __init__(self, stock):
        # Explain what information the constructor stores.
        """Store the product-to-count dictionary."""
        # Retain the dictionary on this tool for later inventory lookups.
        self.stock = stock

    # Accept message text to identify which known product the user mentions.
    def find_product(self, text):
        # Specify that a missing match returns None for safe caller handling.
        """Return the first known product in text, or None."""
        # Inspect product keys in insertion order to choose the first match.
        for product in self.stock:
            # Lowercase the message so product recognition ignores text case.
            if product in text.lower():
                # Return the recognized key for the separate count lookup.
                return product
        # Report no match rather than guessing a product.
        return None

    # Provide count lookup as a tool method instead of chatbot data access.
    def count_for(self, product):
        # Distinguish an unknown product from a known product with zero stock.
        """Return a stock count, including zero, or None if unknown."""
        # Test key membership so a zero count is still a successful lookup.
        if product in self.stock:
            # Return the actual stored count without altering inventory.
            return self.stock[product]
        # Signal an unknown product without raising a KeyError.
        return None
```

## my_tool.py

```python
# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.


# Define a read-only FAQ tool so business answers stay outside conversation code.
class FAQBook:
    # Describe the tool's job for readers and help().
    """Find known FAQ topics and retrieve their stored answers."""

    # Receive the answer dictionary so the same tool can serve different shops.
    def __init__(self, answers):
        # Document which information belongs to the tool.
        """Store a dictionary mapping lowercase topics to answers."""
        # Keep the supplied answers as this object's lookup data.
        self.answers = answers

    # Identify a known topic from text without adding conversation behavior.
    def find_topic(self, text):
        # Explain the absence result so callers can handle failed lookups.
        """Return the first known topic in text, or None."""
        # Inspect known topic keys in their dictionary insertion order.
        for topic in self.answers:
            # Normalize user text so topic matching ignores capitalization.
            if topic in text.lower():
                # Return the recognized key so the caller can retrieve its answer.
                return topic
        # Indicate no known topic rather than guessing an answer.
        return None

    # Keep retrieving an answer separate from recognizing its topic.
    def answer_for(self, topic):
        # State the missing-data behavior instead of implying every topic exists.
        """Return the stored answer, or None if no answer is available."""
        # Check the key before indexing so unknown topics do not cause KeyError.
        if topic in self.answers:
            # Return only the stored information without making up shop policies.
            return self.answers[topic]
        # Let the assistant explain a failed lookup safely.
        return None
```

## my_assistant.py

```python
# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.

HANDOFF_WORDS = ["refund", "cancel", "payment", "card", "complaint"]


# Define a separate conversation class that receives the shop's FAQ tool.
class PrintShopAssistant:
    # Explain that keyword rules, not a model, produce the replies.
    """A mock FAQ assistant for the fictional Campus Print Desk."""

    # Accept an existing tool to demonstrate composition rather than inheritance.
    def __init__(self, name, instructions, faq_tool):
        # Describe the state stored separately for each assistant instance.
        """Store the assistant's identity, instructions, tool, and history."""
        # Keep a display name so callers can label the assistant's replies.
        self.name = name
        # Store instructions as metadata without claiming a model reads them.
        self.instructions = instructions
        # Hold the supplied tool so shop answers remain in a separate object.
        self.faq_tool = faq_tool
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
        # Explain that money and order changes take priority over FAQ answers.
        """Route handoffs first, then greetings and tool-backed FAQs."""
        # Normalize matching text while retaining the original text in history.
        text = user_message.lower()
        # Give every configured human-only topic priority over automated answers.
        for word in HANDOFF_WORDS:
            # Detect an issue the read-only FAQ tool cannot resolve.
            if word in text:
                # Direct the user to staff without claiming a ticket was created.
                return "Please contact the print desk staff to handle that request."
        # Handle the known greeting without asking the FAQ tool for a policy.
        if "hello" in text:
            # Introduce this assistant and name the supported FAQ topics.
            return f"Hello! I'm {self.name}. Ask about hours, pricing, or pickup."
        # Let the FAQ response method distinguish known, missing, and unknown data.
        return self.faq_reply(user_message)

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
```
