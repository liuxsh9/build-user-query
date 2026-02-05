#!/usr/bin/env python3
"""
Enhanced Tag Normalization Script

Normalizes collected tags by:
- Deduplicating (exact match, alias match, case-insensitive)
- Converting IDs to kebab-case
- Detecting alias conflicts
- Integrating automated alias expansion
- Preserving source-specific metrics
- Calculating aggregate weighted scores
- Adding granularity metadata
- Sorting alphabetically
- Outputting to YAML format
"""

import argparse
import json
import yaml
import re
import sys
from pathlib import Path
from typing import List, Dict, Set, Any, Optional
from collections import defaultdict

# Import alias expander
sys.path.insert(0, str(Path(__file__).parent))
from expand_aliases import AliasExpander


def load_collected_tags(input_path: Path) -> List[Dict[str, Any]]:
    """Load collected tags from JSON file."""
    with open(input_path, 'r') as f:
        return json.load(f)


def load_taxonomy(taxonomy_path: Path) -> Dict[str, Any]:
    """Load taxonomy definition."""
    with open(taxonomy_path, 'r') as f:
        return yaml.safe_load(f)


def normalize_id(name: str) -> str:
    """Convert name to kebab-case ID."""
    # Remove special characters, convert to lowercase
    normalized = re.sub(r'[^\w\s-]', '', name.lower())
    # Replace spaces and underscores with hyphens
    normalized = re.sub(r'[\s_]+', '-', normalized)
    # Remove consecutive hyphens
    normalized = re.sub(r'-+', '-', normalized)
    # Strip leading/trailing hyphens
    return normalized.strip('-')


