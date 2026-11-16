# Week 12: AI Assistance and Class Code

I used AI assistance to adapt the lab templates and build the Week 12 tools,
guardrails, and approval queues. The code below includes comments explaining
what each part does. I still need to review the code and be able to explain it
myself, as the lab requires. My Week 10 and Week 11 files document the earlier
versions of the project.

## order_tool.py

```python
# order_tool.py
# Author: Minh Nguyen


# Keep order data outside the chatbot.
class OrderLookup:
    # Describe this class or method for callers.
    """A tool that knows about orders. It knows nothing about chatting."""

    # Keep the supplied data and start fresh state.
    def __init__(self, orders):
        # Describe this class or method for callers.
        """Store the orders this tool can look up."""
        # Keep the order records supplied by the caller.
        self.orders = orders

    # Return the first known order ID mentioned in text, or None.
    def find_order_id(self, text):
        # Describe this class or method for callers.
        """Return the first known order ID mentioned in text, or None."""
        # Search the known order IDs.
        for order_id in self.orders:
            # Recognize known IDs even when the message uses lowercase.
            if order_id in text.upper():
                # Return the recognized order key.
                return order_id
        # Signal that no result is available.
        return None

    # Return the status of one order, or None if there is no such order.
    def find_status(self, order_id):
        # Describe this class or method for callers.
        """Return the status of one order, or None if there is no such order."""
        # Check that the exact order key exists before reading it.
        if order_id in self.orders:
            # Return the checked result or the message the caller should display.
            return self.orders[order_id]["status"]
        # Signal that no result is available.
        return None

    # Look up the status of one order.
    def look_up_order(self, order_id):
        # Describe this class or method for callers.
        """Look up the status of one order.

        Args:
            order_id: The order ID, like A100.
        """
        # Find a known order ID in the supplied text.
        found = self.find_order_id(order_id)
        # Handle an unknown ID without inventing an order.
        if found is None:
            # Ask for a valid order ID.
            return "No order with that ID was found. Order IDs look like A100."
        # Return the checked result or the message the caller should display.
        return f"Order {found} is {self.find_status(found)}."

    # Change the shipping address on one order. Only an approval calls this.
    def change_address(self, order_id, new_address):
        # Describe this class or method for callers.
        """Change the shipping address on one order. Only an approval calls this."""
        # Apply the address change after the queue approves it.
        self.orders[order_id]["address"] = new_address

    # Say whether one order can be returned yet.
    def check_return(self, order_id):
        # Describe this class or method for callers.
        """Say whether one order can be returned yet.

        Args:
            order_id: The order ID, like A100.
        """
        # Find a known order ID in the supplied text.
        found = self.find_order_id(order_id)
        # Handle an unknown ID without inventing an order.
        if found is None:
            # Ask for a valid order ID.
            return "No order with that ID was found. Order IDs look like A100."
        # Allow returns only after delivery under the lab's policy.
        if self.find_status(found) == "delivered":
            # Explain the lab's return policy for delivered orders.
            return f"Order {found} was delivered, so it can be returned within 30 days."
        # Explain that this order has not been delivered yet.
        return f"Order {found} has not been delivered, so it cannot be returned yet."
```

## stock_tool.py

```python
# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.


# Define an independent stock tool so the chatbot does not own inventory data.
class StockLookup:
    # Describe the inventory tool before defining its methods.
    """Find known products and read their stock counts."""

    # Check how many of one product are in stock.
    def check_stock(self, item):
        # Describe this class or method for callers.
        """Check how many of one product are in stock.

        Args:
            item: The product name, like rain jacket.
        """
        # Find the stored product mentioned in the request.
        product = self.find_product(item)
        # Stop when the inventory has no matching product.
        if product is None:
            # Return the checked result or the message the caller should display.
            return "That product was not found."
        # Return the checked result or the message the caller should display.
        return f"We have {self.count_for(product)} of the {product} in stock."

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
        # Signal that no result is available.
        return None

    # Provide count lookup as a tool method instead of chatbot data access.
    def count_for(self, product):
        # Distinguish an unknown product from a known product with zero stock.
        """Return a stock count, including zero, or None if unknown."""
        # Test key membership so a zero count is still a successful lookup.
        if product in self.stock:
            # Return the actual stored count without altering inventory.
            return self.stock[product]
        # Signal that no result is available.
        return None
```

## change_queue.py

