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


# Group this component’s state and behavior behind one interface.
class OrderLookup:
    # Document the interface for readers and tool-description generation.
    """A tool that knows about orders. It knows nothing about chatting."""

    # Store the components and start fresh state for this instance.
    def __init__(self, orders):
        # Document the interface for readers and tool-description generation.
        """Store the orders this tool can look up."""
        # Save orders in self.orders for the following steps.
        self.orders = orders

    # Return the first known order ID mentioned in text, or None.
    def find_order_id(self, text):
        # Document the interface for readers and tool-description generation.
        """Return the first known order ID mentioned in text, or None."""
        # Check each order_id in self.orders.
        for order_id in self.orders:
            # Check order_id in text.upper() before choosing the next action.
            if order_id in text.upper():
                # Send order_id back to the caller.
                return order_id
        # Send None back to the caller.
        return None

    # Return the status of one order, or None if there is no such order.
    def find_status(self, order_id):
        # Document the interface for readers and tool-description generation.
        """Return the status of one order, or None if there is no such order."""
        # Check order_id in self.orders before choosing the next action.
        if order_id in self.orders:
            # Send self.orders[order_id]['status'] back to the caller.
            return self.orders[order_id]["status"]
        # Send None back to the caller.
        return None

    # Look up the status of one order.
    def look_up_order(self, order_id):
        # Document the interface for readers and tool-description generation.
        """Look up the status of one order.

        Args:
            order_id: The order ID, like A100.
        """
        # Save self.find_order_id(order_id) in found for the following steps.
        found = self.find_order_id(order_id)
        # Check found is None before choosing the next action.
        if found is None:
            # Send 'No order with that ID was found. Order IDs look like A100.' back to the caller.
            return "No order with that ID was found. Order IDs look like A100."
        # Send f'Order {found} is {self.find_status(found)}.' back to the caller.
        return f"Order {found} is {self.find_status(found)}."

    # Change the shipping address on one order. Only an approval calls this.
    def change_address(self, order_id, new_address):
        # Document the interface for readers and tool-description generation.
        """Change the shipping address on one order. Only an approval calls this."""
        # Save new_address in self.orders[order_id]['address'] for the following steps.
        self.orders[order_id]["address"] = new_address

    # Say whether one order can be returned yet.
    def check_return(self, order_id):
        # Document the interface for readers and tool-description generation.
        """Say whether one order can be returned yet.

        Args:
            order_id: The order ID, like A100.
        """
        # Save self.find_order_id(order_id) in found for the following steps.
        found = self.find_order_id(order_id)
        # Check found is None before choosing the next action.
        if found is None:
            # Send 'No order with that ID was found. Order IDs look like A100.' back to the caller.
            return "No order with that ID was found. Order IDs look like A100."
        # Check self.find_status(found) == 'delivered' before choosing the next action.
        if self.find_status(found) == "delivered":
            # Send f'Order {found} was delivered, so it can be returned within 30 days.' back to the caller.
            return f"Order {found} was delivered, so it can be returned within 30 days."
        # Send f'Order {found} has not been delivered, so it cannot be returned yet.' back to the caller.
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

    # Define check_stock so callers can Check how many of one product are in stock.
    def check_stock(self, item):
        # Document the interface for readers and tool-description generation.
        """Check how many of one product are in stock.

        Args:
            item: The product name, like rain jacket.
        """
        # Store this value for subsequent validation or processing.
        product = self.find_product(item)
        # Check this condition before allowing the next operation.
        if product is None:
            # Return the result to the caller without performing terminal I/O.
            return "That product was not found."
        # Return the result to the caller without performing terminal I/O.
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

## change_queue.py

