"""
Preprocessing Module

Extracts structural signals from SFT conversations before LLM labeling.
These signals are embedded into the prompt to help the LLM focus on semantic
judgment rather than basic information extraction.

Supports two input formats:
  - ShareGPT: {"conversations": [{"from": "human/gpt/tool", "value": "..."}]}
  - Pangu:    {"data": [{"role": "user/assistant/tool", "content": "..."}]}

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
# Format normalization
# ─────────────────────────────────────────────────────────

# Pangu special tokens to strip for labeling
_PANGU_TOKENS_RE = re.compile(
    r'\[unused(?:9|10|11|12|13|14|15|16|17)\]'
)
_NO_THINK_RE = re.compile(r'\s*/no_think')

PANGU_ROLE_MAP = {"user": "human", "assistant": "gpt", "tool": "tool"}


def detect_format(sample):
    """Detect whether sample is ShareGPT or Pangu format."""
    if "conversations" in sample:
        return "sharegpt"
    if "data" in sample:
        return "pangu"
    return "unknown"


def _strip_pangu_tokens(text):
    """Remove Pangu training tokens, preserving semantic content."""
    text = _NO_THINK_RE.sub('', text)
    text = _PANGU_TOKENS_RE.sub('', text)
    return text.strip()


def slice_multiturn(conversations):
    """Slice multi-turn conversations into training-aligned samples.

    Each assistant reply becomes one sample, with full preceding context.
    Mirrors how SFT training expands multi-turn into pyramid-shaped samples:
      [H1] → A1
      [H1, A1, H2] → A2
      [H1, A1, H2, A2, H3] → A3

    Single-turn (1 human + 1 gpt) returns as-is in a list.
    """
    # Find all assistant reply indices
    reply_indices = [i for i, t in enumerate(conversations) if t["from"] == "gpt"]

    if len(reply_indices) <= 1:
        return [conversations]

    slices = []
    for idx in reply_indices:
        # Context = everything up to and including this assistant reply
        slices.append(conversations[:idx + 1])

    return slices


def normalize_pangu(sample):
    """Convert Pangu format sample to internal ShareGPT format.

    - Strips training tokens ([unused*], /no_think)
    - Maps roles (user→human, assistant→gpt)
    - Detects pseudo multi-turn (already a single training sample)
    - Preserves meta_prompt and tools in metadata
    """
    data = sample.get("data", [])
    conversations = []
    is_pseudo_multiturn = False

    for turn in data:
        role = PANGU_ROLE_MAP.get(turn.get("role", ""), turn.get("role", ""))
        content = turn.get("content", "")

        # Detect pseudo multi-turn (don't expand, just strip tokens)
        if role == "human" and "[unused10]" in content:
            is_pseudo_multiturn = True

        conversations.append({
            "from": role,
            "value": _strip_pangu_tokens(content),
        })

    # Build normalized sample
    normalized = {
        "id": sample.get("id", ""),
        "conversations": conversations,
        "metadata": sample.get("metadata", {}),
    }

    # Preserve Pangu-specific info in metadata
    pangu_meta = {}
    if sample.get("meta_prompt"):
        pangu_meta["system_prompt"] = sample["meta_prompt"]
    if sample.get("tools"):
        pangu_meta["tool_definitions"] = sample["tools"]
    pangu_meta["is_pseudo_multiturn"] = is_pseudo_multiturn
    pangu_meta["original_format"] = "pangu"
    normalized["metadata"] = {**normalized["metadata"], **pangu_meta}

    return normalized


def normalize_and_slice(sample):
    """Auto-detect format, normalize, and slice multi-turn into training samples.

    Returns a list of samples. Single-turn and pseudo multi-turn return [1 sample].
    True multi-turn returns [N samples], one per assistant reply.
    Each slice has id suffixed with turn number (e.g. "id_t1", "id_t2").
    """
    fmt = detect_format(sample)
    if fmt == "pangu":
        normalized = normalize_pangu(sample)
    else:
        normalized = dict(sample)

    conversations = normalized.get("conversations", [])
    is_pseudo = normalized.get("metadata", {}).get("is_pseudo_multiturn", False)

    # Pseudo multi-turn: already one training sample, don't slice
    if is_pseudo:
        return [normalized]

    slices = slice_multiturn(conversations)

    if len(slices) == 1:
        return [normalized]

    # Build one sample per slice
    results = []
    base_id = normalized.get("id", "")
    for i, conv_slice in enumerate(slices):
        s = {
            "id": f"{base_id}_t{i+1}",
            "conversations": conv_slice,
            "metadata": {
                **normalized.get("metadata", {}),
                "source_id": base_id,
                "turn_index": i + 1,
                "total_turns": len(slices),
            },
        }
        results.append(s)

    return results


# Keep backward-compatible alias
def normalize_sample(sample):
    """Normalize without slicing (for tools that don't need multi-turn expansion)."""
    fmt = detect_format(sample)
    if fmt == "pangu":
        return normalize_pangu(sample)
    return sample


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
        sample: dict in ShareGPT or Pangu format (auto-detected)

    Returns:
        dict with all extracted signals
    """
    sample = normalize_sample(sample)
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
