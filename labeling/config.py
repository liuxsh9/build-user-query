"""
Labeling Pipeline Configuration

All production settings extracted here for easy tuning.
"""

from pathlib import Path

# ─── Paths ───────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

DEFAULT_INPUT = DATA_DIR / "raw_samples.json"
DEFAULT_OUTPUT = DATA_DIR / "labeled_samples.json"

# ─── LLM API ────────────────────────────────────────────
LITELLM_BASE = "http://101.47.36.53:4000/v1"
LITELLM_KEY = "***REDACTED***"

# ─── Pipeline Defaults ──────────────────────────────────
DEFAULT_MODEL = "deepseek-v3.2"
DEFAULT_CONCURRENCY = 30
CONFIDENCE_THRESHOLD = 0.65
MAX_RETRIES = 3
REQUEST_TIMEOUT = 180          # seconds per LLM call
HTTP_CLIENT_TIMEOUT = 120      # httpx client timeout

# ─── Model Tiers ────────────────────────────────────────
MODELS = {
    "strong": [
        "claude-opus-4-5-20251101-thinking",
        "gpt-5",
        "gemini-2.5-pro-thinking",
    ],
    "mid": [
        "claude-sonnet-4-6",
        "deepseek-v3.2",
        "qwen3-235b-a22b",
        "gemini-2.5-flash-thinking",
        "glm-5",
    ],
    "light": [
        "gpt-4o-mini",
        "deepseek-v3.1",
        "qwen3-30b-a3b-instruct-2507",
        "gemini-3-flash-preview",
        "glm-4.7-flash",
    ],
}

PIPELINE_DEFAULTS = {
    "production_labeling": "deepseek-v3.2",
    "gold_set_annotation": "claude-sonnet-4-6",
    "arbitration": "claude-opus-4-5-20251101-thinking",
}

# ─── Consistency Rules ──────────────────────────────────
CONSISTENCY_RULES = [
    ("intent == 'learn' and len(agentic) > 3",
     "Intent=learn but many agentic tags"),
    ("intent == 'build' and 'feature-implementation' not in task and len(task) > 0",
     "Intent=build but no feature-implementation in task"),
    ("difficulty == 'beginner' and len(concept) > 3",
     "Difficulty=beginner but many concepts"),
    ("len(constraint) > 0 and difficulty == 'beginner'",
     "Has constraints but difficulty=beginner"),
]
