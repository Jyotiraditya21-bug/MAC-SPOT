# MAC-SPOT: CLI Commands Reference Guide

This document lists all the available commands, descriptions, arguments, options, and example usage for `mac-spot`.

---

## 🛠️ General Commands

### 1. `setup`
Configure your Google Gemini API key securely.
* **Usage**: `mac-spot setup`
* **Details**: Prompts you for your API key and saves it to `~/.mac-spot/api_key` with secure permissions (`chmod 600`).

### 2. `about` | `owner` | `builder`
Displays details about the builder and owner of MAC-SPOT.
* **Usage**: `mac-spot about` (or `mac-spot owner`, `mac-spot builder`)
* **Output Example**: `🛠️  Built by Jyotiraditya (GitHub: @Jyotiraditya21-bug) | Powered by Google Gemini`

---

## 🤖 Core AI/ML Developer Utilities

### 3. `explain`
Analyzes compilation errors, runtime exceptions, or stack traces and outputs root causes and fixes.
* **Usage**: `mac-spot explain [ERROR_MESSAGE_OR_LOG]`
* **Options**:
  * `--file` / `-f`: Path to a log file to explain.
  * `--lang` / `-l`: Target programming language context.
* **Examples**:
  ```bash
  mac-spot explain "ValueError: Found array with 0 sample(s)"
  mac-spot explain --file runtime.log --lang python
  ```

### 4. `review`
Conducts comprehensive code reviews focusing on bugs, security, performance, or styling.
* **Usage**: `mac-spot review [FILE_PATH]`
* **Options**:
  * `--focus` / `-f`: Review focus. Options: `bugs`, `performance`, `style`, `security`, `all` (default: `bugs`).
* **Example**:
  ```bash
  mac-spot review src/main.py --focus performance
  ```

### 5. `learn`
Teaches complex programming, systems, or ML concepts using analogies, definitions, and runnable code examples.
* **Usage**: `mac-spot learn [CONCEPT]`
* **Options**:
  * `--depth` / `-d`: Detail depth. Options: `beginner`, `intermediate`, `advanced` (default: `intermediate`).
* **Example**:
  ```bash
  mac-spot learn "Transformer Attention Mechanism" --depth advanced
  ```

### 6. `gen`
Generates clean, production-ready code snippets from natural language prompts.
* **Usage**: `mac-spot gen [PROMPT]`
* **Options**:
  * `--lang` / `-l`: Target programming language (default: `python`).
  * `--copy` / `-c`: Auto-copy the generated code block to the clipboard.
* **Example**:
  ```bash
  mac-spot gen "FastAPI route for uploading files to S3" --lang python --copy
  ```

### 7. `chat`
Initiates an interactive terminal-based chat session (REPL) with persistent memory.
* **Usage**: `mac-spot chat`
* **REPL Slash Commands**:
  * `/copy`: Copy the last reply to your clipboard.
  * `/clear`: Reset the chat history memory.
  * `/exit`: Terminate the chat session.

### 8. `git`
Generates conventional commit messages, pull request descriptions, or explains active git diffs.
* **Usage**: `mac-spot git [OPTIONS]`
* **Options**:
  * `--commit` / `-c`: Generate conventional commit message from staged changes.
  * `--pr` / `-p`: Generate a markdown PR description compared to main/master.
  * `--diff` / `-d`: Explain current git differences in plain English.
* **Example**:
  ```bash
  mac-spot git --commit
  ```

### 9. `sheet`
Generates dynamic, structured developer cheatsheets for popular libraries, tools, and databases.
* **Usage**: `mac-spot sheet [LIBRARY_OR_TOOL]`
* **Example**:
  ```bash
  mac-spot sheet pandas
  ```

---

## ⚡ Platform-Specific & Terminal Power Utilities

### 10. `mac`
Hardware-aware system optimizer. Profiles local specs to output optimization guidelines and suggest compatible local model sizes.
* **Platform Support**: macOS and Linux only (Windows is blocked with a friendly "upgrade to mac :)" message).
* **Usage**: `mac-spot mac [TOPIC] [OPTIONS]`
* **Arguments/Options**:
  * `[TOPIC]`: Optional framework to optimize (e.g. `mlx`, `pytorch`, `llama.cpp`, `ollama`).
  * `--model` / `-m`: Optional local model name to check hardware compatibility (e.g. `llama-3-8b`).
* **Example**:
  ```bash
  # Generate general optimization dashboard & compatible models:
  mac-spot mac
  
  # Check if a model fits your memory limits:
  mac-spot mac --model phi-4
  ```

### 11. `pipe`
Shell Pipeline Debugger and Explainer. Analyzes, debugs, and visualizes complex Unix command pipeline logic.
* **Platform Support**: Unix systems (macOS and Linux).
* **Usage**: `mac-spot pipe "[PIPELINE_STRING]"`
* **Example**:
  ```bash
  mac-spot pipe "find . -name '*.py' | xargs grep 'TODO' | wc -l"
  ```
