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
