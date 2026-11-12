# Author: Minh Nguyen

from my_assistant import PrintShopAssistant
from my_tool import FAQBook
from ollama_model import OllamaModel
from print_queue import PrintQueue
from print_toolbox import PrintToolbox

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are Piper, an assistant for the Campus Print Desk.
Answer in one short sentence.
The print desk is in the Student Union, room 118.
Customers should bring their order number when collecting a print job.
The desk accepts PDF files from USB drives.
If the customer only says hello, greet them and ask how you can help.
Use check_faq for hours, pricing, and pickup questions.
To request printing, ask for the PDF filename and the customer's full name.
Print requests wait for staff approval; never claim a job is printed.
Only state facts that appear in these instructions or tool results.
If you do not know, say you do not know and offer to pass the customer to print desk staff."""

ANSWERS = {
    "hours": "Campus Print Desk is open Monday-Friday, 8:00 am-6:00 pm.",
    "pricing": "Black-and-white pages cost $0.10 each; color pages cost $0.50 each.",
    "pickup": "Pick up completed jobs at the print desk with your order number.",
}


if __name__ == "__main__":
    faq_tool = FAQBook(ANSWERS)
    queue = PrintQueue()
    tools = PrintToolbox(faq_tool, queue)
    model = OllamaModel(MODEL_NAME)
    assistant = PrintShopAssistant(
        "Piper",
        INSTRUCTIONS,
        tools,
        model,
    )

    print("Type a message, or type quit to stop.")
    user_message = input("You: ")
    while user_message != "quit":
        print(f"{assistant.name}: {assistant.respond(user_message)}")
        user_message = input("You: ")

    print(f"Messages in this conversation: {len(assistant.history)}")
    print("Print desk review")
    for request in queue.waiting():
        number = request["number"]
        print(f"Request {number}: {request['customer']}, {request['document']}")
        answer = input("Approve? yes or no: ")
        print(queue.approve(number) if answer == "yes" else queue.reject(number))
    print(f"Accepted jobs: {len(queue.jobs)}")
