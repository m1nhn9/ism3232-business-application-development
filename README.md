# ISM3232 - Module 2: zsh Navigation and File Operations

## Week 2: Commands

| Command | Description |
| --- | --- |
| `pwd` | Print the current working directory. |
| `ls` | List visible files and folders. |
| `ls -la` | List files, including hidden files and details. |
| `cd ..` | Move to the parent directory. |
| `cd ~/ism3232` | Move to the course directory. |
| `tree -L 2` | Display the directory tree to two levels. |
| `touch FILE` | Create an empty file or update its timestamp. |
| `echo TEXT > FILE` | Write text to a file. |
| `cat FILE` | Print a file's contents. |
| `head -1 FILE` | Print the first line of a file. |
| `cp SOURCE DEST` | Copy a file. |
| `mv SOURCE DEST` | Move or rename a file. |
| `python3 FILE` | Run a Python script. |
| `rm FILE` | Delete a file after checking location and contents. |

## Week 3: Virtual Environments and .zshrc

| Command or alias | Description |
| --- | --- |
| `python3 -m venv .venv` | Create a project virtual environment. |
| `source .venv/bin/activate` | Activate the environment. |
| `which python3` | Show the active Python interpreter. |
| `pip install pytest ruff` | Install the lab tools. |
| `pip freeze > requirements.txt` | Record installed package versions. |
| `deactivate` | Leave the active virtual environment. |
| `ll` | Run `ls -la`. |
| `c` | Clear the terminal. |
| `py` | Run `python3`. |
| `gs` | Run `git status`. |
| `ga` | Run `git add .`. |
| `gcmsg MESSAGE` | Run `git commit -m MESSAGE`. |
| `gp` | Run `git push`. |
| `gl` | Run `git log --oneline`. |
| `tree2` | Run `tree -L 2`. |
| `mkcd NAME` | Create a directory and enter it. |

## AI Use Statement
I used AI assistance to review course file organization and troubleshoot lint and test issues. I reviewed the resulting files and ran Ruff and pytest.

## Additional Links
- [ISM3232](https://markumreed.github.io/ism3232/index.html)

## Week 10: OOP for Agents

The chatbot, four exercises, and Campus Print Desk FAQ mini-project are in
[module06_agents](module06_agents/README.md). That directory includes run
instructions, tests, exercise answers, and the mini-project documentation.
