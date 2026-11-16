"""One checked entry point for Piper's tools."""


# Check Piper's tool requests and customer details.
class PrintToolbox:
    # Describe this class or method for callers.
    """Validate customer details before dispatching a tool."""

    # Keep the supplied data and start fresh state.
    def __init__(self, faq_tool, queue):
        # Use the supplied FAQ book for stored shop answers.
        self.faq_tool = faq_tool
        # Send proposed print jobs to this queue for staff review.
        self.queue = queue

    # Pass allowed methods to the model without calling them.
    def tool_list(self):
        # Return the checked result or the message the caller should display.
        return [self.faq_tool.check_faq, self.queue.request_print_job]

    # Check the tool name and customer arguments before running it.
    def run(self, name, arguments, history):
        # Handle a request for a stored FAQ answer.
        if name == "check_faq":
            # Require the FAQ topic before looking up an answer.
            keys = ["topic"]
        # Require a document and customer name for a print request.
        elif name == "request_print_job":
            # Require both the filename and customer name before queuing a job.
            keys = ["document", "customer"]
        else:
            # Refuse a tool that this toolbox does not expose.
            return f"There is no tool named {name}."
        # Collect the arguments that pass validation.
        values = {}
        # Check each required argument.
        for key in keys:
            # Treat missing values and whitespace as empty.
            value = str(arguments.get(key) or "").strip()
            # Refuse an empty argument before checking who supplied it.
            if not value:
                # Ask the customer for the required details.
                return f"The {key} is missing. Ask the customer for it."
            # Require the value to appear in a user message, not a model reply.
            if not any(
                m["role"] == "user" and value.lower() in m["content"].lower()
                for m in history
            ):
                # Ask for the missing customer detail instead of using a guessed value.
                return f"The customer has not given that {key}. Ask them for it."
            # Keep this argument after its checks pass.
            values[key] = value
        # Handle a request for a stored FAQ answer.
        if name == "check_faq":
            # Return the checked result or the message the caller should display.
            return self.faq_tool.check_faq(**values)
        # Accept only PDF filenames for this print-desk example.
        if not values["document"].lower().endswith(".pdf"):
            # Return the checked result or the message the caller should display.
            return "Please supply a PDF filename."
        # Return the checked result or the message the caller should display.
        return self.queue.request_print_job(**values)
