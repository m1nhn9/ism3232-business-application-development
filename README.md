# ISM3232: Business Application Development

Coursework is organized by the course modules used throughout ISM3232. Each
module keeps its source, exercises, documentation, tests, and local dependency
information together.

## Repository Structure

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
