# Setup: Google ADK Agent (`my_agent`)

## Prerequisites

- Python **3.10+** 
- A Gemini API key (free, from [Google AI Studio](https://aistudio.google.com/))

## 1. Install Python

The default `python3` on this Mac was too old for ADK. Installed a newer one via Homebrew:

```bash
brew install python@3.12
```

## 2. Create the virtualenv and install ADK

```bash
rm -rf .venv                      
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```


## 3. Scaffold the agent

```bash
adk create my_agent
```

Prompts answered:

| Prompt | Choice | Why |
|---|---|---|
| Choose model | `1` — `gemini-2.5-flash` | Fast, cheap, plenty capable for a demo agent with a simple tool |
| Choose a backend | `1` — Google AI | Uses the free AI Studio API key; Vertex AI (`2`) needs a GCP project + billing, Login with Google (`3`) is only for Vertex's OAuth flow |

This scaffolds:

```
my_agent/
  agent.py      # root_agent definition — model, instruction, tools
  .env          # API key
  __init__.py
```

## 4. Add the API key

```bash
echo 'GOOGLE_API_KEY="YOUR_KEY"' > my_agent/.env
```

Key generated from Google AI Studio.

## 5. Add a tool

`agent.py` is where the agent's anatomy lives — a `root_agent = Agent(model=..., instruction=..., tools=[...])` object. A tool is just a plain Python function; ADK infers the schema from the function signature and docstring, no manual schema needed.

Wired up a tool that calls a mock API ([Beeceptor](https://beeceptor.com/) fake JSON endpoint):

```python
import requests
from google.adk.agents.llm_agent import Agent

MOCK_API_BASE_URL = "https://fake-json-api.mock.beeceptor.com/users"


def get_user_data() -> dict:
    try:
        response = requests.get(f"{MOCK_API_BASE_URL}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}


root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge. Use the get_user_data tool to retrieve user data.',
    tools=[get_user_data],
)
```

Key points:
- The tool function's docstring/type hints double as the schema the model sees — worth keeping them descriptive.
- Return JSON-serializable data (dict/list/str/etc.) — that's what gets fed back to the model as the tool result.
- Catch request errors inside the tool and return an `{"error": ...}` dict instead of letting an exception crash the turn.

## 6. Run it

From the repo root (`atd-2026/`, the parent dir of `my_agent/`):

```bash
adk run my_agent          # quick CLI chat — type a message at [user]:, `exit` to quit
```

or, for the web UI with trace/JSON inspection:

```bash
adk web --port 8000
```

Then open `http://localhost:8000`, select `my_agent` top-left, and chat with it. Click into a turn's trace/events to see the actual system instruction, tool call, and tool response as JSON.
