# MAC-SPOT: Project Workflow & Architecture

This document describes the design architecture, core data flow, libraries, and system tools utilized by MAC-SPOT.

---

## 🏗️ Core Architecture & Data Flow

When a user runs a command in their terminal, MAC-SPOT processes it through several layers:

1. **Typer CLI Layer**: Parses user command-line arguments, options, and flags.
2. **Configuration & Security Check**: Validates the presence of the Gemini API Key from environment variables or the secure credentials file (`~/.mac-spot/api_key`).
3. **Environment/Platform Profiling**: Queries host OS specifications (macOS/Darwin vs. Linux vs. Windows).
   - If Windows is detected, the program terminates immediately with `"upgrade to mac :)"`.
   - On macOS/Linux, it reads CPU Brand, Cores, Memory, and Active Shell details.
4. **Gemini Integration Client**: Injects a structured developer system prompt, constructs the query, and transmits a streaming request to Gemini.
5. **Rich Live Streamer**: Captures response chunks in real-time and dynamically updates a styled Rich Markdown panel in the terminal window.

### 📊 System Workflow Diagram

```mermaid
graph TD
    User([Terminal User]) -->|Runs Command| CLI[cli.py: Typer App]
    
    %% Config & OS Checks
    CLI -->|1. Validate API Key| Config[config.py]
    Config -->|Reads Key| KeyStore[~/.mac-spot/api_key or GEMINI_API_KEY]
    
    CLI -->|2. Check OS| OSCheck{Platform System?}
    OSCheck -->|Windows| WinErr[Print 'upgrade to mac :)' & Exit]
    OSCheck -->|macOS / Linux| ExecCmd[Load Target Command Module]
    
    %% Command Module Execution
    subgraph Commands [Command Handlers]
        ExecCmd -->|mac-spot mac| MacCmd[mac.py: Hardware Profiler]
        ExecCmd -->|mac-spot pipe| PipeCmd[pipe.py: Pipeline Analyzer]
        ExecCmd -->|Others explain/gen/git/etc| OtherCmd[Other Command Modules]
    end
    
    %% System Queries
    MacCmd -->|Read Specs| macOSQuery[macOS: sysctl / sw_vers]
    MacCmd -->|Read Specs| LinuxQuery[Linux: /proc/cpuinfo / /proc/meminfo / os-release]
    PipeCmd -->|Read Env| EnvQuery[Query platform.system / $SHELL]
    
    %% Gemini Communication
    MacCmd & PipeCmd & OtherCmd -->|Construct Prompts| GemClient[gemini_client.py: generate_stream]
    GemClient -->|HTTP Stream| GeminiAPI[Google Gemini API]
    
    %% Output Rendering
    GeminiAPI -->|Text Chunks| Output[output.py: stream_output_panel]
    Output -->|Live Rich Panel| User
```

---

## 📚 Libraries Used

MAC-SPOT is built with lightweight, premium python dependencies:

| Library | Version | Purpose |
| :--- | :--- | :--- |
| **`google-generativeai`** | `>=0.5.0` | The official SDK for communicating with the Gemini API to generate text streams. |
| **`typer`** | `>=0.12.0` | CLI building library powered by Type hints. Provides robust argument parsing, autocomplete, and help layouts. |
| **`rich`** | `>=13.0.0` | Renders styled text, tables, syntax-highlighted code panels, spinners, and live terminal updates. |
| **`pyperclip`** | `>=1.8.0` | Interacts with the system clipboard to copy generated code blocks or git commit messages. |
| **`setuptools`** | - | Handles package builds, dependency installation, and mapping the CLI entrypoint. |

---

## 🛠️ System Tools & Low-Level API Queries

To operate without high-level external dependencies, MAC-SPOT queries native system files and kernel utilities:

### macOS/Darwin Utilities
- **`sysctl`**: Consults the macOS kernel for hardware details:
  - `machdep.cpu.brand_string`: Reads the chip description (e.g. `Apple M1`).
  - `hw.memsize`: Retrieves the total Unified Memory size in bytes.
  - `hw.ncpu`: Retrieves the total CPU core count.
- **`sw_vers`**: Retrieves the macOS system product version.

### Linux Utilities & File Enclaves
- **`/proc/cpuinfo`**: Read to extract the CPU model and brand details.
- **`/proc/meminfo` & `os.sysconf`**: Read to discover system RAM capacity (`MemTotal` / `SC_PHYS_PAGES` * `SC_PAGE_SIZE`).
- **`/etc/os-release`**: Inspected to retrieve the specific Linux distribution name (e.g. `Ubuntu 22.04 LTS`).
- **`os.cpu_count()`**: Utilized to get active core counts.
- **`os.environ.get("SHELL")`**: Utilized to discover the user's active shell terminal emulator (`zsh`, `bash`, `fish`, etc.).
