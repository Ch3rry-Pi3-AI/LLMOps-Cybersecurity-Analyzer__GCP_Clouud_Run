"""
FastAPI backend for the LLMOps Cybersecurity Analyzer.

This service exposes:
- an `/api/analyze` endpoint for running security analysis on uploaded code
  using an OpenAI-powered agent combined with Semgrep-based static analysis
- health and diagnostics endpoints for connectivity and Semgrep integration
- static file serving for the frontend in production deployments
"""

import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from agents import Agent, Runner, trace
from context import SECURITY_RESEARCHER_INSTRUCTIONS, get_analysis_prompt, enhance_summary
from mcp_servers import create_semgrep_server


# --------------------------------------------------
# 🔐 Environment and application setup
# --------------------------------------------------

# Load environment variables from a .env file into the process environment
load_dotenv()

# Create the FastAPI application instance with a descriptive title
app: FastAPI = FastAPI(title="Cybersecurity Analyzer API")


# --------------------------------------------------
# 🌍 CORS configuration
# --------------------------------------------------

# Define allowed origins for development and containerised environments
cors_origins: List[str] = [
    "http://localhost:3000",    # Local development
    "http://frontend:3000",     # Docker-based frontend in development
]

# In production, allow all origins (frontend is normally served from the same domain)
if os.getenv("ENVIRONMENT") == "production":
    # Allow requests from any origin (can be tightened if you know the exact domain)
    cors_origins.append("*")

# Attach the CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# 🧾 Request / response models
# --------------------------------------------------

class AnalyzeRequest(BaseModel):
    """
    Request model for the `/api/analyze` endpoint.

    Expects the raw source code to be analysed as a string.

    Attributes
    ----------
    code : str
        Source code to be analysed for security vulnerabilities.
    """
    code: str


class SecurityIssue(BaseModel):
    """
    Represents a single security issue found in the analysed code.

    Includes metadata about the issue, the vulnerable code snippet,
    and a suggested fix with an associated CVSS score.

    Attributes
    ----------
    title : str
        Brief title of the security vulnerability.
    description : str
        Detailed description of the issue and its potential impact.
    code : str
        Code snippet that demonstrates the vulnerability.
    fix : str
        Recommended fix or mitigation strategy.
    cvss_score : float
        CVSS score between 0.0 and 10.0 indicating severity.
    severity : str
        Severity level, e.g. "critical", "high", "medium", or "low".
    """
    title: str = Field(description="Brief title of the security vulnerability")
    description: str = Field(
        description="Detailed description of the security issue and its potential impact"
    )
    code: str = Field(
        description="The specific vulnerable code snippet that demonstrates the issue"
    )
    fix: str = Field(description="Recommended code fix or mitigation strategy")
    cvss_score: float = Field(
        description="CVSS score from 0.0 to 10.0 representing severity"
    )
    severity: str = Field(
        description="Severity level: critical, high, medium, or low"
    )


class SecurityReport(BaseModel):
    """
    Top-level security report returned to the frontend.

    Contains an executive summary as well as a list of individual security issues.

    Attributes
    ----------
    summary : str
        Executive-style summary of the security analysis.
    issues : list of SecurityIssue
        List of identified security vulnerabilities.
    """
    summary: str = Field(description="Executive summary of the security analysis")
    issues: List[SecurityIssue] = Field(
        description="List of identified security vulnerabilities"
    )


# --------------------------------------------------
# 🧪 Validation and configuration helpers
# --------------------------------------------------

def validate_request(request: AnalyzeRequest) -> None:
    """
    Validate the analysis request payload.

    Ensures that the `code` field is not empty or whitespace-only.

    Parameters
    ----------
    request : AnalyzeRequest
        The incoming request model containing the code to analyse.

    Raises
    ------
    HTTPException
        If the request does not contain usable source code.
    """
    # Strip whitespace and check if any code remains
    if not request.code.strip():
        # Abort with a 400 Bad Request if no code is provided
        raise HTTPException(status_code=400, detail="No code provided for analysis")


def check_api_keys() -> None:
    """
    Verify that required API keys are configured.

    Currently ensures that the OpenAI API key is available in the environment.

    Raises
    ------
    HTTPException
        If the OpenAI API key is missing.
    """
    # Read the OpenAI API key from environment variables
    if not os.getenv("OPENAI_API_KEY"):
        # If the key is missing, return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")


# --------------------------------------------------
# 🤖 Agent creation and analysis execution
# --------------------------------------------------

def create_security_agent(semgrep_server: Any) -> Agent:
    """
    Create and configure the security analysis agent.

    The agent:
    - uses SECURITY_RESEARCHER_INSTRUCTIONS as its system prompt
    - is backed by a specified LLM model
    - integrates with an MCP Semgrep server
    - returns structured `SecurityReport` objects

    Parameters
    ----------
    semgrep_server : Any
        An MCP server instance providing Semgrep-based static analysis tools.

    Returns
    -------
    Agent
        Configured security research agent capable of producing SecurityReport results.
    """
    # Instantiate an Agent configured for security research tasks
    return Agent(
        name="Security Researcher",
        instructions=SECURITY_RESEARCHER_INSTRUCTIONS,
        model="gpt-4.1-mini",
        mcp_servers=[semgrep_server],
        output_type=SecurityReport,
    )


