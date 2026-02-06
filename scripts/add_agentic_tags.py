#!/usr/bin/env python3
"""
Add 19 new Agentic tags to taxonomy.
"""

import yaml
from pathlib import Path

# New Agentic tags to add
NEW_AGENTIC_TAGS = [
    # Search Capabilities (2)
    {
        "id": "file-search",
        "name": "File Search",
        "category": "Agentic",
        "aliases": ["glob", "find", "path-search"],
        "source": "Claude Code"
    },
    {
        "id": "code-search",
        "name": "Code Search",
        "category": "Agentic",
        "aliases": ["grep", "content-search", "text-search"],
        "source": "Claude Code"
    },

    # Interaction & Coordination (4)
    {
        "id": "user-interaction",
        "name": "User Interaction",
        "category": "Agentic",
        "aliases": ["ask-user", "user-input", "confirmation"],
        "source": "Claude Code"
    },
    {
        "id": "subagent-management",
        "name": "Subagent Management",
        "category": "Agentic",
        "aliases": ["spawn-agent", "delegate-task", "agent-coordination"],
        "source": "Claude Code"
    },
    {
        "id": "parallel-execution",
        "name": "Parallel Execution",
        "category": "Agentic",
        "aliases": ["concurrent", "parallel-tasks"],
        "source": "curated-list"
    },
    {
        "id": "task-tracking",
        "name": "Task Tracking",
        "category": "Agentic",
        "aliases": ["todo-management", "progress-tracking"],
        "source": "Claude Code"
    },

    # Planning & Extensibility (2)
    {
        "id": "planning",
        "name": "Planning",
        "category": "Agentic",
        "aliases": ["task-planning", "design", "architecture"],
        "source": "Claude Code"
    },
    {
        "id": "skill-execution",
        "name": "Skill Execution",
        "category": "Agentic",
        "aliases": ["plugin", "command", "mcp"],
        "source": "Claude Code"
    },

    # Code Intelligence (6)
    {
        "id": "code-analysis",
        "name": "Code Analysis",
        "category": "Agentic",
        "aliases": ["ast-analysis", "code-understanding", "dependency-analysis"],
        "source": "curated-list"
    },
    {
        "id": "code-generation",
        "name": "Code Generation",
        "category": "Agentic",
        "aliases": ["code-gen", "scaffolding", "boilerplate"],
        "source": "curated-list"
    },
    {
        "id": "refactoring",
        "name": "Refactoring",
        "category": "Agentic",
        "aliases": ["code-refactor", "restructure"],
        "source": "curated-list"
    },
    {
        "id": "documentation-generation",
        "name": "Documentation Generation",
        "category": "Agentic",
        "aliases": ["doc-gen", "api-docs", "comments"],
        "source": "curated-list"
    },
    {
        "id": "test-generation",
        "name": "Test Generation",
        "category": "Agentic",
        "aliases": ["test-gen", "unit-test-gen"],
        "source": "curated-list"
    },
    {
        "id": "code-review",
        "name": "Code Review",
        "category": "Agentic",
        "aliases": ["pr-review", "code-quality", "style-check"],
        "source": "curated-list"
    },

    # Quality & Debugging (2)
    {
        "id": "static-analysis",
        "name": "Static Analysis",
        "category": "Agentic",
        "aliases": ["linting", "type-check", "security-scan"],
        "source": "curated-list"
    },
    {
        "id": "debugging",
        "name": "Debugging",
        "category": "Agentic",
        "aliases": ["debug", "log-analysis", "diagnostics"],
        "source": "curated-list"
    },

    # Multimodal (5)
    {
        "id": "visual-understanding",
        "name": "Visual Understanding",
        "category": "Agentic",
        "aliases": ["screenshot-analysis", "diagram-reading", "image-understanding"],
        "source": "curated-list"
    },
    {
        "id": "diagram-generation",
        "name": "Diagram Generation",
        "category": "Agentic",
        "aliases": ["diagram-gen", "mermaid", "plantuml"],
        "source": "curated-list"
    },
    {
        "id": "ui-automation",
        "name": "UI Automation",
        "category": "Agentic",
        "aliases": ["browser-automation", "gui-testing", "e2e-testing"],
        "source": "curated-list"
    },
    {
        "id": "design-to-code",
        "name": "Design to Code",
        "category": "Agentic",
        "aliases": ["figma-to-code", "sketch-to-html"],
        "source": "curated-list"
    },
    {
        "id": "visual-debugging",
        "name": "Visual Debugging",
        "category": "Agentic",
        "aliases": ["visual-regression", "ui-diff", "layout-debugging"],
        "source": "curated-list"
    }
]


def main():
    tags_file = Path("taxonomy/tags/agentic.yaml")

    print(f"Loading {tags_file}...")
    with open(tags_file, 'r') as f:
        tags = yaml.safe_load(f)

    print(f"Current count: {len(tags)} Agentic tags")

    # Check for duplicates
    existing_ids = {tag['id'] for tag in tags}
    new_tags = []
    skipped = []

    for new_tag in NEW_AGENTIC_TAGS:
        if new_tag['id'] in existing_ids:
            skipped.append(new_tag['id'])
            print(f"  ⚠ Skipping duplicate: {new_tag['id']}")
        else:
            new_tags.append(new_tag)
            print(f"  ✓ Adding: {new_tag['name']}")

    # Add new tags
    tags.extend(new_tags)

    # Sort alphabetically by ID
    tags.sort(key=lambda x: x['id'])

    print(f"\nSaving {len(tags)} tags to {tags_file}...")
    with open(tags_file, 'w') as f:
        yaml.dump(tags, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"\n✅ Added {len(new_tags)} new Agentic tags")
    print(f"   Skipped {len(skipped)} duplicates: {skipped}")
    print(f"   Total: {len(tags)} tags")

    # Print summary by category
    print("\n" + "="*70)
    print("CATEGORY SUMMARY")
    print("="*70)

    categories = {
        "Search": ["file-search", "code-search"],
        "Interaction & Coordination": ["user-interaction", "subagent-management", "parallel-execution", "task-tracking"],
        "Planning & Extensibility": ["planning", "skill-execution"],
        "Code Intelligence": ["code-analysis", "code-generation", "refactoring", "documentation-generation", "test-generation", "code-review"],
        "Quality & Debugging": ["static-analysis", "debugging"],
        "Multimodal": ["visual-understanding", "diagram-generation", "ui-automation", "design-to-code", "visual-debugging"]
    }

    for cat, tag_ids in categories.items():
        print(f"\n{cat} ({len(tag_ids)}):")
        for tag in tags:
            if tag['id'] in tag_ids:
                aliases = ', '.join(tag.get('aliases', [])[:2])
                print(f"  • {tag['name']:30s} [{aliases}]")


if __name__ == '__main__':
    main()
