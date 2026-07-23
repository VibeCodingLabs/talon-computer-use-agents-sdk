import os
import sys
import asyncio
from typing import Any
import typer

# Ensure schemas can be imported by adding the root project dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from schemas.voice_intents.voice_intents import ParsedVoiceCommand

# Instructor + OpenAI SDK for Groq inference
import instructor
from openai import AsyncOpenAI

# Load from environment

# Initialize Instructor with Groq's OpenAI-compatible endpoint
# We use Mode.JSON for pure JSON mode compatibility


def get_instructor_client():
    """Lazy-load the client to prevent crash if API key is missing at import time."""
    key = os.getenv("GROQ_API_KEY", "")
    if not key:
        return None
    return instructor.from_openai(
        AsyncOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=key,
        ),
        mode=instructor.Mode.JSON,
    )


async def parse_voice_command(transcript: str) -> ParsedVoiceCommand:
    """Uses Groq + Instructor to convert natural language into a strict Pydantic schema."""
    client = get_instructor_client()
    if not client:
        raise ValueError("Cannot parse: GROQ_API_KEY is missing.")

    print(f"[*] Parsing transcript: '{transcript}'")

    # We use llama3-8b-8192 for extreme speed and low latency
    command = await client.chat.completions.create(
        model="llama-3.1-8b-instant",
        response_model=ParsedVoiceCommand,
        max_retries=3,  # Instructor will automatically retry and self-heal up to 3 times if schema fails!
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the central parsing brain of a Voice-to-IDE execution engine. "
                    "Map the user's natural language spoken command into a strict sequence of executable intents. "
                    "If they ask to type text, ensure correct capitalization and syntax. "
                    "If they ask to press a key, format it for Talon (e.g., 'enter', 'ctrl-c'). "
                    "If they ask to run a terminal command, extract the exact bash command."
                ),
            },
            {"role": "user", "content": transcript},
        ],
        temperature=0.0,
    )
    return command


async def execute_action(intent: Any):
    """Executes the parsed Pydantic intent natively using Linux tools."""
    print(f"[*] Executing Intent: {intent.action}")
    try:
        if intent.action == "type_text":
            import subprocess

            subprocess.run(["wtype", intent.text], check=True)
            print(f"    [+] Typed text: {intent.text}")
        elif intent.action == "run_cli":
            import subprocess

            subprocess.Popen(intent.command, shell=True)
            print(f"    [+] Ran command: {intent.command}")
        else:
            print(
                f"    [!] Executor for {intent.action} not yet implemented natively. Outputting schema: {intent.model_dump_json()}"
            )
    except Exception as e:
        print(f"    [!] Native Execution Error: {e}")


async def process_transcript(transcript: str):
    """Main pipeline: Parse -> Validate -> Execute"""
    key = os.getenv("GROQ_API_KEY", "")
    if not key:
        print(
            "[!] GROQ_API_KEY not found in environment. Please export it or add it to your .env."
        )
        return

    try:
        # 1. Parse via Instructor (Auto-heals schema errors)
        parsed_command = await parse_voice_command(transcript)

        print(f"\n=== Parsed {len(parsed_command.intents)} Intents ===")
        for i, intent in enumerate(parsed_command.intents):
            print(
                f"{i + 1}. {intent.action.upper()} (Confidence: {intent.confidence:.2f})"
            )

        print("========================\n")

        # 2. Execute each intent sequentially via Talon
        # 2. Execute each intent sequentially
        for intent in parsed_command.intents:
            await execute_action(intent)

    except Exception as e:
        print(f"[!] Error processing transcript: {e}")


app = typer.Typer(help="Voice-to-IDE Execution Engine CLI")


@app.command()
def parse(
    transcript: str = typer.Argument(..., help="The natural language command to parse"),
):
    """Parse and execute a natural language transcript."""
    asyncio.run(process_transcript(transcript))


if __name__ == "__main__":
    app()
