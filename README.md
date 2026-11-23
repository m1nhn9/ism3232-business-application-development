# ISM3232: Business Application Development

This repository preserves the original combined coursework and commit history.
The completed modules have now been copied into separate repositories to match
the lab folder boundaries. Use the links below for module submissions.

## Separate Module Repositories

| Weeks | Course folder | Repository | Status |
| --- | --- | --- | --- |
| 1 | `module01_setup` | No repository required by Lab 1 | File uploads |
| 2–4 | `module02_zsh` | [ism3232-module02](https://github.com/m1nhn9/ism3232-module02) | Private, as Lab 4 specifies |
| 5–6 | `module04_programming` | [ism3232-module04](https://github.com/m1nhn9/ism3232-module04) | Public, imported and tested |
| 7–8 | `module05_functions` | [ism3232-module05](https://github.com/m1nhn9/ism3232-module05) | Public, imported and tested |
| 10–12 | `module06_agents` | [ism3232-module06](https://github.com/m1nhn9/ism3232-module06) | Public, imported and tested |
| 13–16 | `module07_final_project` | [ism3232-module07](https://github.com/m1nhn9/ism3232-module07) | Empty public repository; Week 13 draft held locally for review |

Week 4 covers Git while working in `module02_zsh`; it does not create a
separate Module 3 repository. Week 9 is the midterm. The existing midterm
repository was not changed.

The standalone repositories put the module's files at the repository root.
Relevant history was extracted with original authors and messages; commit IDs
changed because their trees and parent histories changed. Each repository also
has a migration commit for its standalone imports and run instructions.
No coursework was removed from this archive.

The completed local checkouts are under `/Users/hoo/ism3232-separated/`.
The uncommitted capstone draft remains in this workspace's ignored
`module07_final_project/` folder. It has an origin remote but has not been pushed.

## Original Archive Structure

| Module | Topics | Coursework |
| --- | --- | --- |
| [Module 1](module01_setup/README.md) | Course and Python setup | Week 1 |
| [Module 2](module02_shell_navigation/README.md) | Shell navigation, environments, search, and Git | Weeks 2–4 |
| [Module 4](module04_programming/README.md) | Variables, collections, functions, tests, and debugging | Weeks 5–8 |
| [Module 6](module06_agents/README.md) | Object-oriented agents, tools, local models, and Ollama | Weeks 10–11 |

Generated caches and machine-specific files are excluded from Git. Historical
AI-use records remain beside the coursework they document.

## Run the Tests

From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ruff format --check .
ruff check .
pytest -v
```

Module 6 has additional Ollama dependencies and its own
[`requirements.txt`](module06_agents/requirements.txt).

## AI Use Statement

I used AI assistance to review course file organization, troubleshoot lint and
test issues, and implement documented lab work. I reviewed the resulting files
and verified them with Ruff and pytest. Detailed disclosures required by the
agent labs are stored in `module06_agents`.

## Course Link

[ISM3232 course materials](https://markumreed.github.io/ism3232/index.html)
