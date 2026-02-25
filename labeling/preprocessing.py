"""
Preprocessing Module

Extracts structural signals from SFT conversations before LLM labeling.
These signals are embedded into the prompt to help the LLM focus on semantic
judgment rather than basic information extraction.

Signals extracted:
  - Language detection from code blocks
  - Tool role detection (agentic signals)
  - Code block count and content analysis
  - Turn count and conversation structure
  - Keyword-based hints
  - Token estimation
  - Last turn extraction
"""

import re
import json


# ─────────────────────────────────────────────────────────
# Language detection patterns
# ─────────────────────────────────────────────────────────

# Map of code fence language identifiers → taxonomy language tag IDs
FENCE_LANG_MAP = {
    "python": "python", "py": "python", "python3": "python",
    "javascript": "javascript", "js": "javascript",
    "typescript": "typescript", "ts": "typescript", "tsx": "typescript", "jsx": "javascript",
    "java": "java",
    "go": "go", "golang": "go",
    "rust": "rust", "rs": "rust",
    "c": "c", "h": "c",
    "cpp": "cpp", "c++": "cpp", "cxx": "cpp", "cc": "cpp", "hpp": "cpp",
    "csharp": "csharp", "cs": "csharp", "c#": "csharp",
    "ruby": "ruby", "rb": "ruby",
    "php": "php",
    "swift": "swift",
    "kotlin": "kotlin", "kt": "kotlin",
    "scala": "scala",
    "sql": "sql", "mysql": "sql", "postgresql": "sql", "postgres": "sql", "sqlite": "sql",
    "html": "html",
    "css": "css", "scss": "css", "sass": "css", "less": "css",
    "shell": "shell", "bash": "shell", "sh": "shell", "zsh": "shell",
    "dockerfile": "dockerfile", "docker": "dockerfile",
    "yaml": "yaml", "yml": "yaml",
    "json": "json", "jsonc": "json",
    "toml": "toml",
    "xml": "xml",
    "markdown": "markdown", "md": "markdown",
    "hcl": "hcl", "terraform": "hcl", "tf": "hcl",
    "lua": "lua",
    "r": "r",
    "dart": "dart",
    "elixir": "elixir", "ex": "elixir",
    "erlang": "erlang", "erl": "erlang",
    "haskell": "haskell", "hs": "haskell",
    "ocaml": "ocaml", "ml": "ocaml",
    "perl": "perl", "pl": "perl",
    "solidity": "solidity", "sol": "solidity",
    "verilog": "verilog", "v": "verilog",
    "zig": "zig",
    "makefile": "makefile", "make": "makefile",
    "cmake": "cmake",
    "nginx": "nginx-config",
    "ini": "ini",
    "properties": "properties",
    "latex": "latex", "tex": "latex",
    "matlab": "matlab",
    "julia": "julia", "jl": "julia",
    "clojure": "clojure", "clj": "clojure",
    "fsharp": "fsharp", "fs": "fsharp", "f#": "fsharp",
    "powershell": "powershell", "ps1": "powershell",
    "prolog": "prolog",
    "scheme": "scheme",
    "lisp": "lisp",
    "assembly": "assembly", "asm": "assembly", "nasm": "assembly",
    "fortran": "fortran", "f90": "fortran",
    "cobol": "cobol",
    "groovy": "groovy",
    "ada": "ada",
    "nim": "nim",
    "crystal": "crystal",
    "vyper": "vyper",
}

