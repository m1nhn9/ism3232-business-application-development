# Week 10: OOP for Agents

## Mini-Project: Campus Print Desk

Campus Print Desk is a fictional campus print shop, and Piper answers FAQs about
its hours, pricing, and pickup process using a separate `FAQBook` tool.
The assistant stores the tool, its name, its instructions, and its own history,
recording both the user and assistant message for each turn.
All replies are mock keyword rules backed by a small dictionary, with no AI
model, API, real customer data, or actual support-ticket integration.
Refunds, cancellations, payment or card issues, and complaints go to print desk
staff because this read-only assistant cannot verify account ownership, change
orders, or resolve disputes.
With real customer data, keeping conversation histories containing student IDs
or payment details without access and retention controls could expose private
information.

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
a person, not a claim that the mock submitted a ticket or changed an account.

## Exercises and AI Assistance

- [Exercise 1](exercise1.md) labels the original class parts and notes the later
  stock-tool addition.
- Exercise 2 is `SupportChatbot.count_user_messages()` and its test.
- Exercise 3 adds `StockLookup`, `stock_reply()`, and stock tests.
- Exercise 4 is [two_bots.py](two_bots.py), with an exact-output test.

The code was generated with AI assistance, adapting the lab's support examples
and designing the print-shop FAQ mini-project. Every nonblank class source line
has an explanatory comment describing its operation and purpose, and
[ai_output.md](ai_output.md) preserves the generated class source. These
annotations support the lab's AI-use condition; they do not claim that the
student has independently written the classes or demonstrated understanding.
