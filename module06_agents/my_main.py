# Author: Minh Nguyen

from my_assistant import PrintShopAssistant
from my_tool import FAQBook

ANSWERS = {
    "hours": "Campus Print Desk is open Monday-Friday, 8:00 am-6:00 pm.",
    "pricing": "Black-and-white pages cost $0.10 each; color pages cost $0.50 each.",
    "pickup": "Pick up completed jobs at the print desk with your order number.",
}


if __name__ == "__main__":
    faq_tool = FAQBook(ANSWERS)
    assistant = PrintShopAssistant(
        "Piper",
        "Answer Campus Print Desk FAQs; send account changes to staff.",
        faq_tool,
    )

    print("Type a message, or type quit to stop.")
    user_message = input("You: ")
    while user_message != "quit":
        print(f"{assistant.name}: {assistant.respond(user_message)}")
        user_message = input("You: ")

    print(f"Messages in this conversation: {len(assistant.history)}")