```python
# change_queue.py
# Author: Minh Nguyen


# Hold proposed address changes until staff decide.
class ChangeQueue:
    # Describe this class or method for callers.
    """Changes waiting for a person to approve. Nothing changes until they do."""

    # Keep the supplied data and start fresh state.
    def __init__(self, order_tool):
        # Describe this class or method for callers.
        """Start with no requests. Approved changes go through the order tool."""
        # Keep the order tool used for lookups and approved changes.
        self.order_tool = order_tool
        # Start with no requests waiting for staff.
        self.requests = []

    # Ask staff to change the shipping address on one order. Staff must approve it.
    def request_address_change(self, order_id, new_address):
        # Describe this class or method for callers.
        """Ask staff to change the shipping address on one order. Staff must approve it.

        Args:
            order_id: The order ID, like A100.
            new_address: The full new shipping address.
        """
        # Match lowercase IDs to the uppercase order keys.
        order_id = order_id.upper()
        # Require an exact order key so A1000 cannot change A100.
        if self.order_tool.find_status(order_id) is None:
            # Ask for a valid order ID.
            return "No order with that ID was found. Order IDs look like A100."
        # Give the new request the next available number.
        number = len(self.requests) + 1
        # Save the proposed change with a waiting status.
        request = {
            "number": number,
            "order_id": order_id,
            "new_address": new_address,
            "status": "waiting",
        }
        # Queue the request without changing the order.
        self.requests.append(request)
        # Confirm the request is queued and still needs staff approval.
        return f"Request {number} was sent to staff. The address has not changed yet."

    # List requests that still need a decision.
    def waiting(self):
        # Describe this class or method for callers.
        """Return the requests that are still waiting for a decision."""
        # Collect the requests that still need a staff decision.
        result = []
        # Check the stored requests one at a time.
        for request in self.requests:
            # Include only requests that staff have not decided yet.
            if request["status"] == "waiting":
                # Add this waiting request to the review list.
                result.append(request)
        # Return the waiting requests for staff review.
        return result

    # Find a request by the number shown to staff.
    def find(self, number):
        # Describe this class or method for callers.
        """Return the request with this number, or None."""
        # Check the stored requests one at a time.
        for request in self.requests:
            # Match the number staff entered.
            if request["number"] == number:
                # Return the matching request.
                return request
        # Signal that no result is available.
        return None

    # Apply this request once after staff approval.
    def approve(self, number):
        # Describe this class or method for callers.
        """Approve one waiting request and make the change."""
        # Find the request staff want to approve or reject.
        request = self.find(number)
        # Refuse a request number that is not in the queue.
        if request is None:
            # Explain that the request number was not found.
            return f"There is no request {number}."
        # Prevent a second decision on an approved or rejected request.
        if request["status"] != "waiting":
            # Explain that staff have already decided this request.
            return f"Request {number} is already {request['status']}."
        # Mark this request approved so it cannot be applied twice.
        request["status"] = "approved"
        # Apply the approved address through the order tool.
        self.order_tool.change_address(request["order_id"], request["new_address"])
        # Confirm the approval.
        return f"Request {number} approved."

    # Reject this request without applying it.
    def reject(self, number):
        # Describe this class or method for callers.
        """Reject one waiting request. Nothing changes."""
        # Find the request staff want to approve or reject.
        request = self.find(number)
        # Refuse a request number that is not in the queue.
        if request is None:
            # Explain that the request number was not found.
            return f"There is no request {number}."
        # Prevent a second decision on an approved or rejected request.
        if request["status"] != "waiting":
            # Explain that staff have already decided this request.
            return f"Request {number} is already {request['status']}."
        # Close the request without making the proposed change.
        request["status"] = "rejected"
        # Confirm the rejection.
        return f"Request {number} rejected."
```

## toolbox.py

