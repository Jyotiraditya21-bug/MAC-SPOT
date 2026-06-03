import typer

from mac_spot.gemini_client import generate_stream, SYSTEM_PROMPT
from mac_spot.output import stream_output_panel

def learn_command(
    concept: str = typer.Argument(..., help="The concept you want to learn (e.g., RAG, LoRA, Attention)."),
    depth: str = typer.Option(
        "intermediate", 
        "--depth", 
        "-d", 
        help="Depth of explanation: beginner, intermediate, or advanced."
    )
) -> None:
    """Learn an ML/GenAI or engineering concept with an analogy, formal definition, code example, and usage scenarios."""
    user_prompt = (
        f"Teach the concept '{concept}' at a/an {depth} level.\n\n"
        f"Format your response in Markdown using the following structure:\n"
        f"1. **Analogy**: Provide an intuitive real-world analogy.\n"
        f"2. **Definition**: Provide a technically precise definition.\n"
        f"3. **Code Example**: Provide a clean, commented Python example demonstrating the concept.\n"
        f"4. **When to Use**: Describe common use cases and scenarios for this concept."
    )

    stream = generate_stream(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
    stream_output_panel(stream, title=f"Learning: {concept} ({depth})")
