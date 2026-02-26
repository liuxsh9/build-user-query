"""
Labeling Pipeline Configuration

All production settings extracted here for easy tuning.
"""

import os
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

DEFAULT_INPUT = DATA_DIR / "raw_samples.json"
DEFAULT_OUTPUT = DATA_DIR / "labeled_samples.json"

# ─── LLM API ────────────────────────────────────────────
LITELLM_BASE = os.environ.get("LITELLM_BASE", "http://localhost:4000/v1")
LITELLM_KEY = os.environ.get("LITELLM_KEY", "")

# ─── Pipeline Defaults ──────────────────────────────────
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_CONCURRENCY = 100
CONFIDENCE_THRESHOLD = 0.65
MAX_RETRIES = 3
SAMPLE_MAX_RETRIES = 3             # sample-level retry on call failure
REQUEST_TIMEOUT = 60           # seconds per LLM call (gpt-4o-mini is fast)
HTTP_CLIENT_TIMEOUT = 60       # httpx client timeout
SAMPLE_TIMEOUT = 300           # seconds total per sample (including all retries)

# ─── Directory Pipeline ────────────────────────────────
DIR_PIPELINE_WATERMARK = 2.0   # load next file when in-flight < concurrency * watermark
DIR_PIPELINE_MAX_FILES = 5     # max files loaded in memory simultaneously

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
        "qwen3-30b-a3b-instruct-2507",
        "gemini-3-flash-preview",
        "deepseek-v3.1",
        "glm-4.7-flashx",
    ],
}

PIPELINE_DEFAULTS = {
    "production_labeling": "gpt-4o-mini",          # 8x faster, 100% success, cheap
    "production_labeling_alt": "deepseek-v3.2",    # quality fallback (0 unmapped)
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