```python
# toolbox.py
# Author: Minh Nguyen


# Check every tool request before it runs.
class Toolbox:
    # Describe this class or method for callers.
    """Every tool request from the model comes through here and is checked."""

    # Keep the supplied data and start fresh state.
    def __init__(self, order_tool, stock_tool, change_queue):
        # Describe this class or method for callers.
        """Hold the tools the model is allowed to ask for."""
        # Keep the order tool used for lookups and approved changes.
        self.order_tool = order_tool
        # Keep the inventory tool used for stock questions.
        self.stock_tool = stock_tool
        # Keep address requests in the approval queue.
        self.change_queue = change_queue

    # Pass allowed methods to the model without calling them.
    def tool_list(self):
        # Describe this class or method for callers.
        """Return the tools the model may ask for. They are not called here."""
        # Advertise the permitted methods without calling them.
        return [
            self.order_tool.look_up_order,
            self.order_tool.check_return,
            self.stock_tool.check_stock,
            self.change_queue.request_address_change,
        ]

    # Check the tool name and customer arguments before running it.
    def run(self, name, arguments, history):
        # Describe this class or method for callers.
        """Check one tool request. Run the tool only if every check passes."""
        # Route order-status requests to the order lookup.
        if name == "look_up_order":
            # Clean the order ID before checking it.
            order_id = self.clean(arguments, "order_id")
            # Ask for the order ID when it is missing.
            if order_id == "":
                # Ask the customer for the required details.
                return "The order ID is missing. Ask the customer for it."
            # Refuse an order ID the customer never supplied.
            if not self.customer_said(history, order_id):
                # Ask for the missing customer detail instead of using a guessed value.
                return "The customer has not given that order ID. Ask them for it."
            # Return the checked result or the message the caller should display.
            return self.order_tool.look_up_order(order_id)
        # Apply the same order-ID checks to return questions.
        if name == "check_return":
            # Clean the order ID before checking it.
            order_id = self.clean(arguments, "order_id")
            # Ask for the order ID when it is missing.
            if order_id == "":
                # Ask the customer for the required details.
                return "The order ID is missing. Ask the customer for it."
            # Refuse an order ID the customer never supplied.
            if not self.customer_said(history, order_id):
                # Ask for the missing customer detail instead of using a guessed value.
                return "The customer has not given that order ID. Ask them for it."
            # Return the checked result or the message the caller should display.
            return self.order_tool.check_return(order_id)
        # Route stock requests to the inventory tool.
        if name == "check_stock":
            # Clean the product name before looking it up.
            item = self.clean(arguments, "item")
            # Ask which product the customer wants checked.
            if item == "":
                # Ask the customer for the required details.
                return "The product is missing. Ask the customer which product."
            # Return the checked result or the message the caller should display.
            return self.stock_tool.check_stock(item)
        # Check both customer details before queuing an address change.
        if name == "request_address_change":
            # Clean the order ID before checking it.
            order_id = self.clean(arguments, "order_id")
            # Clean the address before checking it.
            new_address = self.clean(arguments, "new_address")
            # Require both the order ID and address before proceeding.
            if order_id == "" or new_address == "":
                # Ask the customer for the required details.
                return "The order ID and the new address are both needed."
            # Refuse an order ID the customer never supplied.
            if not self.customer_said(history, order_id):
                # Ask for the missing customer detail instead of using a guessed value.
                return "The customer has not given that order ID. Ask them for it."
            # Refuse an address the customer never supplied.
            if not self.customer_said(history, new_address):
                # Ask for the missing customer detail instead of using a guessed value.
                return "The customer has not given that address. Ask them for it."
            # Return the checked result or the message the caller should display.
            return self.change_queue.request_address_change(order_id, new_address)
        # Refuse a tool that this toolbox does not expose.
        return f"There is no tool named {name}."

    # Return one argument as text without extra spaces, or "" if it is missing.
    def clean(self, arguments, key):
        # Describe this class or method for callers.
        """Return one argument as text without extra spaces, or "" if it is missing."""
        # Return the checked result or the message the caller should display.
        return str(arguments.get(key, "")).strip()

    # Return True if text appears in a message the customer typed.
    def customer_said(self, history, text):
        # Describe this class or method for callers.
        """Return True if text appears in a message the customer typed."""
        # Read the conversation in order.
        for message in history:
            # Match only customer messages, ignoring capitalization.
            if message["role"] == "user" and text.lower() in message["content"].lower():
                # Report a match.
                return True
        # Report that no match was found.
        return False
```

## keyword_model.py

```python
# keyword_model.py
# Author: Minh Nguyen


# Provide simple keyword decisions when Ollama is unavailable.
class KeywordModel:
    # Describe this class or method for callers.
    """A stand-in model that decides with keyword rules. It needs no AI."""

    # Return either reply text or a tool request.
    def decide(self, instructions, history, tools):
        # Describe this class or method for callers.
        """Return a reply or a tool request, based on the last message."""
        # Read the latest message or tool result.
        last = history[-1]
        # After a tool call, use its result as the reply.
        if last["role"] == "tool":
            # Return the checked result or the message the caller should display.
            return {"text": last["content"]}
        # Ignore capitalization when matching keywords.
        text = last["content"].lower()
        # Use the order lookup for messages containing order.
        if "order" in text:
            # Return the checked result or the message the caller should display.
            return {"tool": "look_up_order", "arguments": {"order_id": last["content"]}}
        # Use the stock tool for messages containing stock.
        if "stock" in text:
            # Return the checked result or the message the caller should display.
            return {"tool": "check_stock", "arguments": {"item": last["content"]}}
        # Recognize the fallback model's greeting.
        if "hello" in text:
            # Return the checked result or the message the caller should display.
            return {"text": "Hello! How can I help you today?"}
        # Return the checked result or the message the caller should display.
        return {
            "text": "I'm not sure how to help with that. I can check an order or stock."
        }
```

