# Week 12 AI-assisted class output

The lab templates were adapted with AI assistance for Minh Nguyen. Each statement
has an explanatory comment in the source below. The student must review and be
able to explain the code. Week 10 and 11 archives remain historical records.

## order_tool.py

```python
# order_tool.py
# Author: Minh Nguyen


# Group this component’s state and behavior behind one interface.
class OrderLookup:
    # Document the interface for readers and tool-description generation.
    """A tool that knows about orders. It knows nothing about chatting."""

    # Define __init__ so callers can Store the orders this tool can look up.
    def __init__(self, orders):
        # Document the interface for readers and tool-description generation.
        """Store the orders this tool can look up."""
        # Store this value for subsequent validation or processing.
        self.orders = orders

    # Define find_order_id so callers can Return the first known order ID mentioned in text, or None.
    def find_order_id(self, text):
        # Document the interface for readers and tool-description generation.
        """Return the first known order ID mentioned in text, or None."""
        # Process the collection or bounded loop in a controlled order.
        for order_id in self.orders:
            # Check this condition before allowing the next operation.
            if order_id in text.upper():
                # Return the result to the caller without performing terminal I/O.
                return order_id
        # Return the result to the caller without performing terminal I/O.
        return None

    # Define find_status so callers can Return the status of one order, or None if there is no such order.
    def find_status(self, order_id):
        # Document the interface for readers and tool-description generation.
        """Return the status of one order, or None if there is no such order."""
        # Check this condition before allowing the next operation.
        if order_id in self.orders:
            # Return the result to the caller without performing terminal I/O.
            return self.orders[order_id]["status"]
        # Return the result to the caller without performing terminal I/O.
        return None

    # Define look_up_order so callers can Look up the status of one order.
    def look_up_order(self, order_id):
        # Document the interface for readers and tool-description generation.
        """Look up the status of one order.

        Args:
            order_id: The order ID, like A100.
        """
        # Store this value for subsequent validation or processing.
        found = self.find_order_id(order_id)
        # Check this condition before allowing the next operation.
        if found is None:
            # Return the result to the caller without performing terminal I/O.
            return "No order with that ID was found. Order IDs look like A100."
        # Return the result to the caller without performing terminal I/O.
        return f"Order {found} is {self.find_status(found)}."

    # Define change_address so callers can Change the shipping address on one order. Only an approval calls this.
    def change_address(self, order_id, new_address):
        # Document the interface for readers and tool-description generation.
        """Change the shipping address on one order. Only an approval calls this."""
        # Store this value for subsequent validation or processing.
        self.orders[order_id]["address"] = new_address

    # Define check_return so callers can Say whether one order can be returned yet.
    def check_return(self, order_id):
        # Document the interface for readers and tool-description generation.
        """Say whether one order can be returned yet.

        Args:
            order_id: The order ID, like A100.
        """
        # Store this value for subsequent validation or processing.
        found = self.find_order_id(order_id)
        # Check this condition before allowing the next operation.
        if found is None:
            # Return the result to the caller without performing terminal I/O.
            return "No order with that ID was found. Order IDs look like A100."
        # Check this condition before allowing the next operation.
        if self.find_status(found) == "delivered":
            # Return the result to the caller without performing terminal I/O.
            return f"Order {found} was delivered, so it can be returned within 30 days."
        # Return the result to the caller without performing terminal I/O.
        return f"Order {found} has not been delivered, so it cannot be returned yet."
```

## stock_tool.py

