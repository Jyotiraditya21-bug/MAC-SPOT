import warnings
warnings.filterwarnings("ignore")

from typing import Optional
import typer

from mac_spot import __version__, config
from mac_spot.output import console, print_success, print_error
from mac_spot.commands.explain import explain_command
from mac_spot.commands.review import review_command
from mac_spot.commands.learn import learn_command
from mac_spot.commands.gen import gen_command
from mac_spot.commands.chat import chat_command
from mac_spot.commands.git import git_command
from mac_spot.commands.sheet import sheet_command
from mac_spot.commands.mac import mac_command
from mac_spot.commands.pipe import pipe_command

BANNER = """\b
[cyan]
  ███╗   ███╗ █████╗  ██████╗      ███████╗██████╗  ██████╗ ████████╗
  ████╗ ████║██╔══██╗██╔════╝      ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
  ██╔████╔██║███████║██║     █████╗███████╗██████╔╝██║   ██║   ██║
  ██║╚██╔╝██║██╔══██║██║     ╚════╝╚════██║██╔═══╝ ██║   ██║   ██║
  ██║ ╚═╝ ██║██║  ██║╚██████╗      ███████║██║     ╚██████╔╝   ██║
  ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝      ╚══════╝╚═╝      ╚═════╝    ╚═╝[/cyan]
  Your AI-powered dev assistant for macOS — powered by Gemini
"""

app = typer.Typer(
    help="Your AI-powered dev assistant for macOS — powered by Gemini",
    rich_markup_mode="rich",
    no_args_is_help=False
)

@app.callback(invoke_without_command=True, context_settings={"help_option_names": []})
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(None, "--version", "-v", help="Show the version and exit."),
    help: Optional[bool] = typer.Option(None, "--help", "-h", help="Show this message and exit.")
) -> None:
    """Entry point check for version or help callback."""
    if version:
        console.print(BANNER)
        console.print(f"  Version: {__version__}\n")
        raise typer.Exit()
    
    if help or ctx.invoked_subcommand is None:
        console.print(BANNER)
        console.print(ctx.get_help())
        raise typer.Exit()

@app.command(name="setup")
def setup_command() -> None:
    """Prompt for and save your Gemini API key securely."""
    console.print("[bold primary]════════════════════════════════════════════════════════════[/bold primary]")
    console.print("  [bold primary]MAC-SPOT Setup Configuration[/bold primary]")
    console.print("[bold primary]════════════════════════════════════════════════════════════[/bold primary]\n")
    
    api_key = typer.prompt("Enter your Google Gemini API Key", hide_input=True).strip()
    if not api_key:
        print_error("Gemini API key cannot be empty.")
        raise typer.Exit(code=1)

    try:
        config.save_api_key(api_key)
        print_success("Gemini API key stored successfully at ~/.mac-spot/api_key with chmod 600.")
    except Exception as e:
        print_error(f"Failed to configure setup: {e}")
        raise typer.Exit(code=1)

def about_command() -> None:
    """Display builder and owner information for MAC-SPOT."""
    console.print("[cyan]🛠️  Built by [bold]Jyotiraditya[/bold] (GitHub: [bold]@Jyotiraditya21-bug[/bold]) | Powered by Google Gemini[/cyan]")

# Register command handlers from modular command files
app.command(name="explain")(explain_command)
app.command(name="review")(review_command)
app.command(name="learn")(learn_command)
app.command(name="gen")(gen_command)
app.command(name="chat")(chat_command)
app.command(name="git")(git_command)
app.command(name="sheet")(sheet_command)
app.command(name="mac")(mac_command)
app.command(name="pipe")(pipe_command)
app.command(name="about")(about_command)
app.command(name="owner")(about_command)
app.command(name="builder")(about_command)

if __name__ == "__main__":
    app()
