import subprocess
from typing import Optional
import typer

from mac_spot.gemini_client import generate_stream, SYSTEM_PROMPT
from mac_spot.output import stream_output_panel

def get_sysctl_value(param: str) -> str:
    """Run sysctl to read hardware specs from macOS kernel."""
    try:
        res = subprocess.run(["sysctl", "-n", param], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return "Unknown"

def get_macos_version() -> str:
    """Run sw_vers to read the macOS system version."""
    try:
        res = subprocess.run(["sw_vers", "-productVersion"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return "Unknown"

def mac_command(
    topic: Optional[str] = typer.Argument(
        None, 
        help="Optional framework to optimize (e.g., mlx, pytorch, llama.cpp, ollama)."
    ),
    model: Optional[str] = typer.Option(
        None, 
        "--model", 
        "-m", 
        help="Optional local LLM/VLM name to assess (e.g., llama-3-8b, phi-4, qwen-2.5-7b)."
    )
) -> None:
    """Hardware-aware macOS optimizer: analyzes your Apple Silicon specs to output quant, thread, and memory guidelines."""
    # 1. Profile host machine
    chip = get_sysctl_value("machdep.cpu.brand_string")
    mem_bytes = get_sysctl_value("hw.memsize")
    cores = get_sysctl_value("hw.ncpu")
    os_ver = get_macos_version()
    
    try:
        mem_gb = int(mem_bytes) // (1024 ** 3)
    except ValueError:
        mem_gb = "Unknown"

    hardware_profile = (
        f"Hardware Profile:\n"
        f"- Processor: {chip}\n"
        f"- Unified Memory: {mem_gb} GB RAM\n"
        f"- CPU Cores: {cores}\n"
        f"- OS: macOS {os_ver}\n"
    )

    if model:
        title = f"Local Sizing Profile: {model}"
        user_prompt = (
            f"Analyze if the local model '{model}' can be run on my machine given this hardware profile:\n"
            f"{hardware_profile}\n\n"
            f"Provide your analysis in Markdown containing:\n"
            f"1. **Quantization Sizing Table**: Show RAM requirements for FP16, Q8_0, Q4_K_M (or similar) quantizations.\n"
            f"2. **Fit Assessment**: Detail if it fits comfortably within my {mem_gb} GB Unified Memory, keeping in mind system overhead.\n"
            f"3. **Recommended Engine & Config**: Give optimal commands for Ollama, llama.cpp, or MLX, and specify the exact thread count `-t` matching my {cores} cores (to avoid utilizing efficiency cores unnecessarily).\n"
            f"4. **Performance Outlook**: Expected speeds and performance expectations."
        )
    elif topic:
        title = f"macOS Optimization: {topic}"
        user_prompt = (
            f"Provide advanced macOS-specific optimization instructions for '{topic}' given this hardware profile:\n"
            f"{hardware_profile}\n\n"
            f"Provide your advice in Markdown containing:\n"
            f"1. **Unified Memory & Metal Shaders Optimization**: How to leverage Metal GPU acceleration (MPS) or unified memory configurations.\n"
            f"2. **Optimal Compilation/Build Instructions**: Exact command lines, flags, or configuration variables.\n"
            f"3. **macOS Gotchas**: Core pitfalls (e.g. thrashing, thermal throttling, allocation limits) and fixes."
        )
    else:
        title = "macOS Apple Silicon AI Dashboard"
        user_prompt = (
            f"Generate a customized local AI/ML optimization dashboard based on my hardware profile:\n"
            f"{hardware_profile}\n\n"
            f"Structure your response in Markdown with the following sections:\n"
            f"1. **Hardware Capability Analysis**: Critique my {chip} + {mem_gb} GB Unified Memory for hosting model weights and training.\n"
            f"2. **PyTorch MPS Configuration**: Python snippets to configure and test PyTorch Metal Performance Shaders backend.\n"
            f"3. **Apple MLX Setup**: Code examples showing how to run MLX natively.\n"
            f"4. **Llama.cpp Compilation**: Build steps targeting Metal and optimal `-t` thread allocation for {cores} CPU cores.\n"
            f"5. **Environment Controls**: Essential environment variables (e.g., `PYTORCH_ENABLE_MPS_FALLBACK`, `GGML_METAL_PATH_RESOURCES`) to prevent context overflows."
        )

    stream = generate_stream(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
    stream_output_panel(stream, title=title)