## fake_model.py

```python
# fake_model.py
# Author: Minh Nguyen


# Play back fixed decisions for repeatable tests.
class FakeModel:
    # Describe this class or method for callers.
    """A model for tests. It plays back a list of decisions, one per call."""

    # Keep the supplied data and start fresh state.
    def __init__(self, decisions):
        # Describe this class or method for callers.
        """Store the decisions to play back, in order."""
        # Keep the scripted decisions in their playback order.
        self.decisions = decisions
        # Start playback at the first decision.
        self.calls = 0

    # Return the next decision in the list.
    def decide(self, instructions, history, tools):
        # Describe this class or method for callers.
        """Return the next decision in the list."""
        # Read the decision for this test call.
        decision = self.decisions[self.calls]
        # Move to the next scripted decision.
        self.calls += 1
        # Keep the primary model's answer when it is available.
        return decision
```

## fallback_model.py

```python
# fallback_model.py
# Author: Minh Nguyen


# Use a second model only when the first is unavailable.
class FallbackModel:
    # Describe this class or method for callers.
    """Ask the first model. If it has no answer, ask the second one."""

    # Keep the supplied data and start fresh state.
    def __init__(self, first, second):
        # Describe this class or method for callers.
        """Store the two models, in the order they are asked."""
        # Try this model first.
        self.first = first
        # Use this model only when the first returns None.
        self.second = second

    # Return the first model's decision, or the second's if the first has none.
    def decide(self, instructions, history, tools):
        # Describe this class or method for callers.
        """Return the first model's decision, or the second's if the first has none."""
        # Try the primary model before considering the fallback.
        decision = self.first.decide(instructions, history, tools)
        # Handle an unavailable model without crashing the conversation.
        if decision is None:
            # Ask the fallback model because the primary model is unavailable.
            return self.second.decide(instructions, history, tools)
        # Keep the primary model's answer when it is available.
        return decision
```

## chatbot.py

```python
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
```

## ollama_model.py

```python
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
```

## my_tool.py

```python
# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.


# Define a read-only FAQ tool so business answers stay outside conversation code.
class FAQBook:
    # Describe the FAQ tool before defining its methods.
    """Find known FAQ topics and retrieve their stored answers."""

    # Read a verified print-desk FAQ answer.
    def check_faq(self, topic):
        # Describe this class or method for callers.
        """Read a verified print-desk FAQ answer.

        Args:
            topic: The topic supplied by the customer: hours, pricing, or pickup.
        """
        # Find a stored FAQ topic in the request.
        found = self.find_topic(topic)
        # Handle an unknown ID without inventing an order.
        if found is None:
            # Return the checked result or the message the caller should display.
            return "Which topic? I can check hours, pricing, or pickup."
        # Return the checked result or the message the caller should display.
        return self.answer_for(found) or "Please ask the print desk staff."

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
        # Signal that no result is available.
        return None

    # Keep retrieving an answer separate from recognizing its topic.
    def answer_for(self, topic):
        # State the missing-data behavior instead of implying every topic exists.
        """Return the stored answer, or None if no answer is available."""
        # Check the key before indexing so unknown topics do not cause KeyError.
        if topic in self.answers:
            # Return only the stored information without making up shop policies.
            return self.answers[topic]
        # Signal that no result is available.
        return None
```

## my_assistant.py

```python
"""Campus Print Desk assistant with checked tools."""

try:
    from .chatbot import SupportChatbot
except ImportError:
    from chatbot import SupportChatbot


# Use the shared conversation loop with print-desk handoff rules.
class PrintShopAssistant(SupportChatbot):
    # Describe this class or method for callers.
    """Reuse the bounded tool loop with print-shop handoff rules."""

    # Catch sensitive requests before asking the model.
    def needs_human(self, text):
        # Return the checked result or the message the caller should display.
        return any(
            word in text
            for word in ["refund", "cancel", "payment", "card", "complaint"]
        )
```

## print_queue.py

