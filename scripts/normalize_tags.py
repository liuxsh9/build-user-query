#!/usr/bin/env python3
"""
Tag Normalization Script

Processes collected tags to deduplicate, normalize IDs, resolve conflicts,
and enrich metadata. Outputs normalized tags to YAML files.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Set
from collections import defaultdict
import yaml


def load_collected_tags(input_path: Path) -> List[Dict[str, Any]]:
    """Load collected tags from JSON file."""
    with open(input_path, 'r') as f:
        return json.load(f)


def load_taxonomy(taxonomy_path: Path) -> Dict[str, Any]:
    """Load taxonomy definition."""
    with open(taxonomy_path, 'r') as f:
        return yaml.safe_load(f)


def normalize_id(name: str) -> str:
    """
    Convert tag name to kebab-case ID.

    Examples:
        "Python" -> "python"
        "C++" -> "cpp"
        "React.js" -> "reactjs"
        "ASP.NET" -> "aspnet"
    """
    # Convert to lowercase
    id_str = name.lower()

    # Handle special cases
    id_str = id_str.replace("++", "pp")
    id_str = id_str.replace("#", "sharp")
    id_str = id_str.replace(".net", "net")
    id_str = id_str.replace(".js", "js")

    # Replace spaces and special characters with hyphens
    id_str = re.sub(r'[^a-z0-9]+', '-', id_str)

    # Remove leading/trailing hyphens
    id_str = id_str.strip('-')

    return id_str


def deduplicate_tags(tags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Deduplicate tags using exact match, alias match, and case-insensitive matching.

    Returns deduplicated list with merged metadata.
    """
    print("Deduplicating tags...")

    # Group tags by normalized name
    tag_groups = defaultdict(list)

    for tag in tags:
        # Normalize name for comparison
        norm_name = tag["name"].lower().strip()
        tag_groups[norm_name].append(tag)

    deduplicated = []

    for norm_name, group in tag_groups.items():
        if len(group) == 1:
            deduplicated.append(group[0])
        else:
            # Merge duplicates
            merged = group[0].copy()

            # Collect all aliases
            all_aliases = set(merged.get("aliases", []))
            for tag in group[1:]:
                all_aliases.update(tag.get("aliases", []))

            merged["aliases"] = sorted(list(all_aliases))

            # Collect all sources
            sources = set()
            for tag in group:
                sources.add(tag.get("source", "unknown"))
            merged["source"] = ", ".join(sorted(sources))

            # Merge language_scope if present
            if "language_scope" in merged:
                all_langs = set(merged.get("language_scope", []))
                for tag in group[1:]:
                    all_langs.update(tag.get("language_scope", []))
                merged["language_scope"] = sorted(list(all_langs))

            deduplicated.append(merged)
            print(f"  Merged {len(group)} duplicates: {merged['name']}")

    print(f"Deduplicated {len(tags)} -> {len(deduplicated)} tags")
    return deduplicated


def detect_alias_conflicts(tags: List[Dict[str, Any]]) -> List[str]:
    """
    Detect aliases that appear in multiple different tags.

    Returns list of conflict descriptions.
    """
    alias_to_tags = defaultdict(list)

    for tag in tags:
        for alias in tag.get("aliases", []):
            alias_to_tags[alias].append(tag["name"])

    conflicts = []
    for alias, tag_names in alias_to_tags.items():
        if len(set(tag_names)) > 1:
            conflicts.append(f"Alias '{alias}' used by: {', '.join(set(tag_names))}")

    return conflicts


