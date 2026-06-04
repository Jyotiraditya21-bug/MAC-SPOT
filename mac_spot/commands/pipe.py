import os
import platform
import typer

from mac_spot.gemini_client import generate_stream, SYSTEM_PROMPT
from mac_spot.output import stream_output_panel

def pipe_command(
    pipeline: str = typer.Argument(
        ..., 
        help="The shell pipeline to explain and debug (e.g. 'ps aux | grep python | awk \\'{print $2}\\'')."
    )
) -> None:
    """Shell Pipeline Debugger & Explainer: visualizes stdin/stdout data flows, highlights platform gotchas, and suggests optimizations."""
    # 1. Gather host environment facts
    os_name = platform.system()
    shell_path = os.environ.get("SHELL", "Unknown shell")
    shell_name = os.path.basename(shell_path) if shell_path else "Unknown"

    system_details = (
        f"- Operating System: {os_name}\n"
        f"- Target Shell: {shell_name} ({shell_path})\n"
    )

    # 2. Structure prompt for Gemini
    user_prompt = (
        f"You are analyzing the following Unix shell pipeline:\n\n"
        f"```bash\n"
        f"{pipeline}\n"
        f"```\n\n"
        f"Context details of the user's terminal environment:\n"
        f"{system_details}\n"
        f"Analyze this pipeline and output a detailed explanation in Markdown with the following sections:\n\n"
        f"### 🔗 Pipeline Data Flow\n"
        f"Draw a high-level text/ASCII diagram or visual sequence illustrating how data flows from command to command (stdin -> stdout).\n\n"
        f"### ⚙️ Command-by-Command Breakdown\n"
        f"Break down every command/filter in the pipeline, explaining:\n"
        f"- What the command and its flags do.\n"
        f"- What it consumes (stdin input shape/format).\n"
        f"- What it outputs (stdout format passed to the next pipe).\n\n"
        f"### ⚠️ Platform Gotchas & Shell Compatibility\n"
        f"Identify compatibility warnings or behavior differences between macOS (BSD-based utilities) and Linux (GNU-based utilities) for the tools in this pipeline (e.g., differences in `sed`, `awk`, `find`, `xargs`, `grep`, `stat`, or `date` flags). Let the user know if this pipeline will break or behave differently on one of the OSes.\n\n"
        f"### 🛡️ Safety & Side Effects\n"
        f"Alert the user if the pipeline contains destructive, writing, or system-state-altering actions (e.g. `rm`, `kill`, `killall`, `mv`, `>`, `>>`, `dd`, `curl | sh`). If it is a read-only pipeline, explicitly mark it as **[Safe / Read-Only]**.\n\n"
        f"### 💡 Optimized or Alternative Approach\n"
        f"Suggest a simpler, modern, or more portable command/pipeline that achieves the exact same goal (e.g., using `pgrep`/`pkill` instead of `ps aux | grep`, using built-in flags, or avoiding unnecessary processes like 'Useless Use of Cat'). Provide the alternative command and why it is better."
    )

    title = f"Pipeline Analysis: {pipeline}"
    stream = generate_stream(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
    stream_output_panel(stream, title=title)
