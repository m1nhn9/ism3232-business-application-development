# Author: Minh Nguyen
# AI-assisted source; explanations accompany each class line as the lab requires.


# Define an independent stock tool so the chatbot does not own inventory data.
class StockLookup:
    # Describe the inventory tool before defining its methods.
    """Find known products and read their stock counts."""

    # Check how many of one product are in stock.
    def check_stock(self, item):
        # Describe this class or method for callers.
        """Check how many of one product are in stock.

        Args:
            item: The product name, like rain jacket.
        """
        # Find the stored product mentioned in the request.
        product = self.find_product(item)
        # Stop when the inventory has no matching product.
        if product is None:
            # Return the checked result or the message the caller should display.
            return "That product was not found."
        # Return the checked result or the message the caller should display.
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
        # Signal that no result is available.
        return None

    # Provide count lookup as a tool method instead of chatbot data access.
    def count_for(self, product):
        # Distinguish an unknown product from a known product with zero stock.
        """Return a stock count, including zero, or None if unknown."""
        # Test key membership so a zero count is still a successful lookup.
        if product in self.stock:
            # Return the actual stored count without altering inventory.
            return self.stock[product]
        # Signal that no result is available.
        return None