```python
# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.


# Define an independent stock tool so the chatbot does not own inventory data.
class StockLookup:
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

    # Define __init__ so callers can Hold the tools the model is allowed to ask for.
    def __init__(self, order_tool, stock_tool, change_queue):
        # Document the interface for readers and tool-description generation.
        """Hold the tools the model is allowed to ask for."""
        # Store this value for subsequent validation or processing.
        self.order_tool = order_tool
        # Store this value for subsequent validation or processing.
        self.stock_tool = stock_tool
        # Store this value for subsequent validation or processing.
        self.change_queue = change_queue

    # Define tool_list so callers can Return the tools the model may ask for. They are not called here.
    def tool_list(self):
        # Document the interface for readers and tool-description generation.
        """Return the tools the model may ask for. They are not called here."""
        # Return the result to the caller without performing terminal I/O.
        return [
            self.order_tool.look_up_order,
            self.order_tool.check_return,
            self.stock_tool.check_stock,
            self.change_queue.request_address_change,
        ]

    # Define run so callers can Check one tool request. Run the tool only if every check passes.
    def run(self, name, arguments, history):
        # Document the interface for readers and tool-description generation.
        """Check one tool request. Run the tool only if every check passes."""
        # Check this condition before allowing the next operation.
        if name == "look_up_order":
            # Store this value for subsequent validation or processing.
            order_id = self.clean(arguments, "order_id")
            # Check this condition before allowing the next operation.
            if order_id == "":
                # Return the result to the caller without performing terminal I/O.
                return "The order ID is missing. Ask the customer for it."
            # Check this condition before allowing the next operation.
            if not self.customer_said(history, order_id):
                # Return the result to the caller without performing terminal I/O.
                return "The customer has not given that order ID. Ask them for it."
            # Return the result to the caller without performing terminal I/O.
            return self.order_tool.look_up_order(order_id)
        # Check this condition before allowing the next operation.
        if name == "check_return":
            # Store this value for subsequent validation or processing.
            order_id = self.clean(arguments, "order_id")
            # Check this condition before allowing the next operation.
            if order_id == "":
                # Return the result to the caller without performing terminal I/O.
                return "The order ID is missing. Ask the customer for it."
            # Check this condition before allowing the next operation.
            if not self.customer_said(history, order_id):
                # Return the result to the caller without performing terminal I/O.
                return "The customer has not given that order ID. Ask them for it."
            # Return the result to the caller without performing terminal I/O.
            return self.order_tool.check_return(order_id)
        # Check this condition before allowing the next operation.
        if name == "check_stock":
            # Store this value for subsequent validation or processing.
            item = self.clean(arguments, "item")
            # Check this condition before allowing the next operation.
            if item == "":
                # Return the result to the caller without performing terminal I/O.
                return "The product is missing. Ask the customer which product."
            # Return the result to the caller without performing terminal I/O.
            return self.stock_tool.check_stock(item)
        # Check this condition before allowing the next operation.
        if name == "request_address_change":
            # Store this value for subsequent validation or processing.
            order_id = self.clean(arguments, "order_id")
            # Store this value for subsequent validation or processing.
            new_address = self.clean(arguments, "new_address")
            # Check this condition before allowing the next operation.
            if order_id == "" or new_address == "":
                # Return the result to the caller without performing terminal I/O.
                return "The order ID and the new address are both needed."
            # Check this condition before allowing the next operation.
            if not self.customer_said(history, order_id):
                # Return the result to the caller without performing terminal I/O.
                return "The customer has not given that order ID. Ask them for it."
            # Check this condition before allowing the next operation.
            if not self.customer_said(history, new_address):
                # Return the result to the caller without performing terminal I/O.
                return "The customer has not given that address. Ask them for it."
            # Return the result to the caller without performing terminal I/O.
            return self.change_queue.request_address_change(order_id, new_address)
        # Return the result to the caller without performing terminal I/O.
        return f"There is no tool named {name}."

    # Define clean so callers can Return one argument as text without extra spaces, or "" if it is missing.
    def clean(self, arguments, key):
        # Document the interface for readers and tool-description generation.
        """Return one argument as text without extra spaces, or "" if it is missing."""
        # Return the result to the caller without performing terminal I/O.
        return str(arguments.get(key, "")).strip()

    # Define customer_said so callers can Return True if text appears in a message the customer typed.
    def customer_said(self, history, text):
        # Document the interface for readers and tool-description generation.
        """Return True if text appears in a message the customer typed."""
        # Process the collection or bounded loop in a controlled order.
        for message in history:
            # Check this condition before allowing the next operation.
            if message["role"] == "user" and text.lower() in message["content"].lower():
                # Return the result to the caller without performing terminal I/O.
                return True
        # Return the result to the caller without performing terminal I/O.
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

    # Define __init__ so callers can Store the decisions to play back, in order.
    def __init__(self, decisions):
        # Document the interface for readers and tool-description generation.
        """Store the decisions to play back, in order."""
        # Store this value for subsequent validation or processing.
        self.decisions = decisions
        # Store this value for subsequent validation or processing.
        self.calls = 0

    # Define decide so callers can Return the next decision in the list.
    def decide(self, instructions, history, tools):
        # Document the interface for readers and tool-description generation.
        """Return the next decision in the list."""
        # Store this value for subsequent validation or processing.
        decision = self.decisions[self.calls]
        # Advance the running count to track progress.
        self.calls += 1
        # Return the result to the caller without performing terminal I/O.
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

    # Define __init__ so callers can Store the two models, in the order they are asked.
    def __init__(self, first, second):
        # Document the interface for readers and tool-description generation.
        """Store the two models, in the order they are asked."""
        # Store this value for subsequent validation or processing.
        self.first = first
        # Store this value for subsequent validation or processing.
        self.second = second

    # Define decide so callers can Return the first model's decision, or the second's if the first has none.
    def decide(self, instructions, history, tools):
        # Document the interface for readers and tool-description generation.
        """Return the first model's decision, or the second's if the first has none."""
        # Store this value for subsequent validation or processing.
        decision = self.first.decide(instructions, history, tools)
        # Check this condition before allowing the next operation.
        if decision is None:
            # Return the result to the caller without performing terminal I/O.
            return self.second.decide(instructions, history, tools)
        # Return the result to the caller without performing terminal I/O.
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

    # Define __init__ so callers can Remember which model to ask.
    def __init__(self, model_name):
        # Document the interface for readers and tool-description generation.
        """Remember which model to ask."""
        # Store this value for subsequent validation or processing.
        self.model_name = model_name

    # Define reply so callers can Send the instructions and the conversation to the model. Return its reply.
    def reply(self, instructions, history):
        # Document the interface for readers and tool-description generation.
        """Send the instructions and the conversation to the model. Return its reply."""
        # Store this value for subsequent validation or processing.
        messages = [{"role": "system", "content": instructions}]
        # Store this value for subsequent validation or processing.
        messages = messages + history
        # Handle the expected model connection and response failures.
        try:
            # Store this value for subsequent validation or processing.
            response = chat(model=self.model_name, messages=messages)
        except ConnectionError:
            # Return the result to the caller without performing terminal I/O.
            return None
        except ResponseError:
            # Return the result to the caller without performing terminal I/O.
            return None
        # Return the result to the caller without performing terminal I/O.
        return response.message.content

    # Define decide so callers can Send the conversation and the tools. Return a reply or a tool request.
    def decide(self, instructions, history, tools):
        # Document the interface for readers and tool-description generation.
        """Send the conversation and the tools. Return a reply or a tool request."""
        # Store this value for subsequent validation or processing.
        messages = [{"role": "system", "content": instructions}]
        # Process the collection or bounded loop in a controlled order.
        for message in history:
            # Check this condition before allowing the next operation.
            if message["role"] == "tool":
                # Store this value for subsequent validation or processing.
                messages = messages + self.tool_messages(message)
            else:
                # Record or delegate this operation through the component’s interface.
                messages.append(message)
        # Handle the expected model connection and response failures.
        try:
            # Store this value for subsequent validation or processing.
            response = chat(model=self.model_name, messages=messages, tools=tools)
        except ConnectionError:
            # Return the result to the caller without performing terminal I/O.
            return None
        except ResponseError:
            # Return the result to the caller without performing terminal I/O.
            return None
        # Check this condition before allowing the next operation.
        if response.message.tool_calls:
            # Store this value for subsequent validation or processing.
            call = response.message.tool_calls[0]
            # Return the result to the caller without performing terminal I/O.
            return {"tool": call.function.name, "arguments": call.function.arguments}
        # Return the result to the caller without performing terminal I/O.
        return {"text": response.message.content}

    # Define tool_messages so callers can Turn one tool entry into the two messages Ollama expects.
    def tool_messages(self, message):
        # Document the interface for readers and tool-description generation.
        """Turn one tool entry into the two messages Ollama expects."""
        # Store this value for subsequent validation or processing.
        name = message["tool_name"]
        # Store this value for subsequent validation or processing.
        request = {"function": {"name": name, "arguments": message["arguments"]}}
        # Return the result to the caller without performing terminal I/O.
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
"""Campus Print Desk assistant with checked tools."""

try:
    from .chatbot import SupportChatbot
except ImportError:
    from chatbot import SupportChatbot


# Group this component’s state and behavior behind one interface.
class PrintShopAssistant(SupportChatbot):
    # Document the interface for readers and tool-description generation.
    """Reuse the bounded tool loop with print-shop handoff rules."""

    # Define needs_human so callers can needs human.
    def needs_human(self, text):
        # Return the result to the caller without performing terminal I/O.
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

    # Define __init__ so callers can   init  .
    def __init__(self):
        # Store this value for subsequent validation or processing.
        self.requests = []
        # Store this value for subsequent validation or processing.
        self.jobs = []

    # Define request_print_job so callers can Ask staff to accept a print job; nothing is printed yet.
    def request_print_job(self, document, customer):
        # Document the interface for readers and tool-description generation.
        """Ask staff to accept a print job; nothing is printed yet.

        Args:
            document: The PDF filename supplied by the customer.
            customer: The customer's full name.
        """
        # Store this value for subsequent validation or processing.
        number = len(self.requests) + 1
        # Record or delegate this operation through the component’s interface.
        self.requests.append(
            {
                "number": number,
                "document": document,
                "customer": customer,
                "status": "waiting",
            }
        )
        # Return the result to the caller without performing terminal I/O.
        return f"Request {number} sent to staff. Nothing has been printed yet."

    # Define waiting so callers can waiting.
    def waiting(self):
        # Return the result to the caller without performing terminal I/O.
        return [r for r in self.requests if r["status"] == "waiting"]

    # Define approve so callers can approve.
    def approve(self, number):
        # Store this value for subsequent validation or processing.
        request = next((r for r in self.requests if r["number"] == number), None)
        # Check this condition before allowing the next operation.
        if request is None:
            # Return the result to the caller without performing terminal I/O.
            return f"There is no request {number}."
        # Check this condition before allowing the next operation.
        if request["status"] != "waiting":
            # Return the result to the caller without performing terminal I/O.
            return f"Request {number} is already {request['status']}."
        # Record or delegate this operation through the component’s interface.
        self.jobs.append(
            {"document": request["document"], "customer": request["customer"]}
        )
        # Store this value for subsequent validation or processing.
        request["status"] = "approved"
        # Return the result to the caller without performing terminal I/O.
        return f"Request {number} approved."

    # Define reject so callers can reject.
    def reject(self, number):
        # Store this value for subsequent validation or processing.
        request = next((r for r in self.requests if r["number"] == number), None)
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

## print_toolbox.py

```python
"""One checked entry point for Piper's tools."""