def normalize_tags(tags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Normalize tag IDs and structure.

    Adds 'id' field with kebab-case identifier.
    """
    print("Normalizing tag IDs...")

    normalized = []
    id_counts = defaultdict(int)

    for tag in tags:
        normalized_tag = tag.copy()

        # Generate ID
        tag_id = normalize_id(tag["name"])

        # Handle ID collisions
        if id_counts[tag_id] > 0:
            tag_id = f"{tag_id}-{id_counts[tag_id]}"
        id_counts[tag_id] += 1

        normalized_tag["id"] = tag_id

        # Ensure aliases are lowercase
        if "aliases" in normalized_tag:
            normalized_tag["aliases"] = [a.lower() for a in normalized_tag["aliases"]]

        normalized.append(normalized_tag)

    print(f"Normalized {len(normalized)} tags")
    return normalized


def validate_granularity(tags: List[Dict[str, Any]]) -> List[str]:
    """
    Check tag granularity and flag issues.

    Returns list of warnings.
    """
    warnings = []

    for tag in tags:
        name = tag["name"]

        # Flag overly specific tags (function-level)
        if "." in name and name.count(".") > 1:
            warnings.append(f"Tag '{name}' may be too specific (function-level)")

        # Flag overly broad tags
        if name.lower() in ["programming", "coding", "software"]:
            warnings.append(f"Tag '{name}' may be too broad")

    return warnings


def save_normalized_tags(tags: List[Dict[str, Any]], output_dir: Path):
    """
    Save normalized tags to category-specific YAML files.

    Tags are sorted alphabetically by ID.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Group tags by category
    by_category = defaultdict(list)
    for tag in tags:
        by_category[tag["category"]].append(tag)

    # Save each category
    for category, category_tags in by_category.items():
        # Sort by ID
        category_tags.sort(key=lambda t: t["id"])

        # Convert to YAML-friendly format
        yaml_tags = []
        for tag in category_tags:
            yaml_tag = {
                "id": tag["id"],
                "name": tag["name"],
                "category": tag["category"]
            }

            if "subcategory" in tag:
                yaml_tag["subcategory"] = tag["subcategory"]
            if "description" in tag:
                yaml_tag["description"] = tag["description"]
            if "aliases" in tag and tag["aliases"]:
                yaml_tag["aliases"] = tag["aliases"]
            if "language_scope" in tag and tag["language_scope"]:
                yaml_tag["language_scope"] = tag["language_scope"]
            if "difficulty" in tag:
                yaml_tag["difficulty"] = tag["difficulty"]
            if "source" in tag:
                yaml_tag["source"] = tag["source"]

            yaml_tags.append(yaml_tag)

        # Write to file
        filename = f"{category.lower()}.yaml"
        output_path = output_dir / filename

        with open(output_path, 'w') as f:
            yaml.dump(yaml_tags, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print(f"Saved {len(yaml_tags)} tags to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Normalize collected tags and output to YAML files"
    )
    parser.add_argument(
        '--input',
        type=Path,
        required=True,
        help='Input JSON file with collected tags'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('taxonomy/tags'),
        help='Output directory for YAML files'
    )
    parser.add_argument(
        '--taxonomy',
        type=Path,
        default=Path('taxonomy.yaml'),
        help='Path to taxonomy.yaml'
    )

    args = parser.parse_args()

    # Load inputs
    print(f"Loading collected tags from {args.input}...")
    tags = load_collected_tags(args.input)
    print(f"Loaded {len(tags)} tags")

    taxonomy = load_taxonomy(args.taxonomy)

    # Deduplicate
    tags = deduplicate_tags(tags)

    # Detect alias conflicts
    conflicts = detect_alias_conflicts(tags)
    if conflicts:
        print("\nWARNING: Alias conflicts detected:")
        for conflict in conflicts:
            print(f"  - {conflict}")
        print()

    # Normalize IDs
    tags = normalize_tags(tags)

    # Validate granularity
    warnings = validate_granularity(tags)
    if warnings:
        print("\nGranularity warnings:")
        for warning in warnings:
            print(f"  - {warning}")
        print()

    # Save to YAML files
    print(f"\nSaving normalized tags to {args.output_dir}...")
    save_normalized_tags(tags, args.output_dir)

    print("\nNormalization complete!")
    print(f"Review tags in {args.output_dir}")
    print("Next step: Run validate_taxonomy.py to check for errors")


if __name__ == '__main__':
    main()
