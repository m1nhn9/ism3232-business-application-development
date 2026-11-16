# Module 6: Building AI Agents

## Mini-Project: Campus Print Desk

Campus Print Desk is a fictional campus print shop, and Piper answers FAQs about
its hours, pricing, and pickup process using a separate `FAQBook` tool.
The assistant stores the tool, model, name, instructions, and its own history,
recording both the user and assistant message for each turn.
The local `granite4.1:3b` model chooses tools, and the toolbox checks each
request before reading a verified FAQ or queuing a print job for staff approval.
Refunds, cancellations, payment or card issues, and complaints go to print desk
staff because this assistant cannot verify account ownership, change
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

## Week 12 Tools and Approval

Piper handled “Please print essay.pdf for Dana Cruz” by filing a waiting request,
and the real-model run accepted one job only after staff approved it.
The toolbox refused a FakeModel request naming Dana Cruz when the customer
had supplied only essay.pdf, leaving the queue empty.
I added instructions to ask for the PDF filename and full name before requesting
printing and to explain that printing still needs staff approval.
The greeting instruction tells the model to greet rather than invoke a tool.
Refunds, cancellations, payment questions, and complaints still go to a person
before the model is called.

Sunny and Piper share a loop that stops after three tool rounds. Each has its
own toolbox and handoff rules. Requests and accepted jobs are stored in memory
and reset when the program exits. Staff review starts after the customer types
`quit`. Week 12 uses `decide` and records tool results in the conversation history.

See [Week 12 answers](week12_answers.md) and the
[annotated class archive](week12_ai_output.md).

## Running the Programs

Install and start Ollama, then run `ollama pull granite4.1:3b` for the real-model
conversations. Sunny uses KeywordModel when Ollama is unavailable, as required
by Exercise 4. Piper returns a safe retry message when its model is unavailable.

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

## Week 10 Exercises (Historical)

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

The Week 12 code and comments are saved in
[week12_ai_output.md](week12_ai_output.md). I used AI assistance for the code,
comments, answers, and README. The model results came from actual runs. I still
need to review the explanations and be able to explain each class line myself.
