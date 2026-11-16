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