# Framework → language inference
FRAMEWORK_LANG_MAP = {
    "react": "typescript", "next.js": "typescript", "nextjs": "typescript",
    "vue": "typescript", "nuxt": "typescript", "angular": "typescript",
    "svelte": "typescript", "sveltekit": "typescript",
    "django": "python", "flask": "python", "fastapi": "python", "tornado": "python",
    "spring": "java", "spring boot": "java", "springboot": "java",
    "express": "javascript", "express.js": "javascript", "koa": "javascript",
    "rails": "ruby", "ruby on rails": "ruby", "sinatra": "ruby",
    "laravel": "php", "symfony": "php",
    "gin": "go", "echo": "go", "fiber": "go",
    "actix": "rust", "axum": "rust", "tokio": "rust", "rocket": "rust",
    "swiftui": "swift", "uikit": "swift",
    "jetpack compose": "kotlin", "ktor": "kotlin",
    "flutter": "dart",
    "pytorch": "python", "tensorflow": "python", "keras": "python",
    "pandas": "python", "numpy": "python", "scikit-learn": "python",
    "tailwind": "css", "bootstrap": "css",
    "terraform": "hcl", "ansible": "yaml", "helm": "yaml",
    "docker compose": "yaml", "docker-compose": "yaml",
    "prisma": "typescript", "drizzle": "typescript",
    "sqlalchemy": "python", "alembic": "python",
    "playwright": "typescript", "cypress": "typescript", "selenium": "python",
    "pygame": "python",
}

# Tool name → agentic tag mapping
TOOL_NAME_MAP = {
    # File operations
    "read_file": "file-operations", "write_file": "file-operations",
    "edit_file": "file-operations", "read": "file-operations",
    "write": "file-operations", "edit": "file-operations",
    "glob": "file-operations", "grep": "file-operations",
    "search_files": "file-operations", "list_files": "file-operations",
    "cat": "file-operations", "ls": "file-operations",

    # Shell / bash
    "bash": "bash-execution", "shell": "bash-execution",
    "terminal": "bash-execution", "execute_command": "bash-execution",
    "run_command": "bash-execution",

    # Code execution
    "python": "code-execution", "execute_code": "code-execution",
    "run_code": "code-execution", "jupyter": "code-execution",
    "repl": "code-execution",

    # Git
    "git": "git-operations",

    # Web
    "web_search": "web-search", "search": "web-search",
    "browser": "web-search", "fetch_url": "web-search",

    # Build
    "build": "build-execution", "compile": "build-execution",
    "make": "build-execution",

    # Test
    "test": "test-running", "run_tests": "test-running",
    "pytest": "test-running",

    # DB
    "sql": "database-query", "query": "database-query",

    # Package management
    "install": "dependency-installation", "pip": "dependency-installation",
    "npm": "dependency-installation", "yarn": "dependency-installation",
}


def detect_code_fence_languages(text):
    """Extract language tags from markdown code fences."""
    pattern = r'```(\w[\w+#.-]*)'
    matches = re.findall(pattern, text)
    languages = set()
    for match in matches:
        lang = match.lower().strip()
        if lang in FENCE_LANG_MAP:
            languages.add(FENCE_LANG_MAP[lang])
    return sorted(languages)


def detect_framework_languages(text):
    """Infer languages from framework/library mentions."""
    text_lower = text.lower()
    languages = set()
    for framework, lang in FRAMEWORK_LANG_MAP.items():
        if framework in text_lower:
            languages.add(lang)
    return sorted(languages)


def count_code_blocks(text):
    """Count number of code blocks in text."""
    return len(re.findall(r'```', text)) // 2


