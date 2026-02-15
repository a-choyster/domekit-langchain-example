# LangChain + DomeKit Example

This example shows how to run a LangChain agent through [DomeKit](https://github.com/a-choyster/domekit), an open-source local-first AI runtime with enforced privacy boundaries. DomeKit exposes an OpenAI-compatible API on `localhost:8080`, so LangChain treats it like any other OpenAI endpoint. Behind the scenes, DomeKit policy-checks every tool call and audit-logs everything -- your agent gets guardrails without changing a single line of LangChain code.

## Prerequisites

- **Python 3.11+**
- **Ollama** installed and running, with the `llama3.1:8b` model pulled:
  ```bash
  ollama pull llama3.1:8b
  ```
- **DomeKit** cloned and installed. Follow the setup instructions at [github.com/a-choyster/domekit](https://github.com/a-choyster/domekit).

## Setup

1. **Clone this repo:**
   ```bash
   git clone https://github.com/a-choyster/domekit-langchain-example.git
   cd domekit-langchain-example
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create the sample database:**
   ```bash
   python setup_data.py
   ```

4. **Start DomeKit with the included manifest:**
   ```bash
   domekit run --manifest domekit.yaml
   ```
   Leave this running in a separate terminal. DomeKit will start serving on `http://localhost:8080`.

5. **Run the agent:**
   ```bash
   python agent.py
   ```
   Type questions about books and the agent will query the SQLite database and search book summaries -- all policy-checked by DomeKit.

## What to Expect

The agent can:
- Query the `books` SQLite database (titles, authors, years, genres)
- Search book summaries via vector search over the `book-summaries` collection

Every tool call the agent makes passes through DomeKit's policy engine. If the agent tried to access a file outside `data/` or call a tool not in the allow-list, DomeKit would block it.

Example interaction:
```
You: What sci-fi books are in the database?
Agent: Let me check the database...
       [sql_query] SELECT * FROM books WHERE genre = 'Science Fiction'
       ...
```

## Checking the Audit Log

DomeKit writes every tool call and policy decision to `audit.jsonl`. Inspect it with:

```bash
cat audit.jsonl | python -m json.tool --json-lines
```

Each entry includes the tool name, arguments, policy verdict, and timestamp.

## Links

- [DomeKit](https://github.com/a-choyster/domekit) -- the local-first AI runtime powering this example
