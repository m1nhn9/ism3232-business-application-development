# change_queue.py
# Author: Minh Nguyen


# Hold proposed address changes until staff decide.
class ChangeQueue:
    # Describe this class or method for callers.
    """Changes waiting for a person to approve. Nothing changes until they do."""

    # Keep the supplied data and start fresh state.
    def __init__(self, order_tool):
        # Describe this class or method for callers.
        """Start with no requests. Approved changes go through the order tool."""
        # Keep the order tool used for lookups and approved changes.
        self.order_tool = order_tool
        # Start with no requests waiting for staff.
        self.requests = []

    # Ask staff to change the shipping address on one order. Staff must approve it.
    def request_address_change(self, order_id, new_address):
        # Describe this class or method for callers.
        """Ask staff to change the shipping address on one order. Staff must approve it.

        Args:
            order_id: The order ID, like A100.
            new_address: The full new shipping address.
        """
        # Match lowercase IDs to the uppercase order keys.
        order_id = order_id.upper()
        # Require an exact order key so A1000 cannot change A100.
        if self.order_tool.find_status(order_id) is None:
            # Ask for a valid order ID.
            return "No order with that ID was found. Order IDs look like A100."
        # Give the new request the next available number.
        number = len(self.requests) + 1
        # Save the proposed change with a waiting status.
        request = {
            "number": number,
            "order_id": order_id,
            "new_address": new_address,
            "status": "waiting",
        }
        # Queue the request without changing the order.
        self.requests.append(request)
        # Confirm the request is queued and still needs staff approval.
        return f"Request {number} was sent to staff. The address has not changed yet."

    # List requests that still need a decision.
    def waiting(self):
        # Describe this class or method for callers.
        """Return the requests that are still waiting for a decision."""
        # Collect the requests that still need a staff decision.
        result = []
        # Check the stored requests one at a time.
        for request in self.requests:
            # Include only requests that staff have not decided yet.
            if request["status"] == "waiting":
                # Add this waiting request to the review list.
                result.append(request)
        # Return the waiting requests for staff review.
        return result

    # Find a request by the number shown to staff.
    def find(self, number):
        # Describe this class or method for callers.
        """Return the request with this number, or None."""
        # Check the stored requests one at a time.
        for request in self.requests:
            # Match the number staff entered.
            if request["number"] == number:
                # Return the matching request.
                return request
        # Signal that no result is available.
        return None

    # Apply this request once after staff approval.
    def approve(self, number):
        # Describe this class or method for callers.
        """Approve one waiting request and make the change."""
        # Find the request staff want to approve or reject.
        request = self.find(number)
        # Refuse a request number that is not in the queue.
        if request is None:
            # Explain that the request number was not found.
            return f"There is no request {number}."
        # Prevent a second decision on an approved or rejected request.
        if request["status"] != "waiting":
            # Explain that staff have already decided this request.
            return f"Request {number} is already {request['status']}."
        # Mark this request approved so it cannot be applied twice.
        request["status"] = "approved"
        # Apply the approved address through the order tool.
        self.order_tool.change_address(request["order_id"], request["new_address"])
        # Confirm the approval.
        return f"Request {number} approved."

    # Reject this request without applying it.
    def reject(self, number):
        # Describe this class or method for callers.
        """Reject one waiting request. Nothing changes."""
        # Find the request staff want to approve or reject.
        request = self.find(number)
        # Refuse a request number that is not in the queue.
        if request is None:
            # Explain that the request number was not found.
            return f"There is no request {number}."
        # Prevent a second decision on an approved or rejected request.
        if request["status"] != "waiting":
            # Explain that staff have already decided this request.
            return f"Request {number} is already {request['status']}."
        # Close the request without making the proposed change.
        request["status"] = "rejected"
        # Confirm the rejection.
        return f"Request {number} rejected."
