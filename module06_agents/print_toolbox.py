"""One checked entry point for Piper's tools."""


# Group this component’s state and behavior behind one interface.
class PrintToolbox:
    # Document the interface for readers and tool-description generation.
    """Validate customer details before dispatching a tool."""

    # Store the components and start fresh state for this instance.
    def __init__(self, faq_tool, queue):
        # Save faq_tool in self.faq_tool for the following steps.
        self.faq_tool = faq_tool
        # Save queue in self.queue for the following steps.
        self.queue = queue

    # Pass allowed methods to the model without calling them.
    def tool_list(self):
        # Send [self.faq_tool.check_faq, self.queue.request_print_job] back to the caller.
        return [self.faq_tool.check_faq, self.queue.request_print_job]

    # Check the tool name and customer arguments before running it.
    def run(self, name, arguments, history):
        # Check name == 'check_faq' before choosing the next action.
        if name == "check_faq":
            # Save ['topic'] in keys for the following steps.
            keys = ["topic"]
        # Check name == 'request_print_job' before choosing the next action.
        elif name == "request_print_job":
            # Save ['document', 'customer'] in keys for the following steps.
            keys = ["document", "customer"]
        else:
            # Send f'There is no tool named {name}.' back to the caller.
            return f"There is no tool named {name}."
        # Save {} in values for the following steps.
        values = {}
        # Check each key in keys.
        for key in keys:
            # Save str(arguments.get(key) or '').strip() in value for the following steps.
            value = str(arguments.get(key) or "").strip()
            # Check not value before choosing the next action.
            if not value:
                # Send f'The {key} is missing. Ask the customer for it.' back to the caller.
                return f"The {key} is missing. Ask the customer for it."
            # Check not any((m['role'] == 'user' and value.lower() in m['content'].lower() for m in history)) before choosing the next action.
            if not any(
                m["role"] == "user" and value.lower() in m["content"].lower()
                for m in history
            ):
                # Send f'The customer has not given that {key}. Ask them for it.' back to the caller.
                return f"The customer has not given that {key}. Ask them for it."
            # Save value in values[key] for the following steps.
            values[key] = value
        # Check name == 'check_faq' before choosing the next action.
        if name == "check_faq":
            # Send self.faq_tool.check_faq(**values) back to the caller.
            return self.faq_tool.check_faq(**values)
        # Check not values['document'].lower().endswith('.pdf') before choosing the next action.
        if not values["document"].lower().endswith(".pdf"):
            # Send 'Please supply a PDF filename.' back to the caller.
            return "Please supply a PDF filename."
        # Send self.queue.request_print_job(**values) back to the caller.
        return self.queue.request_print_job(**values)
