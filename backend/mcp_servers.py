"""
MCP (Model Context Protocol) server configuration for Semgrep integration.

This module provides helper functions for building and configuring an
MCP server instance that exposes Semgrep as a tool the security agent
can call during analysis. The server is launched via `uvx` and filtered
to allow only the `semgrep_scan` tool.
"""

import os
from typing import Any, Dict

from agents.mcp import MCPServerStdio, create_static_tool_filter


# --------------------------------------------------
# 🛠️ Semgrep MCP server configuration
# --------------------------------------------------

def get_semgrep_server_params() -> Dict[str, Any]:
    """
    Build the configuration parameters required to launch
    the Semgrep MCP server.

    Parameters
    ----------
    None

    Returns
    -------
    dict
        A dictionary containing:
        - the command used to launch the MCP server
        - its arguments
        - an environment variable map (including Semgrep tokens)

    Notes
    -----
    The environment includes:
    - `SEMGREP_APP_TOKEN` from OS environment
    - `PYTHONUNBUFFERED=1` to ensure unbuffered server output
    """
    # Retrieve the Semgrep app token from environment variables
    semgrep_app_token: str | None = os.getenv("SEMGREP_APP_TOKEN")

    # Build the environment dictionary passed to the MCP server process
    env: Dict[str, str | None] = {
        "SEMGREP_APP_TOKEN": semgrep_app_token,
        "PYTHONUNBUFFERED": "1",  # Ensures immediate stdout flushing
    }

    # Return the full invocation parameters for the Semgrep MCP server
    return {
        "command": "uvx",
        "args": [
            "--with", "mcp==1.12.2",
            "--quiet",              # Reduce uvx console noise
            "semgrep-mcp"           # MCP server implementation
        ],
        "env": env,
    }


# --------------------------------------------------
# 🚀 Semgrep MCP server creation
# --------------------------------------------------

def create_semgrep_server() -> MCPServerStdio:
    """
    Create and configure a Semgrep MCP server instance.

    This function wraps the Semgrep server parameters and applies
    a strict tool filter so that the agent can access **only**
    the `semgrep_scan` tool.

    Returns
    -------
    MCPServerStdio
        A configured MCP server instance ready for use as an async context manager.

    Notes
    -----
    The server is created with:
    - a 120-second client timeout
    - a static tool filter that allows only `semgrep_scan`
    """
    # Build the launch parameters for Semgrep
    params: Dict[str, Any] = get_semgrep_server_params()

    # Return a fully configured MCP server instance
    return MCPServerStdio(
        params=params,
        client_session_timeout_seconds=120,
        tool_filter=create_static_tool_filter(
            allowed_tool_names=["semgrep_scan"]
        ),
    )
