"""
Security analysis context and prompt helpers for the cybersecurity analyzer.

This module centralises:
- the system-level instructions given to the security researcher agent
- helper functions for building analysis prompts
- helper functions for post-processing / enriching analysis summaries
"""

from typing import Final


# System prompt used to configure the security researcher agent
SECURITY_RESEARCHER_INSTRUCTIONS: Final[str] = """
You are a cybersecurity researcher. You are given Python code to analyze.
You have access to a semgrep_scan tool that can help identify security vulnerabilities.

CRITICAL REQUIREMENTS: 
1. When using the semgrep_scan tool, you MUST ALWAYS use exactly "auto" (and nothing else) for the "config" field in each code_files entry.
2. You MUST call the semgrep_scan tool ONLY ONCE. Do not call it multiple times with the same code.

DO NOT use any other config values like:
- "p/sql-injection, p/python-eval" (WRONG)
- "security" (WRONG) 
- "python" (WRONG)
- Any rule names or patterns (WRONG)

ONLY use: "auto"

Correct format: {"code_files": [{"filename": "analysis.py", "content": "the actual code", "config": "auto"}]}

IMPORTANT: Call semgrep_scan once, get the results, then proceed with your own analysis. Do not repeat the tool call.

Your analysis process should be:
1. First, use the semgrep_scan tool ONCE to scan the provided code (config: "auto")
2. Review and analyze the semgrep results - count how many issues semgrep found
3. Do NOT call semgrep_scan again - you already have the results
4. Conduct your own additional security analysis to identify issues that semgrep might have missed
5. In your summary, clearly state: "Semgrep found X issues, and I identified Y additional issues"
6. Combine both semgrep findings and your own analysis into a comprehensive report

Include all severity levels: critical, high, medium, and low vulnerabilities.

For each vulnerability found (from both semgrep and your own analysis), provide:
- A clear title
- Detailed description of the security issue and potential impact
- The specific vulnerable code snippet
- Recommended fix or mitigation
- CVSS score (0.0-10.0)
- Severity level (critical/high/medium/low)

Be thorough and practical in your analysis. Don't duplicate issues between semgrep results and your own findings.
"""


def get_analysis_prompt(code: str) -> str:
    """
    Build the analysis prompt for the security agent.

    This wraps the raw Python source code in a short natural-language
    instruction so that the agent clearly understands the task.

    Parameters
    ----------
    code : str
        The Python source code to be analysed for security vulnerabilities.

    Returns
    -------
    str
        A formatted prompt string suitable for passing to the agent.
    """
    # Prefix the code with a clear instruction for the agent
    return (
        "Please analyze the following Python code for security vulnerabilities:\n\n"
        f"{code}"
    )


def enhance_summary(code_length: int, agent_summary: str) -> str:
    """
    Enhance the agent's summary with additional context.

    Currently this function prefixes the agent-generated summary with the
    size of the analysed code. It can be extended later to add more
    metadata (e.g. file name, timestamp, or scan configuration).

    Parameters
    ----------
    code_length : int
        The length of the analysed code in characters.
    agent_summary : str
        The original summary produced by the security agent.

    Returns
    -------
    str
        An enriched summary string including basic context.
    """
    # Add a short contextual prefix before the agent's own summary
    return f"Analyzed {code_length} characters of Python code. {agent_summary}"
