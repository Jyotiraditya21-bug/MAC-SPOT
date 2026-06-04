document.addEventListener("DOMContentLoaded", () => {
    // --- 1. Menu Bar Clock ---
    const timeDisplay = document.getElementById("time-display");
    const updateClock = () => {
        const now = new Date();
        const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        const day = days[now.getDay()];
        let hours = now.getHours();
        let minutes = now.getMinutes();
        const ampm = hours >= 12 ? "PM" : "AM";
        
        hours = hours % 12;
        hours = hours ? hours : 12; // Handle 0 as 12
        minutes = minutes < 10 ? "0" + minutes : minutes;
        
        timeDisplay.innerText = `${day} ${hours}:${minutes} ${ampm}`;
    };
    setInterval(updateClock, 1000);
    updateClock();

    // --- 2. Apple Dropdown Menu Toggle ---
    const appleBtn = document.getElementById("apple-logo-btn");
    const appleDropdown = document.getElementById("apple-dropdown");

    appleBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        appleDropdown.style.display = appleDropdown.style.display === "flex" ? "none" : "flex";
    });

    document.addEventListener("click", () => {
        appleDropdown.style.display = "none";
    });

    // --- 3. Install Command Tabs & Clipboard Copy ---
    const tabMacos = document.getElementById("tab-macos");
    const tabWindows = document.getElementById("tab-windows");
    const installCmdEl = document.getElementById("install-cmd");
    const copyBtn = document.getElementById("copy-btn");
    const tooltip = copyBtn.querySelector(".tooltip");
    const installNote = document.querySelector(".install-note");

    const MACOS_CMD = "curl -sL https://tinyurl.com/289km8xg | bash";
    const WINDOWS_CMD = "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/Jyotiraditya21-bug/MAC-SPOT/main/install.ps1'))";

    tabMacos.addEventListener("click", () => {
        tabMacos.classList.add("active");
        tabWindows.classList.remove("active");
        installCmdEl.innerText = MACOS_CMD;
        installNote.innerText = "Runs globally in Zsh/Bash. Configures short aliases automatically.";
    });

    tabWindows.addEventListener("click", () => {
        tabWindows.classList.add("active");
        tabMacos.classList.remove("active");
        installCmdEl.innerText = WINDOWS_CMD;
        installNote.innerText = "Runs in PowerShell. Registers global functions in your profile.";
    });

    copyBtn.addEventListener("click", () => {
        const textToCopy = installCmdEl.innerText;
        navigator.clipboard.writeText(textToCopy).then(() => {
            tooltip.innerText = "Copied!";
            setTimeout(() => {
                tooltip.innerText = "Copy to Clipboard";
            }, 2000);
        }).catch(err => {
            console.error("Could not copy link: ", err);
        });
    });

    // --- 4. macOS Window Dragging ---
    const makeWindowDraggable = (windowEl, headerEl) => {
        let startX = 0, startY = 0, currentX = 0, currentY = 0;

        headerEl.addEventListener("mousedown", (e) => {
            if (e.target.classList.contains("win-btn")) return;
            e.preventDefault();
            startX = e.clientX;
            startY = e.clientY;

            const dragMove = (moveEvent) => {
                currentX = startX - moveEvent.clientX;
                currentY = startY - moveEvent.clientY;
                startX = moveEvent.clientX;
                startY = moveEvent.clientY;

                windowEl.style.top = `${windowEl.offsetTop - currentY}px`;
                windowEl.style.left = `${windowEl.offsetLeft - currentX}px`;
            };

            const dragEnd = () => {
                document.removeEventListener("mousemove", dragMove);
                document.removeEventListener("mouseup", dragEnd);
            };

            document.addEventListener("mousemove", dragMove);
            document.addEventListener("mouseup", dragEnd);

            // Bring active window to focus depth
            document.querySelectorAll(".mac-window").forEach(w => w.style.zIndex = 10);
            windowEl.style.zIndex = 100;
        });
    };

    makeWindowDraggable(document.getElementById("about-window"), document.getElementById("about-header"));
    makeWindowDraggable(document.getElementById("terminal-window"), document.getElementById("terminal-header"));

    // --- 5. About Window Dialog Triggers ---
    const aboutWindow = document.getElementById("about-window");
    const aboutCloseBtn = document.getElementById("about-close-btn");
    const aboutTrigger = document.getElementById("about-trigger");
    const dockAboutTrigger = document.getElementById("dock-about-trigger");
    const aboutIndicator = document.getElementById("about-indicator");

    const openAboutWindow = () => {
        // Trigger bounce animation on Dock icon
        dockAboutTrigger.classList.add("bounce");
        setTimeout(() => {
            dockAboutTrigger.classList.remove("bounce");
            aboutWindow.style.display = "block";
            aboutWindow.style.top = "120px";
            aboutWindow.style.left = "100px";
            aboutIndicator.classList.add("active");
            aboutWindow.style.zIndex = 100;
        }, 900);
    };

    aboutTrigger.addEventListener("click", openAboutWindow);
    dockAboutTrigger.addEventListener("click", () => {
        if (aboutWindow.style.display === "none") {
            openAboutWindow();
        } else {
            aboutWindow.style.display = "none";
            aboutIndicator.classList.remove("active");
        }
    });

    aboutCloseBtn.addEventListener("click", () => {
        aboutWindow.style.display = "none";
        aboutIndicator.classList.remove("active");
    });

    // --- 6. Terminal Window Hide/Show simulation ---
    const termWindow = document.getElementById("terminal-window");
    const termCloseBtn = document.getElementById("term-close-btn");
    const dockTermTrigger = document.getElementById("dock-term-trigger");
    const termIndicator = document.getElementById("term-indicator");

    termCloseBtn.addEventListener("click", (e) => {
        e.preventDefault();
        termWindow.style.display = "none";
        termIndicator.classList.remove("active");
    });

    dockTermTrigger.addEventListener("click", (e) => {
        if (termWindow.style.display === "none") {
            e.preventDefault();
            dockTermTrigger.classList.add("bounce");
            setTimeout(() => {
                dockTermTrigger.classList.remove("bounce");
                termWindow.style.display = "flex";
                termIndicator.classList.add("active");
                // Smooth scroll to Try section
                document.getElementById("try").scrollIntoView({ behavior: "smooth" });
            }, 900);
        }
    });

    // --- 7. macOS Dock Mathematical Magnification ---
    const dock = document.getElementById("macos-dock");
    const dockItems = document.querySelectorAll("#macos-dock .dock-item");

    dock.addEventListener("mousemove", (e) => {
        const mouseX = e.clientX;
        dockItems.forEach(item => {
            const rect = item.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const dist = Math.abs(mouseX - centerX);
            
            const maxDist = 180; // Distance of magnification effect
            let scale = 1.0;
            if (dist < maxDist) {
                scale = 1.0 + (1.0 - dist / maxDist) * 0.45; // Smooth curve peaking at 1.45x
            }
            
            item.style.width = `${48 * scale}px`;
            item.style.height = `${48 * scale}px`;
        });
    });

    dock.addEventListener("mouseleave", () => {
        dockItems.forEach(item => {
            item.style.width = "48px";
            item.style.height = "48px";
        });
    });

    // --- 8. Terminal Command Simulator logic ---
    const termBody = document.getElementById("terminal-body");
    const cmdButtons = document.querySelectorAll(".cmd-btn");

    const RESPONSES = {
        help: `
  ███╗   ███╗ █████╗  ██████╗      ███████╗██████╗  ██████╗ ████████╗
  ████╗ ████║██╔══██╗██╔════╝      ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
  ██╔████╔██║███████║██║     █████╗███████╗██████╔╝██║   ██║   ██║
  ██║╚██╔╝██║██╔══██║██║     ╚════╝╚════██║██╔═══╝ ██║   ██║   ██║
  ██║ ╚═╝ ██║██║  ██║╚██████╗      ███████║██║     ╚██████╔╝   ██║
  ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝      ╚══════╝╚═╝      ╚═════╝    ╚═╝
  Your AI-powered dev assistant for macOS — powered by Gemini

 Usage: <span style="color: #06b6d4;">mac-spot</span> [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Show the version and exit.                   │
│ --help                -h        Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ setup    Prompt for and save your Gemini API key securely.                   │
│ explain  Explain a terminal/code error, its root cause, and how to fix it.   │
│ review   Analyze a code file and output suggested improvements, style.       │
│ learn    Learn an ML/GenAI concept with analogies & code examples.           │
│ gen      Generate production-ready, commented code block for a prompt.       │
│ chat     Start an interactive chat session with MAC-SPOT.                    │
│ git      Git tools: generate commits, PR descriptions, or explain diffs.     │
│ sheet    Generate structured cheatsheets for popular frameworks/tools.       │
│ mac      Hardware-aware macOS optimizer: analyzes Apple Silicon.             │
╰──────────────────────────────────────────────────────────────────────────────╯
`,
        mac: `
<div class="mock-panel">
  <div class="mock-panel-title">Local Sizing Profile: llama-3-8b</div>
  
  <strong>Hardware Profile:</strong>
  • Processor: Apple M1
  • Unified Memory: 8 GB RAM
  • CPU Cores: 8 (4 Performance, 4 Efficiency)
  • OS: macOS Sonoma
  
  -----------------------------------------------------------------------------
  
  <strong>1. Quantization Sizing Table:</strong>
  
  Format            Model File RAM    Total RAM Needed    Assessment
  <span style="color: #9ca3af;">─────────────────────────────────────────────────────────────────────────────</span>
  FP16 (Unquant)    ~16.0 GB          ~17.0 GB            ❌ Impossible
  Q8_0 (8-bit)      ~8.5 GB           ~9.5 GB             ❌ Impossible (Severe Swap)
  Q4_K_M (4-bit)    ~4.8 GB           ~5.8 GB             ⚠️ Marginal (Fits tight)
  Q3_K_M (3-bit)    ~4.0 GB           ~5.0 GB             Safe (Recommended)
  
  -----------------------------------------------------------------------------
  
  <strong>2. Fit Assessment: Marginal / Tight</strong>
  An 8 GB Apple Silicon system allocates ~2.5 GB to 3.0 GB for macOS system
  overhead, leaving only ~5.0 GB of free Unified Memory. 
  • Running <strong>Q4_K_M (4-bit)</strong> is tight. It will run, but you should close 
    other heavy apps (Chrome, Slack) to prevent severe thrashing.
  
  -----------------------------------------------------------------------------
  
  <strong>3. Recommended Engine & Config:</strong>
  Use <span style="color: #06b6d4;">llama.cpp</span> with Metal GPU acceleration. 
  
  <strong>Optimal Thread Selection:</strong>
  • Set thread count to <strong>-t 4</strong>.
  • <i>Reasoning:</i> Restricting threads to the 4 Performance (P) cores bypasses
    the slow efficiency E-cores, preventing thread sync lag and giving 15% better speed.
    
  <strong>Execution CLI Command:</strong>
  ./build/bin/llama-cli -m ./Meta-Llama-3-8B-Instruct-Q4_K_M.gguf -ngl 99 -t 4
</div>
`,
        learn: `
<div class="mock-panel">
  <div class="mock-panel-title">Learning Concept: Retrieval-Augmented Generation (RAG)</div>
  
  <strong>1. Analogy:</strong>
  Imagine you are sitting an exam. A standard LLM is like answering questions 
  solely from memory. RAG is like an "open-book" exam. When asked a question, 
  you first lookup relevant pages in a textbook (Retriever), read them, 
  and then write down a precise, factual answer based on that text (Generator).
  
  <strong>2. Definition:</strong>
  RAG is an architecture that optimizes the output of a Large Language Model by 
  querying an external, authoritative knowledge base (usually represented as vectors 
  in a Vector DB) before generating a response, ensuring up-to-date and non-hallucinated results.
  
  <strong>3. Code Example:</strong>
  <pre style="color: #a855f7; font-family: monospace; font-size: 0.8rem; margin: 8px 0; background: rgba(0,0,0,0.2); padding: 8px; border-radius: 4px;">
def run_rag_pipeline(user_query: str) -> str:
    # 1. Retrieve context
    context = vector_db.similarity_search(user_query, k=2)
    
    # 2. Augment prompt
    augmented_prompt = f"Context: {context}\\n\\nQuestion: {user_query}"
    
    # 3. Generate response
    return llm.generate(augmented_prompt)
  </pre>
</div>
`,
        git: `
<div class="mock-panel">
  <div class="mock-panel-title">Git Commit Generator</div>
  
  <strong>Staged Diff:</strong>
  - Modified: mac_spot/cli.py (registered 'mac' command)
  - Added: mac_spot/commands/mac.py (hardware profiling)
  
  <strong>Generated Conventional Commit Message:</strong>
  
  <span style="color: #06b6d4;">feat(cli): add 'mac' hardware-aware local optimizer subcommand</span>
  
  - Implemented sysctl queries to inspect chip, cores, and RAM size.
  - Resolved llama.cpp quantization limits based on host memory.
  - Linked new commands to 'spot mac' entrypoint.
</div>
`,
        chat: `
════════════════════════════════════════════════════════════
  MAC-SPOT Interactive Chat Session
  Commands:
    /copy  - Copy the last reply to the clipboard
    /clear - Clear conversation history
    /exit  - Exit the chat session
════════════════════════════════════════════════════════════

<span style="color: #10b981; font-weight: bold;">You:</span> hi
<span style="color: #06b6d4; font-weight: bold;">MAC-SPOT:</span> Hello! I am MAC-SPOT, your macOS GenAI development assistant.
I can help you optimize models for Apple Silicon, configure MPS
backends, compile llama.cpp, or build MLX local workflows.
What are we building today?
`
    };

    let isTyping = false;

    const runCommandSim = (cmdName) => {
        if (isTyping) return;
        isTyping = true;

        // Clear terminal screen
        termBody.innerHTML = "";

        // Construct command line elements
        const inputLine = document.createElement("div");
        inputLine.className = "terminal-input-line";
        
        const prompt = document.createElement("span");
        prompt.className = "terminal-prompt";
        prompt.innerText = "jimmycodes@MacBook-Air ~ % ";
        
        const cmdSpan = document.createElement("span");
        cmdSpan.style.color = "#f3f4f6";
        
        const cursor = document.createElement("span");
        cursor.className = "cursor";
        
        inputLine.appendChild(prompt);
        inputLine.appendChild(cmdSpan);
        inputLine.appendChild(cursor);
        termBody.appendChild(inputLine);

        // Command text
        const cmdMap = {
            help: "mac-spot --help",
            mac: "spot mac --model llama-3-8b",
            learn: "spot learn \"RAG\"",
            git: "spot git --commit",
            chat: "ms chat"
        };
        const cmdText = cmdMap[cmdName];
        let idx = 0;

        // Type command character by character
        const typingInterval = setInterval(() => {
            if (idx < cmdText.length) {
                cmdSpan.innerText += cmdText[idx];
                idx++;
            } else {
                clearInterval(typingInterval);
                cursor.remove(); // Remove blinking cursor from prompt
                
                // Show loader status
                const loader = document.createElement("div");
                loader.style.color = "#06b6d4";
                loader.style.marginTop = "8px";
                loader.innerText = "Thinking...";
                termBody.appendChild(loader);

                // Stream response in chunks
                setTimeout(() => {
                    loader.remove();
                    streamResponse(RESPONSES[cmdName]);
                }, 600);
            }
        }, 60);
    };

    const streamResponse = (fullHtml) => {
        const outputDiv = document.createElement("div");
        outputDiv.className = "terminal-output";
        termBody.appendChild(outputDiv);

        // Parse HTML into tags and text chunks for smooth streaming
        const regex = /(<[^>]*>|[^<]+)/g;
        const chunks = fullHtml.match(regex) || [];
        let chunkIdx = 0;

        const streamingInterval = setInterval(() => {
            if (chunkIdx < chunks.length) {
                outputDiv.innerHTML += chunks[chunkIdx];
                chunkIdx++;
                termBody.scrollTop = termBody.scrollHeight; // Auto-scroll
            } else {
                clearInterval(streamingInterval);
                isTyping = false;
                
                // Append fresh input prompt at the bottom
                const finalPromptLine = document.createElement("div");
                finalPromptLine.className = "terminal-input-line";
                finalPromptLine.innerHTML = `<span class="terminal-prompt">jimmycodes@MacBook-Air ~ % </span><span class="cursor"></span>`;
                termBody.appendChild(finalPromptLine);
                termBody.scrollTop = termBody.scrollHeight;
            }
        }, 30);
    };

    // Button event click handler
    cmdButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            if (isTyping) return;
            
            // Toggle active state
            cmdButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            
            const cmd = btn.getAttribute("data-cmd");
            runCommandSim(cmd);
        });
    });

    // Run first command (help) automatically on load
    runCommandSim("help");
});
