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
