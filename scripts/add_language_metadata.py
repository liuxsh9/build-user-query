#!/usr/bin/env python3
"""
Add metadata (paradigm, typing, runtime, use_cases) to existing Language tags.
"""

import yaml
from pathlib import Path

# Metadata mapping for all 50 existing languages
LANGUAGE_METADATA = {
    "ada": {
        "paradigm": ["imperative", "object-oriented"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["systems", "embedded"]
    },
    "apl": {
        "paradigm": ["functional", "array-oriented"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["scientific", "data-science"]
    },
    "assembly": {
        "paradigm": ["imperative"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["systems", "embedded"]
    },
    "c": {
        "paradigm": ["procedural", "imperative"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["systems", "embedded"]
    },
    "clojure": {
        "paradigm": ["functional"],
        "typing": "dynamic",
        "runtime": "jit",
        "use_cases": ["web", "data-science"]
    },
    "cobol": {
        "paradigm": ["procedural", "imperative"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["systems"]
    },
    "cpp": {
        "paradigm": ["object-oriented", "procedural", "functional"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["systems", "game-dev", "embedded"]
    },
    "crystal": {
        "paradigm": ["object-oriented"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["web", "systems"]
    },
    "csharp": {
        "paradigm": ["object-oriented", "functional"],
        "typing": "static",
        "runtime": "jit",
        "use_cases": ["web", "game-dev", "mobile"]
    },
    "css": {
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["web", "markup"]
    },
    "dart": {
        "paradigm": ["object-oriented"],
        "typing": "strong-static",
        "runtime": "jit",
        "use_cases": ["mobile", "web"]
    },
    "elixir": {
        "paradigm": ["functional", "concurrent"],
        "typing": "dynamic",
        "runtime": "jit",
        "use_cases": ["web", "systems"]
    },
    "erlang": {
        "paradigm": ["functional", "concurrent"],
        "typing": "dynamic",
        "runtime": "jit",
        "use_cases": ["systems", "web"]
    },
    "fortran": {
        "paradigm": ["procedural", "imperative"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["scientific", "data-science"]
    },
    "fsharp": {
        "paradigm": ["functional", "object-oriented"],
        "typing": "static",
        "runtime": "jit",
        "use_cases": ["web", "data-science"]
    },
    "go": {
        "paradigm": ["procedural", "concurrent"],
        "typing": "strong-static",
        "runtime": "compiled",
        "use_cases": ["systems", "web", "devops"]
    },
    "groovy": {
        "paradigm": ["object-oriented", "functional"],
        "typing": "dynamic",
        "runtime": "jit",
        "use_cases": ["web", "scripting", "build"]
    },
    "haskell": {
        "paradigm": ["functional"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["web", "data-science"]
    },
    "html": {
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["web", "markup"]
    },
    "java": {
        "paradigm": ["object-oriented"],
        "typing": "static",
        "runtime": "jit",
        "use_cases": ["web", "mobile", "systems"]
    },
    "javascript": {
        "paradigm": ["object-oriented", "functional", "event-driven"],
        "typing": "dynamic",
        "runtime": "hybrid",
        "use_cases": ["web", "mobile", "scripting"]
    },
    "julia": {
        "paradigm": ["functional", "procedural"],
        "typing": "dynamic",
        "runtime": "jit",
        "use_cases": ["scientific", "data-science"]
    },
    "kotlin": {
        "paradigm": ["object-oriented", "functional"],
        "typing": "static",
        "runtime": "jit",
        "use_cases": ["mobile", "web"]
    },
    "lisp": {
        "paradigm": ["functional"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["scripting", "data-science"]
    },
    "lua": {
        "paradigm": ["procedural", "object-oriented"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["scripting", "game-dev", "embedded"]
    },
    "matlab": {
        "paradigm": ["procedural"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["scientific", "data-science"]
    },
    "nim": {
        "paradigm": ["imperative", "functional"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["systems", "web"]
    },
    "objective-c": {
        "paradigm": ["object-oriented"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["mobile"]
    },
    "ocaml": {
        "paradigm": ["functional", "object-oriented"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["web", "systems"]
    },
    "perl": {
        "paradigm": ["procedural", "object-oriented"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["scripting", "web"]
    },
    "php": {
        "paradigm": ["object-oriented", "procedural"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["web"]
    },
    "powershell": {
        "paradigm": ["object-oriented", "procedural"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["scripting", "devops"]
    },
    "prolog": {
        "paradigm": ["logic"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["scientific"]
    },
    "python": {
        "paradigm": ["object-oriented", "procedural", "functional"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["data-science", "web", "scripting"]
    },
    "r": {
        "paradigm": ["functional", "procedural"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["data-science", "scientific"]
    },
    "racket": {
        "paradigm": ["functional"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["scripting", "scientific"]
    },
    "ruby": {
        "paradigm": ["object-oriented"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["web", "scripting"]
    },
    "rust": {
        "paradigm": ["functional", "procedural"],
        "typing": "strong-static",
        "runtime": "compiled",
        "use_cases": ["systems", "web", "embedded"]
    },
    "scala": {
        "paradigm": ["object-oriented", "functional"],
        "typing": "static",
        "runtime": "jit",
        "use_cases": ["web", "data-science"]
    },
    "scheme": {
        "paradigm": ["functional"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["scripting", "scientific"]
    },
    "shell": {
        "paradigm": ["procedural"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["scripting", "devops"]
    },
    "smalltalk": {
        "paradigm": ["object-oriented"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["scripting"]
    },
    "solidity": {
        "paradigm": ["object-oriented"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["blockchain"]
    },
    "sql": {
        "paradigm": ["declarative"],
        "typing": "static",
        "runtime": "interpreted",
        "use_cases": ["data-science", "web"]
    },
    "swift": {
        "paradigm": ["object-oriented", "functional"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["mobile"]
    },
    "typescript": {
        "paradigm": ["object-oriented", "functional"],
        "typing": "gradual",
        "runtime": "transpiled",
        "use_cases": ["web", "mobile"]
    },
    "verilog": {
        "paradigm": ["declarative"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["embedded", "systems"]
    },
    "vhdl": {
        "paradigm": ["declarative"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["embedded", "systems"]
    },
    "vyper": {
        "paradigm": ["object-oriented"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["blockchain"]
    },
    "zig": {
        "paradigm": ["imperative"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["systems", "embedded"]
    }
}


def main():
    tags_file = Path("taxonomy/tags/language.yaml")

    print(f"Loading {tags_file}...")
    with open(tags_file, 'r') as f:
        tags = yaml.safe_load(f)

    print(f"Loaded {len(tags)} language tags")

    # Add metadata to each tag
    updated_count = 0
    for tag in tags:
        tag_id = tag.get("id")
        if tag_id in LANGUAGE_METADATA:
            metadata = LANGUAGE_METADATA[tag_id]
            tag["paradigm"] = metadata["paradigm"]
            tag["typing"] = metadata["typing"]
            tag["runtime"] = metadata["runtime"]
            tag["use_cases"] = metadata["use_cases"]
            updated_count += 1
            print(f"  ✓ Updated {tag_id}")
        else:
            print(f"  ⚠ No metadata for {tag_id}")

    # Save updated tags
    print(f"\nSaving updated tags to {tags_file}...")
    with open(tags_file, 'w') as f:
        yaml.dump(tags, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"\n✅ Updated {updated_count}/{len(tags)} language tags with metadata")


if __name__ == '__main__':
    main()
