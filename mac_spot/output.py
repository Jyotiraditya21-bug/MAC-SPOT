from typing import Generator
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.syntax import Syntax

# Configure custom styles mapping to the spec's color scheme
theme = Theme({
    "primary": "cyan",
    "success": "green",
    "warning": "yellow",
    "error": "red",
    "muted": "dim white"
})

console = Console(theme=theme)

def print_success(message: str) -> None:
    """Print a success message styled with the green accent."""
    console.print(f"[success]✔ {message}[/success]")

def print_warning(message: str) -> None:
    """Print a warning message styled with the yellow accent."""
    console.print(f"[warning]⚠ {message}[/warning]")

def print_error(message: str) -> None:
    """Print an error message styled with the red accent."""
    console.print(f"[error]✖ {message}[/error]")

def print_muted(message: str) -> None:
    """Print a muted/dim message."""
    console.print(f"[muted]{message}[/muted]")

def print_panel(content: str, title: str, style: str = "primary") -> None:
    """Render and print static markdown content wrapped in a styled Panel."""
    panel = Panel(
        Markdown(content),
        title=f"[{style}]{title}[/{style}]",
        border_style=style,
        title_align="left"
    )
    console.print(panel)

def print_code_panel(code: str, language: str, title: str, style: str = "primary") -> None:
    """Render and print a syntax-highlighted code block wrapped in a Panel."""
    syntax = Syntax(code, language, theme="monokai", line_numbers=True, word_wrap=True)
    panel = Panel(
        syntax,
        title=f"[{style}]{title}[/{style}]",
        border_style=style,
        title_align="left"
    )
    console.print(panel)

def stream_output_panel(generator: Generator[str, None, None], title: str, style: str = "primary") -> str:
    """Starts by showing a spinner, then captures chunks from the generator,
    dynamically rendering live Markdown updates inside a Panel.
    
    Returns:
        The full accumulated string from the generator.
    """
    full_text = ""
    try:
        # Display thinking spinner until the first chunk is received
        with console.status(f"[{style}]Thinking...[/{style}]"):
            try:
                first_chunk = next(generator)
                full_text += first_chunk
            except StopIteration:
                # Handle case where generator is completely empty
                print_panel("", title, style=style)
                return ""

        # Set up Live updating panel
        panel = Panel(
            Markdown(full_text),
            title=f"[{style}]{title}[/{style}]",
            border_style=style,
            title_align="left"
        )
        
        with Live(panel, console=console, refresh_per_second=10) as live:
            for chunk in generator:
                full_text += chunk
                live.update(
                    Panel(
                        Markdown(full_text),
                        title=f"[{style}]{title}[/{style}]",
                        border_style=style,
                        title_align="left"
                    )
                )
    except Exception as e:
        print_error(f"Error during execution: {str(e)}")
        raise e

    return full_text