```python
# change_queue.py
# Author: Minh Nguyen


# Group this component’s state and behavior behind one interface.
class ChangeQueue:
    # Document the interface for readers and tool-description generation.
    """Changes waiting for a person to approve. Nothing changes until they do."""

    # Define __init__ so callers can Start with no requests. Approved changes go through the order tool.
    def __init__(self, order_tool):
        # Document the interface for readers and tool-description generation.
        """Start with no requests. Approved changes go through the order tool."""
        # Store this value for subsequent validation or processing.
        self.order_tool = order_tool
        # Store this value for subsequent validation or processing.
        self.requests = []

    # Define request_address_change so callers can Ask staff to change the shipping address on one order. Staff must approve it.
    def request_address_change(self, order_id, new_address):
        # Document the interface for readers and tool-description generation.
        """Ask staff to change the shipping address on one order. Staff must approve it.

        Args:
            order_id: The order ID, like A100.
            new_address: The full new shipping address.
        """
        # Store this value for subsequent validation or processing.
        order_id = order_id.upper()
        # Check this condition before allowing the next operation.
        if self.order_tool.find_status(order_id) is None:
            # Return the result to the caller without performing terminal I/O.
            return "No order with that ID was found. Order IDs look like A100."
        # Store this value for subsequent validation or processing.
        number = len(self.requests) + 1
        # Store this value for subsequent validation or processing.
        request = {
            "number": number,
            "order_id": order_id,
            "new_address": new_address,
            "status": "waiting",
        }
        # Record or delegate this operation through the component’s interface.
        self.requests.append(request)
        # Return the result to the caller without performing terminal I/O.
        return f"Request {number} was sent to staff. The address has not changed yet."

    # Define waiting so callers can Return the requests that are still waiting for a decision.
    def waiting(self):
        # Document the interface for readers and tool-description generation.
        """Return the requests that are still waiting for a decision."""
        # Store this value for subsequent validation or processing.
        result = []
        # Process the collection or bounded loop in a controlled order.
        for request in self.requests:
            # Check this condition before allowing the next operation.
            if request["status"] == "waiting":
                # Record or delegate this operation through the component’s interface.
                result.append(request)
        # Return the result to the caller without performing terminal I/O.
        return result

    # Define find so callers can Return the request with this number, or None.
    def find(self, number):
        # Document the interface for readers and tool-description generation.
        """Return the request with this number, or None."""
        # Process the collection or bounded loop in a controlled order.
        for request in self.requests:
            # Check this condition before allowing the next operation.
            if request["number"] == number:
                # Return the result to the caller without performing terminal I/O.
                return request
        # Return the result to the caller without performing terminal I/O.
        return None

    # Define approve so callers can Approve one waiting request and make the change.
    def approve(self, number):
        # Document the interface for readers and tool-description generation.
        """Approve one waiting request and make the change."""
        # Store this value for subsequent validation or processing.
        request = self.find(number)
        # Check this condition before allowing the next operation.
        if request is None:
            # Return the result to the caller without performing terminal I/O.
            return f"There is no request {number}."
        # Check this condition before allowing the next operation.
        if request["status"] != "waiting":
            # Return the result to the caller without performing terminal I/O.
            return f"Request {number} is already {request['status']}."
        # Store this value for subsequent validation or processing.
        request["status"] = "approved"
        # Record or delegate this operation through the component’s interface.
        self.order_tool.change_address(request["order_id"], request["new_address"])
        # Return the result to the caller without performing terminal I/O.
        return f"Request {number} approved."

    # Define reject so callers can Reject one waiting request. Nothing changes.
    def reject(self, number):
        # Document the interface for readers and tool-description generation.
        """Reject one waiting request. Nothing changes."""
        # Store this value for subsequent validation or processing.
        request = self.find(number)
        # Check this condition before allowing the next operation.
        if request is None:
            # Return the result to the caller without performing terminal I/O.
            return f"There is no request {number}."
        # Check this condition before allowing the next operation.
        if request["status"] != "waiting":
            # Return the result to the caller without performing terminal I/O.
            return f"Request {number} is already {request['status']}."
        # Store this value for subsequent validation or processing.
        request["status"] = "rejected"
        # Return the result to the caller without performing terminal I/O.
        return f"Request {number} rejected."
```

## toolbox.py

