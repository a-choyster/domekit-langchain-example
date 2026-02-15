"""Tests for domekit.yaml — verifies manifest structure and policy."""

import os

import yaml
import pytest

MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "..", "domekit.yaml")


@pytest.fixture
def manifest():
    with open(MANIFEST_PATH) as f:
        return yaml.safe_load(f)


def test_manifest_loads(manifest):
    assert manifest is not None


def test_app_name(manifest):
    assert manifest["app"]["name"] == "langchain-example"


def test_network_outbound_deny(manifest):
    assert manifest["policy"]["network"]["outbound"] == "deny"


def test_tools_allow_list(manifest):
    tools = manifest["policy"]["tools"]["allow"]
    assert "sql_query" in tools
    assert "read_file" in tools
    assert "vector_search" in tools


def test_sqlite_allow(manifest):
    assert "data/books.db" in manifest["policy"]["data"]["sqlite"]["allow"]


def test_filesystem_no_writes(manifest):
    assert manifest["policy"]["data"]["filesystem"]["allow_write"] == []


def test_vector_collection(manifest):
    assert "book-summaries" in manifest["policy"]["data"]["vector"]["allow"]


def test_embedding_config(manifest):
    assert manifest["embedding"]["backend"] == "ollama"
    assert manifest["embedding"]["model"] == "nomic-embed-text"


def test_vector_db_config(manifest):
    assert manifest["vector_db"]["backend"] == "chroma"
    assert manifest["vector_db"]["default_top_k"] == 5


def test_audit_path(manifest):
    assert manifest["audit"]["path"] == "audit.jsonl"
