# Module 6: Building AI Agents

## Mini-Project: Campus Print Desk

Campus Print Desk is a fictional campus print shop, and Piper answers FAQs about
its hours, pricing, and pickup process using a separate `FAQBook` tool.
The assistant stores the tool, model, name, instructions, and its own history,
recording both the user and assistant message for each turn.
Verified FAQ replies use a small dictionary, and other language questions go
to the local `granite4.1:3b` model through Ollama.
Refunds, cancellations, payment or card issues, and complaints go to print desk
staff because this read-only assistant cannot verify account ownership, change
orders, or resolve disputes.
With real customer data, keeping conversation histories containing student IDs
or payment details without access and retention controls could expose private
information.

## Week 11 Model Review

The model answered “Where is the print desk?” correctly from its instructions:
the Student Union, room 118. It also correctly said to bring an order number
when collecting a print job. When asked whether the desk prints posters, it
said it did not know and offered to send the customer to staff instead of
inventing a service. Hours, pricing, and pickup answers stay in the `FAQBook`
because those facts must be exact. Refunds, cancellations, payments, cards,
and complaints stay in code as staff handoffs because a model must not approve
or claim to perform those actions.

## Run

From this directory:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
python3 two_bots.py
python3 my_main.py
ruff format . && ruff check . && pytest -v
```

Both interactive programs stop when the user types `quit`; the command itself
is not added to conversation history. Staff handoffs are directions to contact
a person, not a claim that the assistant submitted a ticket or changed an account.

## Exercises

- [Exercise 1](exercise1.md) labels the original class parts and notes the later
  stock-tool addition.
- Exercise 2 is `SupportChatbot.count_user_messages()` and its test.
- Exercise 3 adds `StockLookup`, `stock_reply()`, and stock tests.
- Exercise 4 is [two_bots.py](two_bots.py), with an exact-output test.
- [Week 11 answers](week11_answers.md) records the message-history analysis,
  real-model transcripts, and model-risk reflection.

## Class Documentation

Every nonblank class source line has a comment explaining its operation and
purpose. The Week 10 [annotated class output](ai_output.md) and Week 11
[annotated model output](week11_ai_output.md) are archived separately to
document the generated class code required by both labs.
