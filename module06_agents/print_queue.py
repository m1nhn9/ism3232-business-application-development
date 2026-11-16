"""Staff-reviewed print requests."""


# Hold proposed print jobs until staff approve them.
class PrintQueue:
    # Describe this class or method for callers.
    """Keep proposed jobs separate from approved jobs."""

    # Keep the supplied data and start fresh state.
    def __init__(self):
        # Start with no requests waiting for staff.
        self.requests = []
        # Keep accepted jobs separate from proposed jobs.
        self.jobs = []

    # Ask staff to accept a print job; nothing is printed yet.
    def request_print_job(self, document, customer):
        # Describe this class or method for callers.
        """Ask staff to accept a print job; nothing is printed yet.

        Args:
            document: The PDF filename supplied by the customer.
            customer: The customer's full name.
        """
        # Give the new request the next available number.
        number = len(self.requests) + 1
        # Save the proposed print job for staff to review.
        self.requests.append(
            {
                "number": number,
                "document": document,
                "customer": customer,
                "status": "waiting",
            }
        )
        # Confirm the request is queued and still needs staff approval.
        return f"Request {number} sent to staff. Nothing has been printed yet."

    # List undecided requests so staff can review them.
    def waiting(self):
        # Return only requests that still need staff review.
        return [r for r in self.requests if r["status"] == "waiting"]

    # Apply a waiting request once; refuse missing or completed requests.
    def approve(self, number):
        # Find the numbered request, or use None if it does not exist.
        request = next((r for r in self.requests if r["number"] == number), None)
        # Refuse a request number that is not in the queue.
        if request is None:
            # Explain that the request number was not found.
            return f"There is no request {number}."
        # Prevent a second decision on an approved or rejected request.
        if request["status"] != "waiting":
            # Explain that staff have already decided this request.
            return f"Request {number} is already {request['status']}."
        # Accept this job only after staff approval.
        self.jobs.append(
            {"document": request["document"], "customer": request["customer"]}
        )
        # Mark this request approved so it cannot be applied twice.
        request["status"] = "approved"
        # Confirm the approval.
        return f"Request {number} approved."

    # Reject a waiting request without applying its change.
    def reject(self, number):
        # Find the numbered request, or use None if it does not exist.
        request = next((r for r in self.requests if r["number"] == number), None)
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
