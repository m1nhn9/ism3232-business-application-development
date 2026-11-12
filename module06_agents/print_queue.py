"""Staff-reviewed print requests."""


# Group this component’s state and behavior behind one interface.
class PrintQueue:
    # Document the interface for readers and tool-description generation.
    """Keep proposed jobs separate from approved jobs."""

    # Define __init__ so callers can   init  .
    def __init__(self):
        # Store this value for subsequent validation or processing.
        self.requests = []
        # Store this value for subsequent validation or processing.
        self.jobs = []

    # Define request_print_job so callers can Ask staff to accept a print job; nothing is printed yet.
    def request_print_job(self, document, customer):
        # Document the interface for readers and tool-description generation.
        """Ask staff to accept a print job; nothing is printed yet.

        Args:
            document: The PDF filename supplied by the customer.
            customer: The customer's full name.
        """
        # Store this value for subsequent validation or processing.
        number = len(self.requests) + 1
        # Record or delegate this operation through the component’s interface.
        self.requests.append(
            {
                "number": number,
                "document": document,
                "customer": customer,
                "status": "waiting",
            }
        )
        # Return the result to the caller without performing terminal I/O.
        return f"Request {number} sent to staff. Nothing has been printed yet."

    # Define waiting so callers can waiting.
    def waiting(self):
        # Return the result to the caller without performing terminal I/O.
        return [r for r in self.requests if r["status"] == "waiting"]

    # Define approve so callers can approve.
    def approve(self, number):
        # Store this value for subsequent validation or processing.
        request = next((r for r in self.requests if r["number"] == number), None)
        # Check this condition before allowing the next operation.
        if request is None:
            # Return the result to the caller without performing terminal I/O.
            return f"There is no request {number}."
        # Check this condition before allowing the next operation.
        if request["status"] != "waiting":
            # Return the result to the caller without performing terminal I/O.
            return f"Request {number} is already {request['status']}."
        # Record or delegate this operation through the component’s interface.
        self.jobs.append(
            {"document": request["document"], "customer": request["customer"]}
        )
        # Store this value for subsequent validation or processing.
        request["status"] = "approved"
        # Return the result to the caller without performing terminal I/O.
        return f"Request {number} approved."

    # Define reject so callers can reject.
    def reject(self, number):
        # Store this value for subsequent validation or processing.
        request = next((r for r in self.requests if r["number"] == number), None)
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