```python
# toolbox.py
# Author: Minh Nguyen


# Group this component’s state and behavior behind one interface.
class Toolbox:
    # Document the interface for readers and tool-description generation.
    """Every tool request from the model comes through here and is checked."""

    # Store the components and start fresh state for this instance.
    def __init__(self, order_tool, stock_tool, change_queue):
        # Document the interface for readers and tool-description generation.
        """Hold the tools the model is allowed to ask for."""
        # Save order_tool in self.order_tool for the following steps.
        self.order_tool = order_tool
        # Save stock_tool in self.stock_tool for the following steps.
        self.stock_tool = stock_tool
        # Save change_queue in self.change_queue for the following steps.
        self.change_queue = change_queue

    # Pass allowed methods to the model without calling them.
    def tool_list(self):
        # Document the interface for readers and tool-description generation.
        """Return the tools the model may ask for. They are not called here."""
        # Send [self.order_tool.look_up_order, self.order_tool.check_return, self.stock_tool.check_stock, self.change_queue.request_address_change] back to the caller.
        return [
            self.order_tool.look_up_order,
            self.order_tool.check_return,
            self.stock_tool.check_stock,
            self.change_queue.request_address_change,
        ]

    # Check the tool name and customer arguments before running it.
    def run(self, name, arguments, history):
        # Document the interface for readers and tool-description generation.
        """Check one tool request. Run the tool only if every check passes."""
        # Check name == 'look_up_order' before choosing the next action.
        if name == "look_up_order":
            # Save self.clean(arguments, 'order_id') in order_id for the following steps.
            order_id = self.clean(arguments, "order_id")
            # Check order_id == '' before choosing the next action.
            if order_id == "":
                # Send 'The order ID is missing. Ask the customer for it.' back to the caller.
                return "The order ID is missing. Ask the customer for it."
            # Check not self.customer_said(history, order_id) before choosing the next action.
            if not self.customer_said(history, order_id):
                # Send 'The customer has not given that order ID. Ask them for it.' back to the caller.
                return "The customer has not given that order ID. Ask them for it."
            # Send self.order_tool.look_up_order(order_id) back to the caller.
            return self.order_tool.look_up_order(order_id)
        # Check name == 'check_return' before choosing the next action.
        if name == "check_return":
            # Save self.clean(arguments, 'order_id') in order_id for the following steps.
            order_id = self.clean(arguments, "order_id")
            # Check order_id == '' before choosing the next action.
            if order_id == "":
                # Send 'The order ID is missing. Ask the customer for it.' back to the caller.
                return "The order ID is missing. Ask the customer for it."
            # Check not self.customer_said(history, order_id) before choosing the next action.
            if not self.customer_said(history, order_id):
                # Send 'The customer has not given that order ID. Ask them for it.' back to the caller.
                return "The customer has not given that order ID. Ask them for it."
            # Send self.order_tool.check_return(order_id) back to the caller.
            return self.order_tool.check_return(order_id)
        # Check name == 'check_stock' before choosing the next action.
        if name == "check_stock":
            # Save self.clean(arguments, 'item') in item for the following steps.
            item = self.clean(arguments, "item")
            # Check item == '' before choosing the next action.
            if item == "":
                # Send 'The product is missing. Ask the customer which product.' back to the caller.
                return "The product is missing. Ask the customer which product."
            # Send self.stock_tool.check_stock(item) back to the caller.
            return self.stock_tool.check_stock(item)
        # Check name == 'request_address_change' before choosing the next action.
        if name == "request_address_change":
            # Save self.clean(arguments, 'order_id') in order_id for the following steps.
            order_id = self.clean(arguments, "order_id")
            # Save self.clean(arguments, 'new_address') in new_address for the following steps.
            new_address = self.clean(arguments, "new_address")
            # Check order_id == '' or new_address == '' before choosing the next action.
            if order_id == "" or new_address == "":
                # Send 'The order ID and the new address are both needed.' back to the caller.
                return "The order ID and the new address are both needed."
            # Check not self.customer_said(history, order_id) before choosing the next action.
            if not self.customer_said(history, order_id):
                # Send 'The customer has not given that order ID. Ask them for it.' back to the caller.
                return "The customer has not given that order ID. Ask them for it."
            # Check not self.customer_said(history, new_address) before choosing the next action.
            if not self.customer_said(history, new_address):
                # Send 'The customer has not given that address. Ask them for it.' back to the caller.
                return "The customer has not given that address. Ask them for it."
            # Send self.change_queue.request_address_change(order_id, new_address) back to the caller.
            return self.change_queue.request_address_change(order_id, new_address)
        # Send f'There is no tool named {name}.' back to the caller.
        return f"There is no tool named {name}."

    # Return one argument as text without extra spaces, or "" if it is missing.
    def clean(self, arguments, key):
        # Document the interface for readers and tool-description generation.
        """Return one argument as text without extra spaces, or "" if it is missing."""
        # Send str(arguments.get(key, '')).strip() back to the caller.
        return str(arguments.get(key, "")).strip()

    # Return True if text appears in a message the customer typed.
    def customer_said(self, history, text):
        # Document the interface for readers and tool-description generation.
        """Return True if text appears in a message the customer typed."""
        # Check each message in history.
        for message in history:
            # Check message['role'] == 'user' and text.lower() in message['content'].lower() before choosing the next action.
            if message["role"] == "user" and text.lower() in message["content"].lower():
                # Send True back to the caller.
                return True
        # Send False back to the caller.
        return False
```

