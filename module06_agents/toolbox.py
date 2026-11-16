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
