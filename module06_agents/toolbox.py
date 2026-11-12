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
