import os
import typer

from mac_spot.gemini_client import generate_stream, SYSTEM_PROMPT
from mac_spot.output import stream_output_panel, print_error

def review_command(
    file_path: str = typer.Argument(..., help="Path to the file to review."),
    focus: str = typer.Option(
        "bugs", 
        "--focus", 
        "-f", 
        help="Review focus area: bugs, performance, style, security, or all."
    )
) -> None:
    """Analyze a code file and output suggested improvements, bugs, and style issues."""
    if not os.path.exists(file_path):
        print_error(f"File not found: {file_path}")
        raise typer.Exit(code=1)
        
    try:
        with open(file_path, "r") as f:
            code_content = f.read()
    except Exception as e:
        print_error(f"Failed to read file: {e}")
        raise typer.Exit(code=1)

    filename = os.path.basename(file_path)
    
    user_prompt = (
        f"Review the code in the file '{filename}'.\n"
        f"Focus area: {focus}.\n\n"
        f"Please organize your output in Markdown with the following sections:\n"
        f"1. **Issues Table**: A Markdown table with columns: ID, Severity (Critical/Warning/Info), Category, and Description.\n"
        f"2. **Detailed Recommendations**: A breakdown of each issue, including code suggestions or diff-style comparisons.\n\n"
        f"Here is the code to review:\n"
        f"```\n{code_content}\n```"
    )

    stream = generate_stream(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
    stream_output_panel(stream, title=f"Code Review: {filename}")
