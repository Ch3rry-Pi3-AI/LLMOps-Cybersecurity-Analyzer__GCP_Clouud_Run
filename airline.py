"""
Airline assistant application using the Agent/Runner framework.

This script:
- sets up a small SQLite database of city ticket prices,
- exposes agent tools for querying prices and evaluating expressions,
- defines an airline assistant that can calculate discounts and answer
  travel questions for "FlightAI",
- launches a Gradio chat interface in the browser.
"""

from __future__ import annotations

import sqlite3
import traceback
from typing import Any, Dict, List

import gradio as gr
from dotenv import load_dotenv

from agents import Agent, Runner, function_tool


# ------------------------------------------------------------
# 🚀 Environment Setup
# ------------------------------------------------------------

# Load environment variables, overriding existing environments if present
load_dotenv(override=True)

# LLM model used by the Airline AI assistant
MODEL: str = "gpt-4.1-mini"


# ------------------------------------------------------------
# ✈️ Airline Agent Instructions
# ------------------------------------------------------------

# Base prompt for the FlightAI assistant
instructions: str = (
    "You are a helpful assistant for an Airline called FlightAI. "
    "Use your tools to get ticket prices and calculate discounts. "
    "Trips to London have a 10% discount on the price. "
    "Always be accurate. If you don't know the answer, say so."
)


# ------------------------------------------------------------
# 💾 SQLite Ticket Database Setup
# ------------------------------------------------------------

# Database file name
DB: str = "prices.db"

# Initial ticket prices used to populate the table
initial_ticket_prices: Dict[str, float] = {
    "london": 799,
    "paris": 899,
    "tokyo": 1400,
    "sydney": 2999,
}

# Create table and populate with initial data (if not already present)
with sqlite3.connect(DB) as conn:
    cursor = conn.cursor()

    # Create table for ticket prices
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS prices (city TEXT PRIMARY KEY, price REAL)"
    )

    # Insert initial rows but ignore duplicates
    for city, price in initial_ticket_prices.items():
        cursor.execute(
            "INSERT OR IGNORE INTO prices (city, price) VALUES (?, ?)",
            (city, price),
        )

    conn.commit()


# ------------------------------------------------------------
# 🧰 Agent Tools
# ------------------------------------------------------------

@function_tool
def get_ticket_price(city: str) -> str:
    """
    Retrieve the ticket price for the given city.

    Parameters
    ----------
    city : str
        City name to query.

    Returns
    -------
    str
        Price in dollars (e.g., "$799") or "Not found" if unavailable.

    Notes
    -----
    A parameterised query is used to prevent SQL injection.
    """
    print(f"TOOL CALLED: Getting price for {city}", flush=True)

    try:
        # Convert city name to lowercase for consistency
        city_normalised = city.lower()

        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()

            # Parameterised SQL query ensures safety
            cursor.execute("SELECT price FROM prices WHERE city = ?", (city_normalised,))
            result = cursor.fetchone()

            return f"${result[0]}" if result else "Not found"

    except Exception:
        # Capture full traceback for debugging
        return f"Error: {traceback.format_exc()}"


@function_tool
def calculate(expr: str) -> str:
    """
    Evaluate a numeric expression (e.g., "799 * 0.9").

    Parameters
    ----------
    expr : str
        Python-compatible numeric expression to evaluate.

    Returns
    -------
    str
        Evaluation result converted to string.

    Warning
    -------
    `eval()` is potentially unsafe. Only trusted expressions should be allowed.
    """
    print(f"TOOL CALLED: Calculating {expr}", flush=True)
    try:
        # NOTE: eval is inherently risky, but acceptable here because it is tool-restricted.
        return str(eval(expr))
    except Exception:
        return f"Error: {traceback.format_exc()}"


# ------------------------------------------------------------
# 🤖 Chat Function (Agent Execution)
# ------------------------------------------------------------

async def chat(message: str, history: List[Dict[str, str]]) -> str:
    """
    Handle chat messages from the user and return the assistant's reply.

    Parameters
    ----------
    message : str
        Latest message from the user.
    history : list of dict
        Chat history where each entry contains `role` and `content`.

    Returns
    -------
    str
        Final content output from the agent.
    """
    # Convert history into messages suitable for the Agent API
    messages = [{"role": m["role"], "content": m["content"]} for m in history]
    messages.append({"role": "user", "content": message})

    # Create FlightAI agent configured with tools
    agent = Agent(
        name="FlightAI",
        instructions=instructions,
        model=MODEL,
        tools=[get_ticket_price, calculate],
    )

    # Run the agent with the message list
    result = await Runner.run(agent, messages)

    # Return the final text output
    return result.final_output


# ------------------------------------------------------------
# 💬 Gradio Chat Interface
# ------------------------------------------------------------

# Launch a browser-based chat UI using Gradio
gr.ChatInterface(chat, type="messages").launch(inbrowser=True)
