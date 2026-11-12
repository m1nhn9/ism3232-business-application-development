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
