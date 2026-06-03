import typer

from mac_spot.gemini_client import generate_stream, SYSTEM_PROMPT
from mac_spot.output import stream_output_panel, print_error

VALID_TOPICS = [
    "langchain", "langgraph", "huggingface", "faiss", "chromadb",
    "openai-api", "gemini-api", "pytorch", "fastapi", "docker",
    "git", "regex", "bash"
]

def sheet_command(
    topic: str = typer.Argument(..., help=f"The cheatsheet topic. Allowed: {', '.join(VALID_TOPICS)}")
) -> None:
    """Generate a structured developer cheatsheet for popular developer frameworks, libraries, or tools."""
    topic_clean = topic.strip().lower()
    
    if topic_clean not in VALID_TOPICS:
        print_error(
            f"Unsupported topic '{topic}'.\n"
            f"Please choose one of the following: {', '.join(VALID_TOPICS)}"
        )
        raise typer.Exit(code=1)

    user_prompt = (
        f"Generate a comprehensive, structured cheatsheet for '{topic_clean}'.\n\n"
        f"The output must contain the following sections in Markdown:\n"
        f"1. **Core Classes & Structures** (essential imports and components)\n"
        f"2. **Key Methods & API Calls** (or essential command syntax)\n"
        f"3. **Quick Usage Code Snippets** (production-ready copy-paste examples)\n"
        f"4. **Gotchas & Best Practices** (common pitfalls and troubleshooting tips)\n\n"
        f"Format everything clearly with code blocks and concise, high-value bullet points."
    )

    stream = generate_stream(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
    stream_output_panel(stream, title=f"Cheatsheet: {topic_clean}")