## keyword_model.py

```python
# keyword_model.py
# Author: Minh Nguyen


# Group this component’s state and behavior behind one interface.
class KeywordModel:
    # Document the interface for readers and tool-description generation.
    """A stand-in model that decides with keyword rules. It needs no AI."""

    # Define decide so callers can Return a reply or a tool request, based on the last message.
    def decide(self, instructions, history, tools):
        # Document the interface for readers and tool-description generation.
        """Return a reply or a tool request, based on the last message."""
        # Store this value for subsequent validation or processing.
        last = history[-1]
        # Check this condition before allowing the next operation.
        if last["role"] == "tool":
            # Return the result to the caller without performing terminal I/O.
            return {"text": last["content"]}
        # Store this value for subsequent validation or processing.
        text = last["content"].lower()
        # Check this condition before allowing the next operation.
        if "order" in text:
            # Return the result to the caller without performing terminal I/O.
            return {"tool": "look_up_order", "arguments": {"order_id": last["content"]}}
        # Check this condition before allowing the next operation.
        if "stock" in text:
            # Return the result to the caller without performing terminal I/O.
            return {"tool": "check_stock", "arguments": {"item": last["content"]}}
        # Check this condition before allowing the next operation.
        if "hello" in text:
            # Return the result to the caller without performing terminal I/O.
            return {"text": "Hello! How can I help you today?"}
        # Return the result to the caller without performing terminal I/O.
        return {
            "text": "I'm not sure how to help with that. I can check an order or stock."
        }
```

## fake_model.py

```python
# fake_model.py
# Author: Minh Nguyen


# Group this component’s state and behavior behind one interface.
class FakeModel:
    # Document the interface for readers and tool-description generation.
    """A model for tests. It plays back a list of decisions, one per call."""

    # Store the components and start fresh state for this instance.
    def __init__(self, decisions):
        # Document the interface for readers and tool-description generation.
        """Store the decisions to play back, in order."""
        # Save decisions in self.decisions for the following steps.
        self.decisions = decisions
        # Save 0 in self.calls for the following steps.
        self.calls = 0

    # Return the next decision in the list.
    def decide(self, instructions, history, tools):
        # Document the interface for readers and tool-description generation.
        """Return the next decision in the list."""
        # Save self.decisions[self.calls] in decision for the following steps.
        decision = self.decisions[self.calls]
        # Count this completed step with self.calls += 1.
        self.calls += 1
        # Send decision back to the caller.
        return decision
```

## fallback_model.py

