# Week 12 Answers

## Exercise 1

1. The customer typed: “I want to change my shipping address”, “It's order A102”,
   and “9 Pine Street, Tampa”.
2. Two requests were refused. The first invented A100, and the second invented
   123 Main St, Anytown, AN 12345; neither detail came from the customer.
3. Ollama receives 14 messages: one system message, six user/assistant messages,
   six messages representing three tool calls and results, and the new user turn.
4. “Gift cards” contains “card”, which triggers the payment handoff rule.
   An unnecessary staff handoff costs time, while a missed payment request can
   expose sensitive details to the model.

## Exercise 2

Added check_return with an Args docstring, advertised it in tool_list, and
validated order IDs in run before dispatch. Tool and FakeModel tests cover it.
Delivered orders receive the exercise's 30-day return message; other statuses
cannot be returned yet. This is the course's simplified policy, not a check
of actual delivery dates.

## Exercise 3 — actual local-model run

For this isolated experiment, customer_said was overridden on one in-memory
toolbox to always return True, equivalent to the lab's temporary return True.
The source file kept the guardrail enabled throughout.

```text
You: I want to change my shipping address
Sunny: Your request to change the shipping address for order A100 has been submitted and is awaiting staff approval.
Tool: request_address_change
Arguments: A100, 123 Main St, Anytown, AN 12345
Result: Request 1 was sent to staff. The address has not changed yet.
Staff review: no
Request 1 rejected.
A100 14 Bay Road
A101 3 Gull Lane
A102 88 Pier Street
```

The model fabricated both details when checks were disabled. Approval remained
a second barrier: rejecting the request left every address unchanged.

## Exercise 4

FallbackModel asks its first model for a decision and asks its second only if
the first returns None. The silent-model plus KeywordModel test verifies order
lookups remain available without Ollama. Keyword matching still misses wording
such as “Has my package A101 shipped?”; it is a limited fallback.
