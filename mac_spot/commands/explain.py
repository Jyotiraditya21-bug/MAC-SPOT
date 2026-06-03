import os
from typing import Optional
import typer

from mac_spot.gemini_client import generate_stream, SYSTEM_PROMPT
from mac_spot.output import stream_output_panel, print_error

def explain_command(
    error: Optional[str] = typer.Argument(None, help="The error message to explain."),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Read the error message from a file."),
    lang: Optional[str] = typer.Option(None, "--lang", "-l", help="Programming language context (e.g., Python, Go, JS).")
) -> None:
    """Explain a terminal/code error, its root cause, and how to fix it."""
    if not error and not file:
        print_error("Please provide either an error message or use the --file flag to read from a file.")
        raise typer.Exit(code=1)
        
    error_content = ""
    if file:
        if not os.path.exists(file):
            print_error(f"File not found: {file}")
            raise typer.Exit(code=1)
        try:
            with open(file, "r") as f:
                error_content = f.read()
        except Exception as e:
            print_error(f"Failed to read file: {e}")
            raise typer.Exit(code=1)
    else:
        error_content = error

    user_prompt = "Explain what this error means, its root cause, and the exact fix with a code snippet.\n"
    if lang:
        user_prompt += f"Language context: {lang}\n"
    user_prompt += f"Error content:\n```\n{error_content}\n```"

    stream = generate_stream(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
    stream_output_panel(stream, title="Error Explanation")
