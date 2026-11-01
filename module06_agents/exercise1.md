# Exercise 1

These answers describe the original two-class chatbot from Parts 2-4. The note
afterward identifies the additional attribute introduced by Exercise 3.

1. The two classes are: `OrderLookup` and `SupportChatbot`.
2. One object of each class in `main.py`: `order_tool` is an `OrderLookup` object,
   and `bot` is a `SupportChatbot` object.
3. Every original attribute of `SupportChatbot`: `name`, `instructions`,
   `order_tool`, and `history`.
4. Every method of `OrderLookup`: `__init__`, `find_order_id`, and `find_status`.
5. The line in `chatbot.py` that is the composition: `self.order_tool = order_tool`.
6. In `bot.respond("hello")`, `self` is: `bot`, the object receiving the call.

Exercise 3 adds `stock_tool` as the fifth attribute, and
`self.stock_tool = stock_tool` is another example of composition. Exercise 2 adds
the method `count_user_messages`, which reads only user-role history entries.
The two-bot example shares the tool objects while each bot retains its own
`name`, `instructions`, and `history`; this mock stores instructions but does not
use them to change its replies.
