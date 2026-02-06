#!/usr/bin/env python3
"""
Add Phase 1 & 2 languages to taxonomy.
"""

import yaml
from pathlib import Path

# New languages to add
NEW_LANGUAGES = [
    # Phase 1: Infrastructure & Config
    {
        "id": "makefile",
        "name": "Makefile",
        "category": "Language",
        "aliases": ["makefile", "make", "gnumake"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["build", "devops"]
    },
    {
        "id": "cmake",
        "name": "CMake",
        "category": "Language",
        "aliases": ["cmake"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["build"]
    },
    {
        "id": "gradle",
        "name": "Gradle",
        "category": "Language",
        "aliases": ["gradle", "groovy-dsl", "kotlin-dsl"],
        "source": "GitHub",
        "paradigm": ["declarative", "imperative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["build"]
    },
    {
        "id": "maven",
        "name": "Maven",
        "category": "Language",
        "aliases": ["maven", "pom", "pom.xml"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "static",
        "runtime": "interpreted",
        "use_cases": ["build"]
    },
    {
        "id": "bazel",
        "name": "Bazel",
        "category": "Language",
        "aliases": ["bazel", "starlark"],
        "source": "GitHub",
        "paradigm": ["declarative", "functional"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["build"]
    },
    {
        "id": "yaml",
        "name": "YAML",
        "category": "Language",
        "aliases": ["yaml", "yml"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["config", "devops"]
    },
    {
        "id": "toml",
        "name": "TOML",
        "category": "Language",
        "aliases": ["toml"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "static",
        "runtime": "interpreted",
        "use_cases": ["config"]
    },
    {
        "id": "json",
        "name": "JSON",
        "category": "Language",
        "aliases": ["json"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "static",
        "runtime": "interpreted",
        "use_cases": ["config", "web"]
    },
    {
        "id": "xml",
        "name": "XML",
        "category": "Language",
        "aliases": ["xml"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "static",
        "runtime": "interpreted",
        "use_cases": ["config", "markup"]
    },
    {
        "id": "ini",
        "name": "INI",
        "category": "Language",
        "aliases": ["ini", "cfg", "conf"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["config"]
    },
    {
        "id": "dockerfile",
        "name": "Dockerfile",
        "category": "Language",
        "aliases": ["dockerfile", "docker"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["devops", "config"]
    },
    {
        "id": "dotenv",
        "name": "Dotenv",
        "category": "Language",
        "aliases": ["dotenv", "env"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["config"]
    },
    {
        "id": "properties",
        "name": "Properties",
        "category": "Language",
        "aliases": ["properties", "props"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["config"]
    },
    {
        "id": "nginx-config",
        "name": "Nginx Config",
        "category": "Language",
        "aliases": ["nginx", "nginx-conf"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["config", "devops"]
    },
    {
        "id": "hcl",
        "name": "HCL",
        "category": "Language",
        "aliases": ["hcl", "terraform", "tf"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["devops", "config"]
    },

    # Phase 2: Business-Critical & Documentation
    {
        "id": "arkts",
        "name": "ArkTS",
        "category": "Language",
        "aliases": ["arkts", "ark-ts"],
        "source": "Business",
        "paradigm": ["object-oriented", "functional"],
        "typing": "static",
        "runtime": "jit",
        "use_cases": ["mobile"]
    },
    {
        "id": "ascendc",
        "name": "AscendC",
        "category": "Language",
        "aliases": ["ascendc", "ascend-c"],
        "source": "Business",
        "paradigm": ["imperative"],
        "typing": "static",
        "runtime": "compiled",
        "use_cases": ["systems", "scientific"]
    },
    {
        "id": "latex",
        "name": "LaTeX",
        "category": "Language",
        "aliases": ["latex", "tex"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "compiled",
        "use_cases": ["markup", "scientific"]
    },
    {
        "id": "markdown",
        "name": "Markdown",
        "category": "Language",
        "aliases": ["markdown", "md"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["markup"]
    },
    {
        "id": "restructuredtext",
        "name": "reStructuredText",
        "category": "Language",
        "aliases": ["restructuredtext", "rst", "rest"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["markup"]
    },
    {
        "id": "jinja",
        "name": "Jinja",
        "category": "Language",
        "aliases": ["jinja", "jinja2"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["web", "scripting"]
    },
    {
        "id": "handlebars",
        "name": "Handlebars",
        "category": "Language",
        "aliases": ["handlebars", "hbs"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["web"]
    },
    {
        "id": "erb",
        "name": "ERB",
        "category": "Language",
        "aliases": ["erb", "embedded-ruby"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["web"]
    },
    {
        "id": "ejs",
        "name": "EJS",
        "category": "Language",
        "aliases": ["ejs", "embedded-js"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["web"]
    },
    {
        "id": "liquid",
        "name": "Liquid",
        "category": "Language",
        "aliases": ["liquid"],
        "source": "GitHub",
        "paradigm": ["declarative"],
        "typing": "dynamic",
        "runtime": "interpreted",
        "use_cases": ["web"]
    }
]


def main():
    tags_file = Path("taxonomy/tags/language.yaml")

    print(f"Loading {tags_file}...")
    with open(tags_file, 'r') as f:
        tags = yaml.safe_load(f)

    print(f"Current count: {len(tags)} languages")

    # Check for duplicates
    existing_ids = {tag['id'] for tag in tags}
    new_tags = []
    skipped = []

    for new_lang in NEW_LANGUAGES:
        if new_lang['id'] in existing_ids:
            skipped.append(new_lang['id'])
            print(f"  ⚠ Skipping duplicate: {new_lang['id']}")
        else:
            new_tags.append(new_lang)
            print(f"  ✓ Adding: {new_lang['name']}")

    # Add new languages
    tags.extend(new_tags)

    # Sort alphabetically by ID
    tags.sort(key=lambda x: x['id'])

    print(f"\nSaving {len(tags)} languages to {tags_file}...")
    with open(tags_file, 'w') as f:
        yaml.dump(tags, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"\n✅ Added {len(new_tags)} new languages")
    print(f"   Skipped {len(skipped)} duplicates: {skipped}")
    print(f"   Total: {len(tags)} languages")


if __name__ == '__main__':
    main()
