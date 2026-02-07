#!/usr/bin/env python3
"""
Update tags_data.json from YAML files without requiring PyYAML.
Uses simple YAML parsing for our specific tag structure.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

def parse_yaml_list(content):
    """Parse simple YAML list structure for tags."""
    tags = []
    current_tag = None
    current_field = None

    for line in content.split('\n'):
        # Start of new tag
        if line.startswith('- id:'):
            if current_tag:
                tags.append(current_tag)
            current_tag = {'aliases': []}
            current_tag['id'] = line.split(':', 1)[1].strip()
            current_field = None

        elif current_tag:
            stripped = line.lstrip()

            # Field with value on same line
            if stripped.startswith('name:'):
                current_tag['name'] = stripped.split(':', 1)[1].strip()
            elif stripped.startswith('category:'):
                current_tag['category'] = stripped.split(':', 1)[1].strip()
            elif stripped.startswith('source:'):
                current_tag['source'] = stripped.split(':', 1)[1].strip()
            elif stripped.startswith('description:'):
                desc = stripped.split(':', 1)[1].strip()
                current_tag['description'] = desc
                current_field = 'description'

            # Field with list
            elif stripped.startswith('aliases:'):
                current_field = 'aliases'
            elif stripped.startswith('language_scope:'):
                current_field = 'language_scope'
                current_tag['language_scope'] = []

            # List item
            elif stripped.startswith('- ') and current_field:
                value = stripped[2:].strip()
                if current_field == 'aliases':
                    current_tag['aliases'].append(value)
                elif current_field == 'language_scope':
                    current_tag['language_scope'].append(value)

            # Continuation of description
            elif current_field == 'description' and not stripped.startswith(('-', 'id:', 'name:', 'category:', 'source:', 'aliases:', 'language_scope:')):
                if stripped:
                    current_tag['description'] += ' ' + stripped

    if current_tag:
        tags.append(current_tag)

    return tags

def load_all_tags():
    """Load all tags from YAML files."""
    tags_dir = Path('taxonomy/tags')
    all_tags = []
    stats = defaultdict(int)

    for yaml_file in sorted(tags_dir.glob('*.yaml')):
        category = yaml_file.stem
        content = yaml_file.read_text()
        tags = parse_yaml_list(content)

        # Add to all tags
        all_tags.extend(tags)
        stats[category] = len(tags)

        print(f"  {category}: {len(tags)} tags")

    return all_tags, dict(stats)

def main():
    print("Generating tags_data.json from YAML files...")
    print()

    # Load tags
    all_tags, stats = load_all_tags()

    # Create output structure
    output = {
        'tags': all_tags,
        'stats': {
            'total': len(all_tags),
            'by_category': stats
        },
        'generated_at': '2026-02-07',
        'version': '1.0'
    }

    # Write JSON
    output_file = Path('visualization/tags_data.json')
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print()
    print(f"✓ Generated {output_file}")
    print(f"  Total tags: {len(all_tags)}")
    print(f"  Categories: {len(stats)}")

    # Summary by category
    print()
    print("Summary by category:")
    for cat, count in sorted(stats.items()):
        print(f"  - {cat}: {count}")

if __name__ == '__main__':
    main()