async def run_security_analysis(code: str) -> SecurityReport:
    """
    Execute the full security analysis workflow for a given code string.

    Steps
    -----
    1. Create an MCP Semgrep server connection.
    2. Initialise the security agent with the Semgrep tool.
    3. Run the agent with an analysis prompt built from the input code.
    4. Convert the final agent output into a `SecurityReport` instance.

    Parameters
    ----------
    code : str
        Source code to analyse for security vulnerabilities.

    Returns
    -------
    SecurityReport
        Structured report containing summary and list of security issues.

    Raises
    ------
    Exception
        Propagates any unexpected error during analysis execution.
    """
    # Create a trace span for observability and debugging
    with trace("Security Researcher"):
        # Open a context-managed Semgrep MCP server
        async with create_semgrep_server() as semgrep:
            # Build a specialised security analysis agent
            agent: Agent = create_security_agent(semgrep)
            # Run the agent using a generated analysis prompt
            result: Any = await Runner.run(agent, input=get_analysis_prompt(code))
            # Convert the agent output into the strongly-typed SecurityReport model
            return result.final_output_as(SecurityReport)


def format_analysis_response(code: str, report: SecurityReport) -> SecurityReport:
    """
    Post-process and format the final analysis response.

    Enhances the summary using the length of the analysed code and
    preserves the list of identified issues.

    Parameters
    ----------
    code : str
        The original source code that was analysed.
    report : SecurityReport
        Raw report generated by the security analysis pipeline.

    Returns
    -------
    SecurityReport
        New report with an enhanced summary and original issues.
    """
    # Use a helper to enhance or refine the summary based on code length
    enhanced_summary: str = enhance_summary(len(code), report.summary)

    # Construct a new SecurityReport with the improved summary
    return SecurityReport(summary=enhanced_summary, issues=report.issues)


# --------------------------------------------------
# 🌐 API endpoints
# --------------------------------------------------

@app.post("/api/analyze", response_model=SecurityReport)
async def analyze_code(request: AnalyzeRequest) -> SecurityReport:
    """
    Analyse Python code for security vulnerabilities.

    This endpoint:
    - validates the incoming request
    - checks that required API keys are configured
    - runs a combined Semgrep + LLM security analysis
    - returns a structured `SecurityReport` or raises an error

    Parameters
    ----------
    request : AnalyzeRequest
        Request body containing the code to be analysed.

    Returns
    -------
    SecurityReport
        Structured security analysis report.

    Raises
    ------
    HTTPException
        If the request is invalid or if an internal error occurs during analysis.
    """
    # Ensure the request contains valid code to analyse
    validate_request(request)
    # Ensure required API credentials are present
    check_api_keys()

    try:
        # Run the async security analysis workflow
        report: SecurityReport = await run_security_analysis(request.code)
        # Enhance and return the final formatted response
        return format_analysis_response(request.code, report)
    except Exception as e:
        # Wrap unexpected errors into a generic 500 response
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/health")
async def health() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns a simple message to confirm that the API is reachable.

    Returns
    -------
    dict of str to str
        Dictionary containing a single `"message"` key.
    """
    # Respond with a minimal JSON payload indicating service status
    return {"message": "Cybersecurity Analyzer API"}


@app.get("/network-test")
async def network_test() -> Dict[str, Any]:
    """
    Test network connectivity to the Semgrep API.

    Attempts to contact the Semgrep public API endpoint and returns:

    - whether the API is reachable
    - the HTTP status code
    - the size of the response payload

    Returns
    -------
    dict of str to Any
        Diagnostics describing Semgrep API reachability and response details.
    """
    import httpx

    try:
        # Create an async HTTP client with a sensible timeout
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Send a GET request to the Semgrep API root
            response: httpx.Response = await client.get("https://semgrep.dev/api/v1/")
            # Return basic diagnostics about the response
            return {
                "semgrep_api_reachable": True,
                "status_code": response.status_code,
                "response_size": len(response.content),
            }
    except Exception as e:
        # On any error, report that the API could not be reached
        return {
            "semgrep_api_reachable": False,
            "error": str(e),
        }


@app.get("/semgrep-test")
async def semgrep_test() -> Dict[str, Any]:
    """
    Test whether the Semgrep CLI can be installed and invoked.

    This endpoint:
    - attempts to `pip install semgrep`
    - runs `semgrep --version` to confirm it is callable
    - returns diagnostic information about installation and version

    Returns
    -------
    dict of str to Any
        Diagnostics indicating whether Semgrep was installed and callable,
        along with any relevant output or error messages.
    """
    import subprocess

    try:
        # Try to install Semgrep using pip with a timeout to avoid hanging
        install_result: subprocess.CompletedProcess[str] = subprocess.run(
            ["pip", "install", "semgrep"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        # If installation failed, return the error output
        if install_result.returncode != 0:
            return {
                "semgrep_install": False,
                "error": f"Install failed: {install_result.stderr}",
            }

        # If installation succeeded, check that Semgrep responds to --version
        version_result: subprocess.CompletedProcess[str] = subprocess.run(
            ["semgrep", "--version"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Return both installation and version check results
        return {
            "semgrep_install": True,
            "version_check": version_result.returncode == 0,
            "version_output": version_result.stdout,
            "version_error": version_result.stderr,
        }

    except subprocess.TimeoutExpired:
        # Handle cases where installation or version check exceeds the timeout
        return {
            "semgrep_install": False,
            "error": "Timeout during semgrep installation or version check",
        }
    except Exception as e:
        # Catch-all for unexpected errors during installation or version check
        return {
            "semgrep_install": False,
            "error": str(e),
        }


# --------------------------------------------------
# 📁 Static file mounting (frontend assets)
# --------------------------------------------------

# If a "static" directory exists, serve it as the root path
if os.path.exists("static"):
    # Mount static files so the frontend can be served by the same FastAPI app
    app.mount("/", StaticFiles(directory="static", html=True), name="static")


# --------------------------------------------------
# 🚀 Local development entry point
# --------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn for local development
    uvicorn.run(app, host="0.0.0.0", port=8000)