```python
# fallback_model.py
# Author: Minh Nguyen


# Group this component’s state and behavior behind one interface.
class FallbackModel:
    # Document the interface for readers and tool-description generation.
    """Ask the first model. If it has no answer, ask the second one."""

    # Store the components and start fresh state for this instance.
    def __init__(self, first, second):
        # Document the interface for readers and tool-description generation.
        """Store the two models, in the order they are asked."""
        # Save first in self.first for the following steps.
        self.first = first
        # Save second in self.second for the following steps.
        self.second = second

    # Return the first model's decision, or the second's if the first has none.
    def decide(self, instructions, history, tools):
        # Document the interface for readers and tool-description generation.
        """Return the first model's decision, or the second's if the first has none."""
        # Save self.first.decide(instructions, history, tools) in decision for the following steps.
        decision = self.first.decide(instructions, history, tools)
        # Check decision is None before choosing the next action.
        if decision is None:
            # Send self.second.decide(instructions, history, tools) back to the caller.
            return self.second.decide(instructions, history, tools)
        # Send decision back to the caller.
        return decision
```

## chatbot.py

```python
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
```

## ollama_model.py

```python
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
```

## my_tool.py

```python
# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.


# Define a read-only FAQ tool so business answers stay outside conversation code.
class FAQBook:
    # Describe the FAQ tool before defining its methods.
    """Find known FAQ topics and retrieve their stored answers."""

    # Define check_faq so callers can Read a verified print-desk FAQ answer.
    def check_faq(self, topic):
        # Document the interface for readers and tool-description generation.
        """Read a verified print-desk FAQ answer.

        Args:
            topic: The topic supplied by the customer: hours, pricing, or pickup.
        """
        # Store this value for subsequent validation or processing.
        found = self.find_topic(topic)
        # Check this condition before allowing the next operation.
        if found is None:
            # Return the result to the caller without performing terminal I/O.
            return "Which topic? I can check hours, pricing, or pickup."
        # Return the result to the caller without performing terminal I/O.
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
"""Campus Print Desk assistant with checked tools."""

try:
    from .chatbot import SupportChatbot
except ImportError:
    from chatbot import SupportChatbot


# Group this component’s state and behavior behind one interface.
class PrintShopAssistant(SupportChatbot):
    # Document the interface for readers and tool-description generation.
    """Reuse the bounded tool loop with print-shop handoff rules."""

    # Catch sensitive requests before asking the model.
    def needs_human(self, text):
        # Send any((word in text for word in ['refund', 'cancel', 'payment', 'card', 'complaint'])) back to the caller.
        return any(
            word in text
            for word in ["refund", "cancel", "payment", "card", "complaint"]
        )
```

## print_queue.py

```python
"""Staff-reviewed print requests."""


# Group this component’s state and behavior behind one interface.
class PrintQueue:
    # Document the interface for readers and tool-description generation.
    """Keep proposed jobs separate from approved jobs."""

    # Store the components and start fresh state for this instance.
    def __init__(self):
        # Save [] in self.requests for the following steps.
        self.requests = []
        # Save [] in self.jobs for the following steps.
        self.jobs = []

    # Ask staff to accept a print job; nothing is printed yet.
    def request_print_job(self, document, customer):
        # Document the interface for readers and tool-description generation.
        """Ask staff to accept a print job; nothing is printed yet.

        Args:
            document: The PDF filename supplied by the customer.
            customer: The customer's full name.
        """
        # Save len(self.requests) + 1 in number for the following steps.
        number = len(self.requests) + 1
        # Run self.requests.append({'number': number, 'document': document, 'customer': customer, 'status': 'waiting'}) to record or apply this step.
        self.requests.append(
            {
                "number": number,
                "document": document,
                "customer": customer,
                "status": "waiting",
            }
        )
        # Send f'Request {number} sent to staff. Nothing has been printed yet.' back to the caller.
        return f"Request {number} sent to staff. Nothing has been printed yet."

    # List undecided requests so staff can review them.
    def waiting(self):
        # Send [r for r in self.requests if r['status'] == 'waiting'] back to the caller.
        return [r for r in self.requests if r["status"] == "waiting"]

    # Apply a waiting request once; refuse missing or completed requests.
    def approve(self, number):
        # Save next((r for r in self.requests if r['number'] == number), None) in request for the following steps.
        request = next((r for r in self.requests if r["number"] == number), None)
        # Check request is None before choosing the next action.
        if request is None:
            # Send f'There is no request {number}.' back to the caller.
            return f"There is no request {number}."
        # Check request['status'] != 'waiting' before choosing the next action.
        if request["status"] != "waiting":
            # Send f"Request {number} is already {request['status']}." back to the caller.
            return f"Request {number} is already {request['status']}."
        # Run self.jobs.append({'document': request['document'], 'customer': request['customer']}) to record or apply this step.
        self.jobs.append(
            {"document": request["document"], "customer": request["customer"]}
        )
        # Save 'approved' in request['status'] for the following steps.
        request["status"] = "approved"
        # Send f'Request {number} approved.' back to the caller.
        return f"Request {number} approved."

    # Reject a waiting request without applying its change.
    def reject(self, number):
        # Save next((r for r in self.requests if r['number'] == number), None) in request for the following steps.
        request = next((r for r in self.requests if r["number"] == number), None)
        # Check request is None before choosing the next action.
        if request is None:
            # Send f'There is no request {number}.' back to the caller.
            return f"There is no request {number}."
        # Check request['status'] != 'waiting' before choosing the next action.
        if request["status"] != "waiting":
            # Send f"Request {number} is already {request['status']}." back to the caller.
            return f"Request {number} is already {request['status']}."
        # Save 'rejected' in request['status'] for the following steps.
        request["status"] = "rejected"
        # Send f'Request {number} rejected.' back to the caller.
        return f"Request {number} rejected."
```

