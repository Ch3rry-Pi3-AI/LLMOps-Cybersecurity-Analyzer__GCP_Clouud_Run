# **Backend**

This folder contains the FastAPI-based backend for the Cybersecurity Analyzer. It provides the security analysis API, integrates Semgrep through an MCP server, and serves the production frontend when deployed.

## Key Modules

* **`server.py`**
  Main FastAPI application.
  Handles:

  * `/api/analyze` security analysis endpoint
  * health and diagnostic endpoints
  * integration with the Semgrep MCP server
  * static file serving in production

* **`context.py`**
  Holds system-level agent instructions and helpers for generating analysis prompts and enriched summaries.

* **`mcp_server.py`**
  Configures and launches the Semgrep MCP server used by the AI agent for static analysis.

## Purpose

The backend coordinates both AI-driven and static code analysis. It acts as the central processing layer for the application, providing structured security reports to the frontend.

## Running the Backend

Use Uvicorn for local development:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

Environment variables such as `OPENAI_API_KEY` and `SEMGREP_APP_TOKEN` must be set before running the service.