def deduplicate_tags(tags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Deduplicate tags based on:
    1. Exact ID match
    2. Alias match
    3. Case-insensitive name match

    When duplicates found, merge their sources and keep highest weighted score.
    """
    print("Deduplicating tags...")

    # Build lookup maps
    id_map = {}
    alias_map = defaultdict(list)
    name_map = defaultdict(list)

    for tag in tags:
        tag_id = tag.get('id', normalize_id(tag['name']))
        tag['id'] = tag_id  # Ensure ID is set

        # Track by ID
        if tag_id in id_map:
            # Merge with existing tag
            existing = id_map[tag_id]
            existing = merge_tags(existing, tag)
            id_map[tag_id] = existing
        else:
            id_map[tag_id] = tag

        # Track by aliases
        for alias in tag.get('aliases', []):
            alias_map[alias.lower()].append(tag_id)

        # Track by name
        name_map[tag['name'].lower()].append(tag_id)

    # Detect alias conflicts
    conflicts = []
    for alias, tag_ids in alias_map.items():
        if len(set(tag_ids)) > 1:
            conflicts.append(f"Alias '{alias}' used by multiple tags: {set(tag_ids)}")

    if conflicts:
        print(f"⚠️  Alias conflicts detected:")
        for conflict in conflicts:
            print(f"  - {conflict}")

    deduplicated = list(id_map.values())
    print(f"  Deduplicated: {len(tags)} → {len(deduplicated)} tags")

    return deduplicated


def merge_tags(tag1: Dict[str, Any], tag2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two duplicate tags, combining their sources and metadata.
    """
    merged = tag1.copy()

    # Merge sources
    if 'sources' in tag1 and 'sources' in tag2:
        merged['sources'] = tag1['sources'] + tag2['sources']
    elif 'sources' in tag2:
        merged['sources'] = tag2['sources']

    # Merge aliases
    aliases1 = set(tag1.get('aliases', []))
    aliases2 = set(tag2.get('aliases', []))
    merged['aliases'] = sorted(list(aliases1 | aliases2))

    # Merge language_scope
    lang1 = set(tag1.get('language_scope', []))
    lang2 = set(tag2.get('language_scope', []))
    merged['language_scope'] = sorted(list(lang1 | lang2))

    # Use higher weighted score
    score1 = tag1.get('weighted_score', 0)
    score2 = tag2.get('weighted_score', 0)
    merged['weighted_score'] = max(score1, score2)

    return merged


def expand_aliases_for_tags(tags: List[Dict[str, Any]], auto_approve: bool = True) -> List[Dict[str, Any]]:
    """
    Run automated alias expansion on all tags.

    Args:
        tags: List of normalized tags
        auto_approve: If True, automatically add high-confidence aliases (>0.8)

    Returns:
        Tags with expanded aliases
    """
    print("Expanding aliases...")

    expander = AliasExpander()
    total_added = 0

    for tag in tags:
        tag_id = tag['id']
        tag_name = tag['name']
        existing_aliases = tag.get('aliases', [])

        # Generate candidates
        candidates = expander.expand_aliases(tag_id, tag_name, existing_aliases)
        categorized = expander.categorize_by_confidence(candidates)

        # Add auto-approve candidates
        if auto_approve and categorized['auto_approve']:
            new_aliases = [c.alias for c in categorized['auto_approve']]
            tag['aliases'] = sorted(list(set(existing_aliases + new_aliases)))
            total_added += len(new_aliases)
            print(f"  {tag_id}: Added {len(new_aliases)} aliases: {new_aliases}")

        # Flag medium-confidence for review
        if categorized['needs_review']:
            review_aliases = [c.alias for c in categorized['needs_review']]
            print(f"  ⚠️  {tag_id}: {len(review_aliases)} aliases need review: {review_aliases}")

    print(f"  Total aliases auto-added: {total_added}")
    return tags


def classify_granularity(tag: Dict[str, Any]) -> str:
    """
    Classify tag granularity based on name patterns and context.

    Returns: 'library', 'module', or 'component'
    """
    tag_id = tag['id']
    tag_name = tag['name']

    # Component-level indicators (most specific)
    component_patterns = [
        r'-hooks?$',  # react-hooks
        r'-middleware$',  # express-middleware
        r'-fixtures?$',  # pytest-fixtures
        r'-decorators?$',  # typeorm-decorators
        r'-groupby$',  # pandas-groupby
        r'-autograd$',  # pytorch-autograd
        r'-waits?$',  # selenium-waits
        r'-intercept$',  # cypress-intercept
    ]

    for pattern in component_patterns:
        if re.search(pattern, tag_id):
            return 'component'

    # Module-level indicators (subsystems)
    module_patterns = [
        r'-orm$',  # django-orm, sqlalchemy-orm
        r'-router$',  # react-router, vue-router
        r'-client$',  # prisma-client
        r'-core$',  # sqlalchemy-core
        r'-nn$',  # pytorch-nn
        r'-dataframe$',  # pandas-dataframe
        r'-compose$',  # docker-compose
        r'-webdriver$',  # selenium-webdriver
    ]

    for pattern in module_patterns:
        if re.search(pattern, tag_id):
            return 'module'

    # Default to library-level (entire framework/library)
    return 'library'


def add_granularity_metadata(tags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Add granularity field to Library tags."""
    print("Adding granularity metadata...")

    for tag in tags:
        if tag.get('category') == 'Library':
            if 'granularity' not in tag:
                tag['granularity'] = classify_granularity(tag)
                print(f"  {tag['id']}: {tag['granularity']}")

    return tags


def calculate_aggregate_scores(tags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Calculate aggregate weighted scores from source-specific metrics.

    Formula: weighted_score = Σ(source_score * source_weight)
    """
    print("Calculating aggregate weighted scores...")

    for tag in tags:
        if 'sources' in tag and tag['sources']:
            total_score = 0.0
            for source in tag['sources']:
                total_score += source['score'] * source['weight']
            tag['weighted_score'] = total_score
            print(f"  {tag['id']}: {tag['weighted_score']:.3f}")
        elif 'weighted_score' not in tag:
            # Default score for tags without sources
            tag['weighted_score'] = 0.5

    return tags


def enrich_metadata(tags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enrich tags with additional metadata."""
    print("Enriching metadata...")

    for tag in tags:
        # Ensure all required fields exist
        if 'aliases' not in tag:
            tag['aliases'] = []
        if 'language_scope' not in tag:
            tag['language_scope'] = []

        # Add default source if missing
        if 'source' not in tag and 'sources' not in tag:
            tag['source'] = 'curated-list'

    return tags


def load_existing_tags(output_dir: Path, category: str) -> List[Dict[str, Any]]:
    """Load existing tags from YAML file if it exists."""
    output_file = output_dir / f"{category.lower()}.yaml"
    if output_file.exists():
        with open(output_file, 'r') as f:
            return yaml.safe_load(f) or []
    return []


def merge_with_existing_tags(new_tags: List[Dict[str, Any]], existing_tags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merge new tags with existing tags, intelligently combining metadata."""
    print("\nMerging with existing tags...")

    # Create map of existing tags by ID
    existing_map = {tag['id']: tag for tag in existing_tags}

    # Update or add new tags
    updated_count = 0
    added_count = 0

    for new_tag in new_tags:
        tag_id = new_tag['id']
        if tag_id in existing_map:
            # Merge with existing tag, preserving existing fields when new tag doesn't have them
            existing_tag = existing_map[tag_id]
            merged_tag = existing_tag.copy()

            # Update with new tag fields, but preserve certain existing fields if not in new tag
            for key, value in new_tag.items():
                if key in ['sources', 'weighted_score', 'aliases', 'language_scope']:
                    # Always update these from new collection
                    merged_tag[key] = value
                elif key == 'granularity':
                    # Preserve existing granularity if new tag doesn't have it
                    if value or 'granularity' not in existing_tag:
                        merged_tag[key] = value
                else:
                    # Update other fields
                    merged_tag[key] = value

            existing_map[tag_id] = merged_tag
            updated_count += 1
            print(f"  Updated: {tag_id}")
        else:
            # Add new tag
            existing_map[tag_id] = new_tag
            added_count += 1
            print(f"  Added: {tag_id}")

    print(f"  Total: {added_count} added, {updated_count} updated, {len(existing_map)} total")

    return list(existing_map.values())


def save_normalized_tags(tags: List[Dict[str, Any]], output_dir: Path, category: str, merge: bool = True):
    """Save normalized tags to YAML file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Merge with existing tags if requested
    if merge:
        existing_tags = load_existing_tags(output_dir, category)
        if existing_tags:
            tags = merge_with_existing_tags(tags, existing_tags)

    # Sort tags alphabetically by ID
    tags.sort(key=lambda t: t['id'])

    # Prepare output (remove internal fields if needed)
    output_tags = []
    for tag in tags:
        # Create clean tag dict with proper field order
        clean_tag = {
            'id': tag['id'],
            'name': tag['name'],
            'category': tag['category'],
        }

        if 'subcategory' in tag:
            clean_tag['subcategory'] = tag['subcategory']
        if 'description' in tag:
            clean_tag['description'] = tag['description']
        if tag.get('aliases'):
            clean_tag['aliases'] = tag['aliases']
        if tag.get('language_scope'):
            clean_tag['language_scope'] = tag['language_scope']
        if 'difficulty' in tag:
            clean_tag['difficulty'] = tag['difficulty']
        if 'granularity' in tag:
            clean_tag['granularity'] = tag['granularity']
        if 'weighted_score' in tag:
            clean_tag['weighted_score'] = round(tag['weighted_score'], 3)
        if 'sources' in tag:
            clean_tag['sources'] = tag['sources']
        if 'source' in tag:
            clean_tag['source'] = tag['source']

        output_tags.append(clean_tag)

    # Write to YAML
    output_file = output_dir / f"{category.lower()}.yaml"
    with open(output_file, 'w') as f:
        yaml.dump(output_tags, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"Saved {len(output_tags)} tags to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Enhanced tag normalization with alias expansion")
    parser.add_argument('--input', type=Path, required=True, help='Input JSON file with collected tags')
    parser.add_argument('--output-dir', type=Path, default=Path('taxonomy/tags'), help='Output directory')
    parser.add_argument('--category', default='Library', help='Tag category')
    parser.add_argument('--taxonomy', type=Path, default=Path('taxonomy.yaml'), help='Taxonomy definition file')
    parser.add_argument('--expand-aliases', action='store_true', help='Run automated alias expansion')
    parser.add_argument('--no-auto-approve', action='store_true', help='Disable auto-approval of high-confidence aliases')
    parser.add_argument('--merge', action='store_true', default=True, help='Merge with existing tags (default: True)')
    parser.add_argument('--no-merge', dest='merge', action='store_false', help='Replace existing tags instead of merging')

    args = parser.parse_args()

    print(f"\n{'='*70}")
    print(f"Enhanced Tag Normalization")
    print(f"{'='*70}\n")

    # Load data
    print(f"Loading tags from {args.input}...")
    tags = load_collected_tags(args.input)
    print(f"  Loaded {len(tags)} tags")

    # Normalize IDs
    print("\nNormalizing IDs...")
    for tag in tags:
        if 'id' not in tag:
            tag['id'] = normalize_id(tag['name'])
        tag['category'] = args.category

    # Deduplicate
    tags = deduplicate_tags(tags)

    # Expand aliases
    if args.expand_aliases:
        tags = expand_aliases_for_tags(tags, auto_approve=not args.no_auto_approve)

    # Add granularity metadata
    if args.category == 'Library':
        tags = add_granularity_metadata(tags)

    # Calculate aggregate scores
    tags = calculate_aggregate_scores(tags)

    # Enrich metadata
    tags = enrich_metadata(tags)

    # Save results
    print(f"\nSaving normalized tags...")
    save_normalized_tags(tags, args.output_dir, args.category, merge=args.merge)

    print(f"\n{'='*70}")
    print(f"Normalization complete!")
    print(f"  Total tags: {len(tags)}")
    print(f"  Output: {args.output_dir / args.category.lower()}.yaml")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    main()
