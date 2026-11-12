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