def extract_tool_signals(conversations):
    """Extract agentic signals from tool role messages."""
    tool_names = []
    agentic_tags = set()

    for turn in conversations:
        if turn.get("from") == "tool":
            value = turn.get("value", "")

            # Try to detect tool name from common patterns
            # Pattern: "$ command ..." (shell)
            if value.strip().startswith("$") or value.strip().startswith("#"):
                tool_names.append("bash")
                agentic_tags.add("bash-execution")

                # Check specific commands within bash
                cmd = value.strip().lstrip("$ ").split()[0] if value.strip().lstrip("$ ") else ""
                if cmd in ("cat", "ls", "find", "head", "tail", "grep"):
                    agentic_tags.add("file-operations")
                elif cmd in ("git",):
                    agentic_tags.add("git-operations")
                elif cmd in ("npm", "pip", "yarn", "pnpm", "cargo", "go"):
                    subargs = value.strip().lstrip("$ ").split()
                    if len(subargs) > 1 and subargs[1] in ("install", "add", "get"):
                        agentic_tags.add("dependency-installation")
                elif cmd in ("pytest", "jest", "go test", "cargo test"):
                    agentic_tags.add("test-running")
                elif cmd in ("docker", "make", "cargo build", "npm run build"):
                    agentic_tags.add("build-execution")
                elif cmd in ("python", "node", "ruby", "go run"):
                    agentic_tags.add("code-execution")

            # Pattern: structured tool call JSON-like
            if '"name"' in value or '"tool"' in value:
                for tool_key, tag in TOOL_NAME_MAP.items():
                    if tool_key in value.lower():
                        tool_names.append(tool_key)
                        agentic_tags.add(tag)

    return sorted(set(tool_names)), sorted(agentic_tags)


def detect_behavioral_patterns(conversations):
    """Detect agentic behavioral patterns from conversation structure."""
    patterns = set()
    turns = len(conversations)
    gpt_turns = [t for t in conversations if t.get("from") == "gpt"]
    tool_turns = [t for t in conversations if t.get("from") == "tool"]

    # Multi-file coordination: multiple file operations on different paths
    file_paths = set()
    for t in tool_turns:
        val = t.get("value", "")
        paths = re.findall(r'(?:cat|read|write|edit)\s+(\S+\.\w+)', val)
        paths += re.findall(r'(?:>\s*)(\S+\.\w+)', val)
        file_paths.update(paths)
    if len(file_paths) >= 2:
        patterns.add("multi-file-coordination")

    # Iterative refinement: multiple tool calls suggesting try-fix-retry
    if len(tool_turns) >= 3:
        patterns.add("iterative-refinement")

    # Planning: first gpt turn contains plan-like language
    if gpt_turns:
        first_gpt = gpt_turns[0].get("value", "").lower()
        plan_signals = ["let me", "first", "step 1", "plan", "i'll start by",
                        "先", "首先", "步骤", "计划", "我来"]
        if any(s in first_gpt for s in plan_signals):
            patterns.add("planning")

    # Multi-step reasoning: long gpt response with sequential logic
    for t in gpt_turns:
        val = t.get("value", "")
        if len(val) > 500:
            reasoning_signals = ["because", "therefore", "this means", "so we need",
                                 "因为", "所以", "这意味着", "因此", "根本原因"]
            if sum(1 for s in reasoning_signals if s in val.lower()) >= 2:
                patterns.add("multi-step-reasoning")
                break

    # Error recovery: error message followed by a fix attempt
    for i, t in enumerate(conversations):
        val = t.get("value", "").lower()
        if any(w in val for w in ["error", "failed", "exception", "traceback", "panic", "报错"]):
            if i + 1 < len(conversations):
                patterns.add("error-recovery")
                break

    return sorted(patterns)


def estimate_tokens(text):
    """Rough token estimate: ~4 chars per token for mixed en/zh content."""
    return len(text) // 4


def extract_last_turn(conversations):
    """Extract the last user query and last assistant response."""
    last_human = ""
    last_gpt = ""
    for turn in reversed(conversations):
        if turn.get("from") == "human" and not last_human:
            last_human = turn.get("value", "")
        if turn.get("from") == "gpt" and not last_gpt:
            last_gpt = turn.get("value", "")
        if last_human and last_gpt:
            break
    return last_human, last_gpt


