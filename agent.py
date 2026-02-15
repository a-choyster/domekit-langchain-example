# LangChain agent that talks to DomeKit.
#
# DomeKit sits between this agent and the LLM, exposing an OpenAI-compatible
# API on localhost:8080. LangChain doesn't know DomeKit is there -- it just
# sees an OpenAI endpoint. But every tool call is policy-checked against
# domekit.yaml and logged to audit.jsonl.

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

# Point LangChain at DomeKit's local endpoint instead of OpenAI.
# DomeKit forwards requests to Ollama (llama3.1:8b) after policy checks.
llm = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed",
    model="llama3.1:8b",
    temperature=0,
)


@tool
def sql_query(query: str) -> str:
    """Execute a read-only SQL query against the books database.

    Use this to look up books by title, author, year, or genre.
    The database has a single table called 'books' with columns:
    id, title, author, year, genre.
    """
    # DomeKit intercepts this tool call, checks it against the policy
    # (only data/books.db is allowed), executes it, and returns the result.
    # We just pass the query through -- DomeKit does the rest.
    return f"[sql_query] {query}"


@tool
def vector_search(query: str) -> str:
    """Search book summaries by semantic similarity.

    Use this to find books related to a topic or theme, even if the
    exact words don't appear in the database.
    """
    # DomeKit handles the actual vector search against the book-summaries
    # collection. The policy allows only that collection.
    return f"[vector_search] {query}"


@tool
def read_file(path: str) -> str:
    """Read a file from the data directory.

    Use this to read supplementary data files. Only files under data/
    are accessible.
    """
    # DomeKit enforces the filesystem policy: only data/ is readable,
    # nothing is writable.
    return f"[read_file] {path}"


# Bind the tools to the model so LangChain knows what's available.
tools = [sql_query, vector_search, read_file]
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = """You are a helpful librarian assistant. You have access to:
- A SQLite database of books (use sql_query)
- A vector search over book summaries (use vector_search)
- The ability to read files in the data directory (use read_file)

When the user asks about books, use your tools to look up real answers.
Be concise and helpful."""


def main():
    print("LangChain + DomeKit Book Agent")
    print("Type your questions about books. Press Ctrl+C to exit.\n")

    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        messages.append(HumanMessage(content=user_input))
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        # If the model wants to call tools, show what it's doing.
        if response.tool_calls:
            for tc in response.tool_calls:
                print(f"  [tool] {tc['name']}({tc['args']})")
            # In a full implementation, DomeKit would execute the tools
            # and return results. For this demo we show the intent.
            print(f"Agent: {response.content or '(tool calls issued -- see above)'}")
        else:
            print(f"Agent: {response.content}")

        print()


if __name__ == "__main__":
    main()
