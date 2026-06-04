# MAC-SPOT

Your AI-powered developer assistant in the terminal — powered by Gemini. Designed specifically for GenAI/ML engineers and developers on macOS.

🌐 **Website & Simulator**: [jyotiraditya21-bug.github.io/MAC-SPOT](https://jyotiraditya21-bug.github.io/MAC-SPOT/)

---

```
  ███╗   ███╗ █████╗  ██████╗      ███████╗██████╗  ██████╗ ████████╗
  ████╗ ████║██╔══██╗██╔════╝      ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
  ██╔████╔██║███████║██║     █████╗███████╗██████╔╝██║   ██║   ██║
  ██║╚██╔╝██║██╔══██║██║     ╚════╝╚════██║██╔═══╝ ██║   ██║   ██║
  ██║ ╚═╝ ██║██║  ██║╚██████╗      ███████║██║     ╚██████╔╝   ██║
  ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝      ╚══════╝╚═╝      ╚═════╝    ╚═╝
  Your AI-powered dev assistant for macOS — powered by Gemini
```

---

## Features

- **setup**: Configures your Gemini API key securely.
- **explain**: Analyzes errors or log files and outputs explanations, causes, and fixes.
- **review**: Conducts comprehensive code reviews focusing on bugs, performance, style, or security.
- **learn**: Teaches complex programming or ML concepts (RAG, attention mechanisms, fine-tuning) using analogies, definitions, and runnable code examples.
- **gen**: Generates clean, production-ready code snippets from natural language prompts.
- **chat**: Initiates an interactive terminal-based chat session (REPL) with persistent history and system instruction overrides.
- **git**: Generates conventional commit messages, PR descriptions, or explains complex git changes from staged/unstaged changes.
- **sheet**: Generates dynamic, structured cheatsheets for popular libraries and tools.
- **mac**: Hardware-aware local optimizer. Automatically profiles your Apple Silicon chip, unified memory size, and CPU cores to generate memory sizing predictions (quantization fitting), run configs, and compilation guides.
- **pipe**: Shell Pipeline Debugger & Explainer. Visualizes stdin/stdout data flows, alerts about safety/side effects, highlights macOS vs. Linux command compatibility gotchas, and recommends optimizations.

---

## Installation & Setup

You can install `mac-spot` globally on any Mac with a single command:

```bash
curl -sSL https://raw.githubusercontent.com/Jyotiraditya21-bug/MAC-SPOT/main/install.sh | bash
```

Once the installation finishes, reload your terminal profile and configure your API key:

```bash
source ~/.zshrc
mac-spot setup
```

---

## Commands & Usage

### 1. Setup API Key
```bash
mac-spot setup
```

### 2. Explain Errors
Explain an error message directly:
```bash
mac-spot explain "ValueError: Found array with 0 sample(s) (shape=(0, 10)) while a minimum of 1 is required."
```
Explain an error log from a file with a language context:
```bash
mac-spot explain --file logs.txt --lang python
```

### 3. Review Code
Perform a style review on a file:
```bash
mac-spot review path/to/file.py --focus style
```
Review options for `--focus`: `bugs` (default), `performance`, `style`, `security`, `all`.

### 4. Learn Concepts
Learn about transformers or agent frameworks at a beginner or advanced level:
```bash
mac-spot learn "Transformer Attention Mechanism" --depth advanced
```
Review options for `--depth`: `beginner`, `intermediate` (default), `advanced`.

### 5. Generate Code
Generate code and copy it automatically to your clipboard:
```bash
mac-spot gen "FastAPI route for uploading files to S3 with progress tracking" --lang python --copy
```

### 6. Interactive Chat (REPL)
Start a chat session:
```bash
mac-spot chat
```
Within the REPL loop, you can use:
- `/copy`: Copy the last reply to your clipboard.
- `/clear`: Clear conversation memory.
- `/exit`: Exit chat.

### 7. Git Assistant
Generate a conventional commit message from staged changes:
```bash
mac-spot git --commit
```
Generate a markdown PR description compared to main/master branch:
```bash
mac-spot git --pr
```
Explain the current git diff in plain English:
```bash
mac-spot git --diff
```
*(All git commands offer a prompt to copy the output to your clipboard).*

### 8. Dynamic Cheatsheets
Fetch a structured cheatsheet for popular tools:
```bash
mac-spot sheet langchain
```
### 9. macOS Apple Silicon Optimizer
Automatically profile your local specs (processor, RAM size, cores) to output a customized AI/ML setup dashboard:
```bash
mac-spot mac
```
Analyze if a model fits in your Unified Memory (calculating RAM sizes for FP16/Q8/Q4 quantizations) and obtain optimal thread count allocations:
```bash
mac-spot mac --model llama-3-8b
```
Generate custom compilation and MPS (Metal Performance Shaders) execution flags for a framework:
```bash
mac-spot mac mlx
```

### 10. Shell Pipeline Debugger & Explainer
Analyze, debug, and visualize complex Unix shell pipelines (specifically detecting macOS/BSD vs. Linux/GNU tool mismatches):
```bash
mac-spot pipe "ps aux | grep python | awk '{print \$2}' | xargs kill -9"
```

---

## Model Selection

By default, MAC-SPOT uses the fast and capable `gemini-1.5-flash` model. You can override the model selection by setting the environment variable `MAC_SPOT_MODEL`:

```bash
export MAC_SPOT_MODEL=gemini-1.5-pro
```