## print_toolbox.py

```python
"""One checked entry point for Piper's tools."""


# Group this component’s state and behavior behind one interface.
class PrintToolbox:
    # Document the interface for readers and tool-description generation.
    """Validate customer details before dispatching a tool."""

    # Store the components and start fresh state for this instance.
    def __init__(self, faq_tool, queue):
        # Save faq_tool in self.faq_tool for the following steps.
        self.faq_tool = faq_tool
        # Save queue in self.queue for the following steps.
        self.queue = queue

    # Pass allowed methods to the model without calling them.
    def tool_list(self):
        # Send [self.faq_tool.check_faq, self.queue.request_print_job] back to the caller.
        return [self.faq_tool.check_faq, self.queue.request_print_job]

    # Check the tool name and customer arguments before running it.
    def run(self, name, arguments, history):
        # Check name == 'check_faq' before choosing the next action.
        if name == "check_faq":
            # Save ['topic'] in keys for the following steps.
            keys = ["topic"]
        # Check name == 'request_print_job' before choosing the next action.
        elif name == "request_print_job":
            # Save ['document', 'customer'] in keys for the following steps.
            keys = ["document", "customer"]
        else:
            # Send f'There is no tool named {name}.' back to the caller.
            return f"There is no tool named {name}."
        # Save {} in values for the following steps.
        values = {}
        # Check each key in keys.
        for key in keys:
            # Save str(arguments.get(key) or '').strip() in value for the following steps.
            value = str(arguments.get(key) or "").strip()
            # Check not value before choosing the next action.
            if not value:
                # Send f'The {key} is missing. Ask the customer for it.' back to the caller.
                return f"The {key} is missing. Ask the customer for it."
            # Check not any((m['role'] == 'user' and value.lower() in m['content'].lower() for m in history)) before choosing the next action.
            if not any(
                m["role"] == "user" and value.lower() in m["content"].lower()
                for m in history
            ):
                # Send f'The customer has not given that {key}. Ask them for it.' back to the caller.
                return f"The customer has not given that {key}. Ask them for it."
            # Save value in values[key] for the following steps.
            values[key] = value
        # Check name == 'check_faq' before choosing the next action.
        if name == "check_faq":
            # Send self.faq_tool.check_faq(**values) back to the caller.
            return self.faq_tool.check_faq(**values)
        # Check not values['document'].lower().endswith('.pdf') before choosing the next action.
        if not values["document"].lower().endswith(".pdf"):
            # Send 'Please supply a PDF filename.' back to the caller.
            return "Please supply a PDF filename."
        # Send self.queue.request_print_job(**values) back to the caller.
        return self.queue.request_print_job(**values)
```