```python
"""Staff-reviewed print requests."""


# Hold proposed print jobs until staff approve them.
class PrintQueue:
    # Describe this class or method for callers.
    """Keep proposed jobs separate from approved jobs."""

    # Keep the supplied data and start fresh state.
    def __init__(self):
        # Start with no requests waiting for staff.
        self.requests = []
        # Keep accepted jobs separate from proposed jobs.
        self.jobs = []

    # Ask staff to accept a print job; nothing is printed yet.
    def request_print_job(self, document, customer):
        # Describe this class or method for callers.
        """Ask staff to accept a print job; nothing is printed yet.

        Args:
            document: The PDF filename supplied by the customer.
            customer: The customer's full name.
        """
        # Give the new request the next available number.
        number = len(self.requests) + 1
        # Save the proposed print job for staff to review.
        self.requests.append(
            {
                "number": number,
                "document": document,
                "customer": customer,
                "status": "waiting",
            }
        )
        # Confirm the request is queued and still needs staff approval.
        return f"Request {number} sent to staff. Nothing has been printed yet."

    # List undecided requests so staff can review them.
    def waiting(self):
        # Return only requests that still need staff review.
        return [r for r in self.requests if r["status"] == "waiting"]

    # Apply a waiting request once; refuse missing or completed requests.
    def approve(self, number):
        # Find the numbered request, or use None if it does not exist.
        request = next((r for r in self.requests if r["number"] == number), None)
        # Refuse a request number that is not in the queue.
        if request is None:
            # Explain that the request number was not found.
            return f"There is no request {number}."
        # Prevent a second decision on an approved or rejected request.
        if request["status"] != "waiting":
            # Explain that staff have already decided this request.
            return f"Request {number} is already {request['status']}."
        # Accept this job only after staff approval.
        self.jobs.append(
            {"document": request["document"], "customer": request["customer"]}
        )
        # Mark this request approved so it cannot be applied twice.
        request["status"] = "approved"
        # Confirm the approval.
        return f"Request {number} approved."

    # Reject a waiting request without applying its change.
    def reject(self, number):
        # Find the numbered request, or use None if it does not exist.
        request = next((r for r in self.requests if r["number"] == number), None)
        # Refuse a request number that is not in the queue.
        if request is None:
            # Explain that the request number was not found.
            return f"There is no request {number}."
        # Prevent a second decision on an approved or rejected request.
        if request["status"] != "waiting":
            # Explain that staff have already decided this request.
            return f"Request {number} is already {request['status']}."
        # Close the request without making the proposed change.
        request["status"] = "rejected"
        # Confirm the rejection.
        return f"Request {number} rejected."
```

## print_toolbox.py

```python
"""One checked entry point for Piper's tools."""


# Check Piper's tool requests and customer details.
class PrintToolbox:
    # Describe this class or method for callers.
    """Validate customer details before dispatching a tool."""

    # Keep the supplied data and start fresh state.
    def __init__(self, faq_tool, queue):
        # Use the supplied FAQ book for stored shop answers.
        self.faq_tool = faq_tool
        # Send proposed print jobs to this queue for staff review.
        self.queue = queue

    # Pass allowed methods to the model without calling them.
    def tool_list(self):
        # Return the checked result or the message the caller should display.
        return [self.faq_tool.check_faq, self.queue.request_print_job]

    # Check the tool name and customer arguments before running it.
    def run(self, name, arguments, history):
        # Handle a request for a stored FAQ answer.
        if name == "check_faq":
            # Require the FAQ topic before looking up an answer.
            keys = ["topic"]
        # Require a document and customer name for a print request.
        elif name == "request_print_job":
            # Require both the filename and customer name before queuing a job.
            keys = ["document", "customer"]
        else:
            # Refuse a tool that this toolbox does not expose.
            return f"There is no tool named {name}."
        # Collect the arguments that pass validation.
        values = {}
        # Check each required argument.
        for key in keys:
            # Treat missing values and whitespace as empty.
            value = str(arguments.get(key) or "").strip()
            # Refuse an empty argument before checking who supplied it.
            if not value:
                # Ask the customer for the required details.
                return f"The {key} is missing. Ask the customer for it."
            # Require the value to appear in a user message, not a model reply.
            if not any(
                m["role"] == "user" and value.lower() in m["content"].lower()
                for m in history
            ):
                # Ask for the missing customer detail instead of using a guessed value.
                return f"The customer has not given that {key}. Ask them for it."
            # Keep this argument after its checks pass.
            values[key] = value
        # Handle a request for a stored FAQ answer.
        if name == "check_faq":
            # Return the checked result or the message the caller should display.
            return self.faq_tool.check_faq(**values)
        # Accept only PDF filenames for this print-desk example.
        if not values["document"].lower().endswith(".pdf"):
            # Return the checked result or the message the caller should display.
            return "Please supply a PDF filename."
        # Return the checked result or the message the caller should display.
        return self.queue.request_print_job(**values)
```
