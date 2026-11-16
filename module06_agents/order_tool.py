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
