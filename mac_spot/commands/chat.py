import typer
import pyperclip
from rich.prompt import Prompt

from mac_spot.gemini_client import generate_stream
from mac_spot.output import console, stream_output_panel, print_success, print_warning

CHAT_SYSTEM_PROMPT = (
    "You are MAC-SPOT, an AI assistant for GenAI engineers and developers on macOS. "
    "Be concise, technical, and give code examples when relevant."
)

def chat_command() -> None:
    """Start an interactive chat session with MAC-SPOT."""
    console.print(
        "[bold primary]════════════════════════════════════════════════════════════[/bold primary]\n"
        "[bold primary]  MAC-SPOT Interactive Chat Session[/bold primary]\n"
        "  Commands:\n"
        "    [bold]/copy[/bold]  - Copy the last reply to the clipboard\n"
        "    [bold]/clear[/bold] - Clear conversation history\n"
        "    [bold]/exit[/bold]  - Exit the chat session\n"
        "[bold primary]════════════════════════════════════════════════════════════[/bold primary]\n"
    )

    history = []
    last_reply = ""

    while True:
        try:
            user_input = Prompt.ask("\n[bold success]You[/bold success]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[primary]Exiting chat session. Goodbye![/primary]")
            break

        if not user_input:
            continue

        if user_input == "/exit":
            console.print("[primary]Exiting chat session. Goodbye![/primary]")
            break

        elif user_input == "/clear":
            history.clear()
            last_reply = ""
            print_success("Conversation history cleared.")
            continue

        elif user_input == "/copy":
            if last_reply:
                try:
                    pyperclip.copy(last_reply)
                    print_success("Last assistant response copied to clipboard!")
                except Exception as e:
                    print_warning(f"Could not copy to clipboard: {e}")
            else:
                print_warning("No response to copy yet.")
            continue

        # Add user query to local memory
        history.append({"role": "user", "text": user_input})

        try:
            # Pass existing history (excluding current user prompt)
            stream = generate_stream(
                system_prompt=CHAT_SYSTEM_PROMPT,
                user_prompt=user_input,
                history=history[:-1]
            )
            reply = stream_output_panel(stream, title="MAC-SPOT")
            
            # Save assistant reply to memory
            history.append({"role": "assistant", "text": reply})
            last_reply = reply
        except Exception as e:
            # Remove the last user query since we failed to get a response
            history.pop()
            print_warning(f"Could not get response: {e}")
