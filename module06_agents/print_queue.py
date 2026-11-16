"""Staff-reviewed print requests."""


# Group this component’s state and behavior behind one interface.
class PrintQueue:
    # Document the interface for readers and tool-description generation.
    """Keep proposed jobs separate from approved jobs."""

    # Store the components and start fresh state for this instance.
    def __init__(self):
        # Save [] in self.requests for the following steps.
        self.requests = []
        # Save [] in self.jobs for the following steps.
        self.jobs = []

    # Ask staff to accept a print job; nothing is printed yet.
    def request_print_job(self, document, customer):
        # Document the interface for readers and tool-description generation.
        """Ask staff to accept a print job; nothing is printed yet.

        Args:
            document: The PDF filename supplied by the customer.
            customer: The customer's full name.
        """
        # Save len(self.requests) + 1 in number for the following steps.
        number = len(self.requests) + 1
        # Run self.requests.append({'number': number, 'document': document, 'customer': customer, 'status': 'waiting'}) to record or apply this step.
        self.requests.append(
            {
                "number": number,
                "document": document,
                "customer": customer,
                "status": "waiting",
            }
        )
        # Send f'Request {number} sent to staff. Nothing has been printed yet.' back to the caller.
        return f"Request {number} sent to staff. Nothing has been printed yet."

    # List undecided requests so staff can review them.
    def waiting(self):
        # Send [r for r in self.requests if r['status'] == 'waiting'] back to the caller.
        return [r for r in self.requests if r["status"] == "waiting"]

    # Apply a waiting request once; refuse missing or completed requests.
    def approve(self, number):
        # Save next((r for r in self.requests if r['number'] == number), None) in request for the following steps.
        request = next((r for r in self.requests if r["number"] == number), None)
        # Check request is None before choosing the next action.
        if request is None:
            # Send f'There is no request {number}.' back to the caller.
            return f"There is no request {number}."
        # Check request['status'] != 'waiting' before choosing the next action.
        if request["status"] != "waiting":
            # Send f"Request {number} is already {request['status']}." back to the caller.
            return f"Request {number} is already {request['status']}."
        # Run self.jobs.append({'document': request['document'], 'customer': request['customer']}) to record or apply this step.
        self.jobs.append(
            {"document": request["document"], "customer": request["customer"]}
        )
        # Save 'approved' in request['status'] for the following steps.
        request["status"] = "approved"
        # Send f'Request {number} approved.' back to the caller.
        return f"Request {number} approved."

    # Reject a waiting request without applying its change.
    def reject(self, number):
        # Save next((r for r in self.requests if r['number'] == number), None) in request for the following steps.
        request = next((r for r in self.requests if r["number"] == number), None)
        # Check request is None before choosing the next action.
        if request is None:
            # Send f'There is no request {number}.' back to the caller.
            return f"There is no request {number}."
        # Check request['status'] != 'waiting' before choosing the next action.
        if request["status"] != "waiting":
            # Send f"Request {number} is already {request['status']}." back to the caller.
            return f"Request {number} is already {request['status']}."
        # Save 'rejected' in request['status'] for the following steps.
        request["status"] = "rejected"
        # Send f'Request {number} rejected.' back to the caller.
        return f"Request {number} rejected."
