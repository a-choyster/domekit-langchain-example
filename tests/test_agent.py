"""Tests for agent.py — verifies imports, configuration, and tool definitions."""

import os
import sys

import pytest

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_langchain_imports():
    """LangChain packages are installed and importable."""
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
    from langchain_core.tools import tool


def test_agent_module_imports():
    """agent.py imports without errors."""
    import agent


def test_llm_configured_for_domekit():
    """LLM points at DomeKit's local endpoint, not OpenAI."""
    import agent

    assert "localhost:8080" in agent.llm.openai_api_base or "localhost:8080" in str(
        agent.llm.openai_api_base
    )


def test_llm_api_key_is_placeholder():
    """API key should be a placeholder since DomeKit doesn't need one."""
    import agent

    assert agent.llm.openai_api_key is not None


def test_three_tools_defined():
    """Agent should have exactly 3 tools: sql_query, vector_search, read_file."""
    import agent

    tool_names = {t.name for t in agent.tools}
    assert tool_names == {"sql_query", "vector_search", "read_file"}


def test_tools_have_descriptions():
    """Each tool should have a non-empty description for the LLM."""
    import agent

    for t in agent.tools:
        assert t.description, f"Tool {t.name} has no description"


def test_system_prompt_exists():
    """System prompt should be defined and non-empty."""
    import agent

    assert agent.SYSTEM_PROMPT
    assert len(agent.SYSTEM_PROMPT) > 50
