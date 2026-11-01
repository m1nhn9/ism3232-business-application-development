import subprocess
import sys
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1]


def run_cli(script, messages=""):
    return subprocess.run(
        [sys.executable, str(MODULE / script)],
        input=messages,
        text=True,
        capture_output=True,
        check=True,
        cwd=MODULE,
    ).stdout


def test_support_conversation_matches_the_lab():
    output = run_cli(
        "main.py",
        "hello\nWhere is order A100?\nwhere is my order\n"
        "Please change my shipping address\nWhat is the weather?\nquit\n",
    )
    assert output == (
        "Type a message, or type quit to stop.\n"
        "You: Sunny: Hello! I'm Sunny. I can check an order status for you.\n"
        "You: Sunny: Order A100 is shipped.\n"
        "You: Sunny: Which order? Please send an order ID like A100.\n"
        "You: Sunny: I can't help with that here. I'm passing you to a human agent.\n"
        "You: Sunny: I'm not sure how to help with that. I can check an order status.\n"
        "You: Messages in this conversation: 10\n"
    )


def test_stock_conversation_matches_the_exercise():
    output = run_cli(
        "main.py",
        "Is the rain jacket in stock?\nDo you have it in stock?\nquit\n",
    )
    assert "We have 12 of the rain jacket in stock." in output
    assert "Which product? Please name the item you want me to check." in output
    assert output.endswith("Messages in this conversation: 4\n")


def test_two_bots_output_matches_the_exercise():
    assert run_cli("two_bots.py") == (
        "Sunny 4\nRiver 2\n"
        "Hello! I'm Sunny. I can check an order status for you.\n"
        "Hello! I'm River. I can check an order status for you.\n"
        "You are cheerful and brief.\n"
        "You are formal and detailed.\n"
    )


def test_print_shop_cli_records_all_turns_and_quits():
    output = run_cli(
        "my_main.py",
        "hello\nWhat are your hours?\nFAQ: delivery?\n"
        "Cancel my order\nWhat is the weather?\nquit\n",
    )
    assert "Hello! I'm Piper." in output
    assert "open Monday-Friday, 8:00 am-6:00 pm." in output
    assert "Which topic?" in output
    assert "print desk staff" in output
    assert "not sure" in output
    assert output.endswith("Messages in this conversation: 10\n")
