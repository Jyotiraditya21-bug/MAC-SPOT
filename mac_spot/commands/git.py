import subprocess
from typing import List
import typer
import pyperclip
from rich.prompt import Confirm

from mac_spot.gemini_client import generate_stream, SYSTEM_PROMPT
from mac_spot.output import stream_output_panel, print_error, print_success, print_warning

def run_git_command(args: List[str]) -> str:
    """Helper to run shell git commands and return standard output."""
    try:
        res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        err_msg = e.stderr.strip() or e.stdout.strip()
        raise RuntimeError(err_msg)
    except FileNotFoundError:
        raise RuntimeError("git CLI command is not available in PATH.")

def git_command(
    commit: bool = typer.Option(False, "--commit", "-c", help="Generate conventional commit message from staged changes."),
    pr: bool = typer.Option(False, "--pr", "-p", help="Generate a PR description comparison against main/master."),
    diff: bool = typer.Option(False, "--diff", "-d", help="Explain the current git diff changes in plain English.")
) -> None:
    """Git tools: generate conventional commits, PR descriptions, or explain changes."""
    active_flags = [commit, pr, diff]
    if sum(active_flags) != 1:
        print_error("Please specify exactly one flag: --commit, --pr, or --diff.")
        raise typer.Exit(code=1)

    try:
        run_git_command(["git", "rev-parse", "--is-inside-work-tree"])
    except Exception as e:
        print_error(f"Failed to run git command. Ensure you are inside a git repository: {e}")
        raise typer.Exit(code=1)

    title = ""
    user_prompt = ""

    try:
        if commit:
            title = "Git Commit Generator"
            git_diff = run_git_command(["git", "diff", "--staged"])
            if not git_diff:
                print_error("No staged changes found. Please stage files using 'git add' first.")
                raise typer.Exit(code=1)
                
            user_prompt = (
                "Analyze the following git diff of staged changes and generate a conventional commit message.\n"
                "Format requirement:\n"
                "<type>(<scope>): <short description>\n\n"
                "[optional body detailing changes]\n"
                "Staged changes diff:\n"
                f"```diff\n{git_diff}\n```"
            )
        elif pr:
            title = "Git PR Description Generator"
            # Try three-dot merges, fallback to direct diffs
            git_diff = ""
            for base_branch in ["main", "master", "origin/main", "origin/master"]:
                try:
                    git_diff = run_git_command(["git", "diff", f"{base_branch}..."])
                    if git_diff:
                        break
                except Exception:
                    continue
            if not git_diff:
                for base_branch in ["main", "master", "origin/main", "origin/master"]:
                    try:
                        git_diff = run_git_command(["git", "diff", base_branch])
                        if git_diff:
                            break
                    except Exception:
                        continue
            if not git_diff:
                print_error("Could not find a valid base branch (main/master) to diff against.")
                raise typer.Exit(code=1)

            user_prompt = (
                "Generate a detailed Pull Request description based on the following diff compared to main/master.\n"
                "Format using Markdown with the following sections:\n"
                "- **Summary**: A high-level description of what this PR accomplishes.\n"
                "- **Changes**: A categorized list of specific file/component modifications.\n"
                "- **Testing**: Instructions detailing how this can be verified.\n\n"
                "Diff:\n"
                f"```diff\n{git_diff}\n```"
            )
        elif diff:
            title = "Git Diff Explainer"
            git_diff = run_git_command(["git", "diff"])
            if not git_diff:
                # If unstaged is empty, fall back to staged
                git_diff = run_git_command(["git", "diff", "--staged"])
            if not git_diff:
                print_error("No active changes (staged or unstaged) detected.")
                raise typer.Exit(code=1)

            user_prompt = (
                "Explain what the following git diff does in plain, concise English.\n"
                "Identify files changed, summarize modifications, and explain the engineering impact.\n\n"
                "Diff:\n"
                f"```diff\n{git_diff}\n```"
            )
    except Exception as e:
        print_error(f"Error inspecting git repository: {e}")
        raise typer.Exit(code=1)

    stream = generate_stream(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
    full_response = stream_output_panel(stream, title=title)

    try:
        if Confirm.ask("\n[bold primary]Copy generated text to clipboard?[/bold primary]"):
            pyperclip.copy(full_response)
            print_success("Text copied to clipboard successfully!")
    except Exception as e:
        print_warning(f"Could not access clipboard: {e}")