# Group this component’s state and behavior behind one interface.
class PrintToolbox:
    # Document the interface for readers and tool-description generation.
    """Validate customer details before dispatching a tool."""

    # Define __init__ so callers can   init  .
    def __init__(self, faq_tool, queue):
        # Store this value for subsequent validation or processing.
        self.faq_tool = faq_tool
        # Store this value for subsequent validation or processing.
        self.queue = queue

    # Define tool_list so callers can tool list.
    def tool_list(self):
        # Return the result to the caller without performing terminal I/O.
        return [self.faq_tool.check_faq, self.queue.request_print_job]

    # Define run so callers can run.
    def run(self, name, arguments, history):
        # Check this condition before allowing the next operation.
        if name == "check_faq":
            # Store this value for subsequent validation or processing.
            keys = ["topic"]
        # Check this condition before allowing the next operation.
        elif name == "request_print_job":
            # Store this value for subsequent validation or processing.
            keys = ["document", "customer"]
        else:
            # Return the result to the caller without performing terminal I/O.
            return f"There is no tool named {name}."
        # Store this value for subsequent validation or processing.
        values = {}
        # Process the collection or bounded loop in a controlled order.
        for key in keys:
            # Store this value for subsequent validation or processing.
            value = str(arguments.get(key) or "").strip()
            # Check this condition before allowing the next operation.
            if not value:
                # Return the result to the caller without performing terminal I/O.
                return f"The {key} is missing. Ask the customer for it."
            # Check this condition before allowing the next operation.
            if not any(
                m["role"] == "user" and value.lower() in m["content"].lower()
                for m in history
            ):
                # Return the result to the caller without performing terminal I/O.
                return f"The customer has not given that {key}. Ask them for it."
            # Store this value for subsequent validation or processing.
            values[key] = value
        # Check this condition before allowing the next operation.
        if name == "check_faq":
            # Return the result to the caller without performing terminal I/O.
            return self.faq_tool.check_faq(**values)
        # Check this condition before allowing the next operation.
        if not values["document"].lower().endswith(".pdf"):
            # Return the result to the caller without performing terminal I/O.
            return "Please supply a PDF filename."
        # Return the result to the caller without performing terminal I/O.
        return self.queue.request_print_job(**values)
```
