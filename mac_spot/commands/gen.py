import re
import typer
import pyperclip

from mac_spot.gemini_client import generate_stream, SYSTEM_PROMPT
from mac_spot.output import stream_output_panel, print_success

def extract_code_block(text: str) -> str:
    """Extract code from within markdown code blocks (```lang ... ```).
    If no code block is found, returns the original text.
    """
    pattern = r"```(?:\w+)?\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def gen_command(
    prompt: str = typer.Argument(..., help="Natural language prompt describing what code to generate."),
    lang: str = typer.Option("python", "--lang", "-l", help="Language for the code (e.g., python, js, bash, sql, yaml)."),
    copy: bool = typer.Option(False, "--copy", "-c", help="Auto-copy the generated code to clipboard.")
) -> None:
    """Generate production-ready, commented code block for a prompt."""
    user_prompt = (
        f"Generate clean, commented, production-ready code for the following task.\n"
        f"Language: {lang}\n"
        f"Task:\n{prompt}\n\n"
        f"Return the code inside a standard markdown code block. Keep any explanations brief and inside comments."
    )

    stream = generate_stream(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
    full_response = stream_output_panel(stream, title=f"Generated Code ({lang})")

    if copy:
        code_only = extract_code_block(full_response)
        try:
            pyperclip.copy(code_only)
            print_success("Generated code successfully copied to clipboard!")
        except Exception as e:
            # Catch clipboard exceptions (e.g. headless environments)
            from mac_spot.output import print_warning
            print_warning(f"Could not copy to clipboard: {e}")