def detect_keywords(text):
    """Detect domain/topic keywords for context hints."""
    text_lower = text.lower()
    hits = []
    keyword_groups = {
        "web": ["react", "vue", "angular", "next.js", "express", "django", "flask",
                "html", "css", "api", "rest", "graphql", "frontend", "backend"],
        "devops": ["docker", "kubernetes", "k8s", "terraform", "ansible", "ci/cd",
                   "github actions", "jenkins", "helm", "nginx", "prometheus", "grafana"],
        "database": ["sql", "postgresql", "mysql", "mongodb", "redis", "sqlite",
                     "database", "query", "index", "migration", "schema"],
        "ml": ["pytorch", "tensorflow", "model", "training", "neural", "dataset",
               "classification", "regression", "epoch", "loss", "optimizer"],
        "security": ["auth", "oauth", "jwt", "xss", "csrf", "injection", "encryption",
                     "password", "token", "vulnerability", "security"],
        "mobile": ["ios", "android", "swift", "kotlin", "flutter", "react native"],
        "systems": ["kernel", "memory", "allocator", "lock-free", "atomic", "assembly",
                    "embedded", "firmware", "rtos"],
    }
    for group, keywords in keyword_groups.items():
        matches = [kw for kw in keywords if kw in text_lower]
        if matches:
            hits.append((group, matches))
    return hits


def preprocess(sample):
    """
    Full preprocessing pipeline for one SFT sample.

    Args:
        sample: dict with "conversations" key in ShareGPT format

    Returns:
        dict with all extracted signals
    """
    conversations = sample.get("conversations", [])
    full_text = " ".join(t.get("value", "") for t in conversations)

    # Language detection
    fence_langs = detect_code_fence_languages(full_text)
    framework_langs = detect_framework_languages(full_text)
    all_detected_langs = sorted(set(fence_langs + framework_langs))

    # Tool / agentic detection
    has_tool_roles = any(t.get("from") == "tool" for t in conversations)
    tool_names, tool_agentic_tags = extract_tool_signals(conversations)
    behavioral_patterns = detect_behavioral_patterns(conversations)

    # Conversation structure
    total_turns = len(conversations)
    code_block_count = count_code_blocks(full_text)
    last_query, last_response = extract_last_turn(conversations)

    # Keywords
    keyword_hits = detect_keywords(full_text)

    # Token estimation
    est_tokens = estimate_tokens(full_text)

    signals = {
        "detected_languages": all_detected_langs,
        "fence_languages": fence_langs,
        "framework_languages": framework_langs,
        "has_tool_roles": has_tool_roles,
        "tool_names": tool_names,
        "tool_agentic_tags": tool_agentic_tags,
        "behavioral_patterns": behavioral_patterns,
        "total_turns": total_turns,
        "code_block_count": code_block_count,
        "est_tokens": est_tokens,
        "keyword_hits": keyword_hits,
        "last_query_preview": last_query[:200] if last_query else "",
        "last_response_length": len(last_response),
    }

    return signals


def format_signals_for_prompt(signals):
    """Format preprocessed signals as a string to embed in the LLM prompt."""
    lines = []
    if signals["detected_languages"]:
        lines.append(f"detected_languages: {signals['detected_languages']}")
    lines.append(f"has_tool_roles: {str(signals['has_tool_roles']).lower()}")
    if signals["tool_names"]:
        lines.append(f"tool_names: {signals['tool_names']}")
    if signals["tool_agentic_tags"]:
        lines.append(f"tool_agentic_tags_detected: {signals['tool_agentic_tags']}")
    if signals["behavioral_patterns"]:
        lines.append(f"behavioral_patterns_detected: {signals['behavioral_patterns']}")
    lines.append(f"code_block_count: {signals['code_block_count']}")
    lines.append(f"total_turns: {signals['total_turns']}")
    lines.append(f"est_tokens: {signals['est_tokens']}")
    if signals["keyword_hits"]:
        kw_str = "; ".join(f"{g}: {', '.join(kws)}" for g, kws in signals["keyword_hits"])
        lines.append(f"keyword_hints: {kw_str}")
    return "\n".join(lines)
