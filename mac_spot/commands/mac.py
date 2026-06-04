import os
import platform
import subprocess
from typing import Optional
import typer

from mac_spot.gemini_client import generate_stream, SYSTEM_PROMPT
from mac_spot.output import stream_output_panel, print_error

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

def get_linux_cpu_info() -> str:
    """Read CPU model name from /proc/cpuinfo."""
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return "Unknown Linux CPU"

def get_linux_memory() -> int:
    """Read total memory size in bytes from /proc/meminfo or os.sysconf."""
    try:
        pages = os.sysconf('SC_PHYS_PAGES')
        page_size = os.sysconf('SC_PAGE_SIZE')
        if pages > 0 and page_size > 0:
            return pages * page_size
    except Exception:
        pass
    
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if "MemTotal" in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        return int(parts[1]) * 1024
    except Exception:
        pass
    return 0

def get_linux_distro() -> str:
    """Read Linux distribution name from /etc/os-release."""
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    return line.split("=", 1)[1].strip().strip('"')
    except Exception:
        pass
    return f"Linux {platform.release()}"

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
    """Hardware-aware OS optimizer: analyzes your specs to output model compatibility, quant, thread, and memory guidelines."""
    # 1. Check OS and block Windows
    system = platform.system()
    if system == "Windows":
        print_error("upgrade to mac :)")
        raise typer.Exit(code=1)
    
    if system not in ("Darwin", "Linux"):
        print_error(f"Unsupported OS: {system}")
        raise typer.Exit(code=1)

    # 2. Profile host machine based on OS
    if system == "Darwin":
        chip = get_sysctl_value("machdep.cpu.brand_string")
        mem_bytes = get_sysctl_value("hw.memsize")
        cores = get_sysctl_value("hw.ncpu")
        os_ver = f"macOS {get_macos_version()}"
        try:
            mem_gb = int(mem_bytes) // (1024 ** 3)
        except ValueError:
            mem_gb = "Unknown"
    else:  # Linux
        chip = get_linux_cpu_info()
        mem_bytes = get_linux_memory()
        cores = os.cpu_count() or "Unknown"
        os_ver = get_linux_distro()
        try:
            mem_gb = int(mem_bytes) // (1024 ** 3) if mem_bytes > 0 else "Unknown"
        except Exception:
            mem_gb = "Unknown"

    hardware_profile = (
        f"Hardware Profile:\n"
        f"- Operating System: {os_ver}\n"
        f"- Processor: {chip}\n"
        f"- Memory: {mem_gb} GB RAM\n"
        f"- CPU Cores: {cores}\n"
    )

    if model:
        title = f"Local Sizing Profile: {model}"
        user_prompt = (
            f"Analyze if the local model '{model}' can be run on my machine given this hardware profile:\n"
            f"{hardware_profile}\n\n"
            f"Provide your analysis in Markdown containing:\n"
            f"1. **Quantization Sizing Table**: Show RAM requirements for FP16, Q8_0, Q4_K_M (or similar) quantizations.\n"
            f"2. **Fit Assessment**: Detail if it fits comfortably within my {mem_gb} GB memory, keeping in mind system overhead.\n"
            f"3. **Recommended Engine & Config**: Give optimal commands for Ollama, llama.cpp, or MLX (macOS only), and specify the exact thread count matching my {cores} cores.\n"
            f"4. **Performance Outlook**: Expected speeds and performance expectations on this platform."
        )
    elif topic:
        title = f"Hardware Optimization: {topic}"
        user_prompt = (
            f"Provide advanced hardware-specific optimization instructions for '{topic}' given this hardware profile:\n"
            f"{hardware_profile}\n\n"
            f"Provide your advice in Markdown containing:\n"
            f"1. **Hardware/Memory Acceleration**: How to leverage GPU acceleration (MPS/Metal for macOS, CUDA/ROCm for Linux) or memory configurations.\n"
            f"2. **Optimal Compilation/Build Instructions**: Exact command lines, flags, or configuration variables.\n"
            f"3. **Platform Gotchas**: Core pitfalls (e.g. thrashing, thermal throttling, allocation limits, OOM killer) and fixes."
        )
    else:
        title = f"{system} Local AI Optimization Dashboard"
        user_prompt = (
            f"Generate a customized local AI/ML optimization dashboard based on my hardware profile:\n"
            f"{hardware_profile}\n\n"
            f"Structure your response in Markdown with the following sections:\n"
            f"1. **Hardware Capability Analysis & Model Compatibility**: Critique my {chip} + {mem_gb} GB RAM for hosting model weights and training. "
            f"Explicitly list compatible local models (e.g., 1.5B, 3B, 8B, 14B, 32B, 70B, etc. at Q4/Q8/FP16) that fit comfortably within my system specs.\n"
            f"2. **PyTorch GPU Configuration**: Code snippets to configure and test GPU acceleration backend ({'Metal Performance Shaders (MPS)' if system == 'Darwin' else 'CUDA or ROCm'} depending on system type).\n"
            f"3. **Local Deployment Setup**: Code/terminal examples showing how to run native engines ({'Apple MLX / Ollama' if system == 'Darwin' else 'vLLM / Ollama'} depending on system type).\n"
            f"4. **Llama.cpp Compilation**: Build steps targeting GPU acceleration ({'Metal' if system == 'Darwin' else 'CUDA/ROCm'} depending on system type) and optimal `-t` thread allocation for {cores} CPU cores.\n"
            f"5. **Environment Controls**: Essential environment variables (e.g., {'`PYTORCH_ENABLE_MPS_FALLBACK`' if system == 'Darwin' else '`CUDA_VISIBLE_DEVICES` or ROCm variables'}) to prevent context overflows."
        )

    stream = generate_stream(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
    stream_output_panel(stream, title=title)
