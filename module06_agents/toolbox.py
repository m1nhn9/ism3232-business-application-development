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
