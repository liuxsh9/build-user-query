#!/usr/bin/env python3
"""
Update tags_data.json and tag-visualization.html from YAML files without requiring PyYAML.
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
    """Load all tags from YAML files, grouped by category."""
    tags_dir = Path('taxonomy/tags')
    tags_by_category = {}
    stats = defaultdict(int)

    for yaml_file in sorted(tags_dir.glob('*.yaml')):
        content = yaml_file.read_text()
        tags = parse_yaml_list(content)

        # Group by category
        for tag in tags:
            category = tag.get('category', 'Unknown')
            if category not in tags_by_category:
                tags_by_category[category] = []
            tags_by_category[category].append(tag)
            stats[category] += 1

    return tags_by_category, dict(stats)

def update_html_embedded_data(html_path, tags_data):
    """Update embedded data in HTML file."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Generate new data (compressed format to reduce file size)
    new_data_json = json.dumps(tags_data, ensure_ascii=False, separators=(',', ':'))

    # Find and replace embedded data
    # Match "let tagsData = {...};"
    start_marker = "let tagsData = "
    end_marker = ";\n        let currentFilter"

    start_idx = html_content.find(start_marker)
    end_idx = html_content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print(f"  ⚠️  Could not find data markers in {html_path}")
        return False

    # Build new content
    new_html_content = (
        html_content[:start_idx + len(start_marker)] +
        new_data_json +
        html_content[end_idx:]
    )

    # Write back
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html_content)

    return True

def main():
    print("Generating tags_data.json and updating HTML from YAML files...")
    print()

    # Load tags grouped by category
    tags_by_category, stats = load_all_tags()

    # Calculate totals
    total_tags = sum(stats.values())

    # Print stats
    print("Tags loaded:")
    for cat, count in sorted(stats.items()):
        print(f"  {cat}: {count} tags")
    print()

    # Write JSON file (按 category 分组的格式，与 HTML 兼容)
    output_file = Path('visualization/tags_data.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tags_by_category, f, indent=2, ensure_ascii=False)

    print(f"✓ Generated {output_file}")
    print(f"  Total tags: {total_tags}")
    print(f"  Categories: {len(stats)}")
    print()

    # Update HTML embedded data
    html_file = Path('visualization/tag-visualization.html')
    if html_file.exists():
        if update_html_embedded_data(html_file, tags_by_category):
            print(f"✓ Updated embedded data in {html_file}")
        else:
            print(f"✗ Failed to update {html_file}")
    else:
        print(f"⚠️  HTML file not found: {html_file}")

    print()
    print("Summary:")
    print(f"  - Total tags: {total_tags}")
    print(f"  - Categories: {len(stats)}")
    print(f"  - Format: Grouped by category (HTML compatible)")

if __name__ == '__main__':
    main()
