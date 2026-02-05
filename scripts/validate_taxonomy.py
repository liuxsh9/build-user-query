#!/usr/bin/env python3
"""
Taxonomy Validation Script

Validates the capability taxonomy for:
- Category orthogonality
- Tag uniqueness
- Schema compliance
- Referential integrity
- Metadata quality
- Distribution balance

Generates a comprehensive validation report.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict
import yaml


class ValidationReport:
    """Collects validation errors, warnings, and statistics."""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {}

    def add_error(self, message: str):
        self.errors.append(message)

    def add_warning(self, message: str):
        self.warnings.append(message)

    def add_stat(self, key: str, value: Any):
        self.stats[key] = value

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def print_report(self):
        """Print formatted validation report."""
        print("\n" + "=" * 70)
        print("TAXONOMY VALIDATION REPORT")
        print("=" * 70)

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("\n✓ No errors found")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        else:
            print("\n✓ No warnings")

        if self.stats:
            print(f"\n📊 STATISTICS:")
            for key, value in self.stats.items():
                print(f"  {key}: {value}")

        print("\n" + "=" * 70)


def load_taxonomy(taxonomy_path: Path) -> Dict[str, Any]:
    """Load taxonomy definition."""
    with open(taxonomy_path, 'r') as f:
        return yaml.safe_load(f)


def load_tags(tags_dir: Path) -> List[Dict[str, Any]]:
    """Load all tags from YAML files in tags directory."""
    all_tags = []

    for yaml_file in tags_dir.glob("*.yaml"):
        with open(yaml_file, 'r') as f:
            tags = yaml.safe_load(f)
            if tags:
                all_tags.extend(tags)

    return all_tags


def validate_category_orthogonality(tags: List[Dict[str, Any]], report: ValidationReport):
    """Ensure no tag appears in multiple categories."""
    print("Validating category orthogonality...")

    tag_id_to_categories = defaultdict(list)

    for tag in tags:
        tag_id = tag.get("id")
        category = tag.get("category")
        if tag_id and category:
            tag_id_to_categories[tag_id].append(category)

    for tag_id, categories in tag_id_to_categories.items():
        if len(categories) > 1:
            report.add_error(f"Tag '{tag_id}' appears in multiple categories: {categories}")


def validate_tag_uniqueness(tags: List[Dict[str, Any]], report: ValidationReport):
    """Ensure tag IDs, aliases, and names are unique."""
    print("Validating tag uniqueness...")

    # Check ID uniqueness
    id_counts = defaultdict(int)
    for tag in tags:
        tag_id = tag.get("id")
        if tag_id:
            id_counts[tag_id] += 1

    for tag_id, count in id_counts.items():
        if count > 1:
            report.add_error(f"Duplicate tag ID: '{tag_id}' appears {count} times")

    # Check alias conflicts across different tags
    alias_to_tags = defaultdict(set)
    for tag in tags:
        tag_id = tag.get("id")
        for alias in tag.get("aliases", []):
            alias_to_tags[alias].add(tag_id)

    for alias, tag_ids in alias_to_tags.items():
        if len(tag_ids) > 1:
            report.add_warning(f"Alias '{alias}' used by multiple tags: {sorted(tag_ids)}")

    # Check name uniqueness within category
    category_names = defaultdict(list)
    for tag in tags:
        category = tag.get("category")
        name = tag.get("name")
        if category and name:
            category_names[category].append(name)

    for category, names in category_names.items():
        name_counts = defaultdict(int)
        for name in names:
            name_counts[name] += 1

        for name, count in name_counts.items():
            if count > 1:
                report.add_error(f"Duplicate name '{name}' in category '{category}' ({count} times)")


def validate_schema_compliance(tags: List[Dict[str, Any]], taxonomy: Dict[str, Any], report: ValidationReport):
    """Validate that all tags comply with schema requirements."""
    print("Validating schema compliance...")

    required_fields = ["id", "name", "category"]
    valid_difficulties = ["basic", "intermediate", "advanced"]

    # Get hierarchical categories
    hierarchical_categories = set()
    for cat in taxonomy.get("categories", []):
        if cat.get("hierarchical"):
            hierarchical_categories.add(cat["name"])

    for tag in tags:
        tag_id = tag.get("id", "unknown")

        # Check required fields
        for field in required_fields:
            if field not in tag:
                report.add_error(f"Tag '{tag_id}' missing required field: {field}")

        # Check difficulty enum
        if "difficulty" in tag:
            if tag["difficulty"] not in valid_difficulties:
                report.add_error(f"Tag '{tag_id}' has invalid difficulty: {tag['difficulty']}")

        # Check hierarchical categories have subcategory
        category = tag.get("category")
        if category in hierarchical_categories:
            if "subcategory" not in tag:
                report.add_error(f"Tag '{tag_id}' in hierarchical category '{category}' missing subcategory")


def validate_referential_integrity(tags: List[Dict[str, Any]], taxonomy: Dict[str, Any], report: ValidationReport):
    """Validate all references between taxonomy elements."""
    print("Validating referential integrity...")

    # Build valid category and subcategory sets
    valid_categories = set()
    valid_subcategories = defaultdict(set)

    for cat in taxonomy.get("categories", []):
        cat_name = cat["name"]
        valid_categories.add(cat_name)

        for subcat in cat.get("subcategories", []):
            valid_subcategories[cat_name].add(subcat["name"])

    # Build set of all tag IDs
    all_tag_ids = {tag.get("id") for tag in tags if tag.get("id")}

    # Build set of all language tag IDs
    language_tag_ids = {tag.get("id") for tag in tags if tag.get("category") == "Language"}

    for tag in tags:
        tag_id = tag.get("id", "unknown")

        # Validate category exists
        category = tag.get("category")
        if category and category not in valid_categories:
            report.add_error(f"Tag '{tag_id}' has invalid category: {category}")

        # Validate subcategory exists
        if "subcategory" in tag:
            subcategory = tag["subcategory"]
            if category and subcategory not in valid_subcategories.get(category, set()):
                report.add_error(f"Tag '{tag_id}' has invalid subcategory '{subcategory}' for category '{category}'")

        # Validate related_tags exist
        for related_id in tag.get("related_tags", []):
            if related_id not in all_tag_ids:
                report.add_error(f"Tag '{tag_id}' references non-existent related tag: {related_id}")

        # Validate language_scope references valid languages
        for lang in tag.get("language_scope", []):
            if lang not in language_tag_ids:
                report.add_warning(f"Tag '{tag_id}' references unknown language in language_scope: {lang}")


def validate_metadata_quality(tags: List[Dict[str, Any]], report: ValidationReport):
    """Check metadata quality standards."""
    print("Validating metadata quality...")

    for tag in tags:
        tag_id = tag.get("id", "unknown")

        # Check description length
        if "description" in tag:
            desc_len = len(tag["description"])
            if desc_len > 200:
                report.add_warning(f"Tag '{tag_id}' has long description ({desc_len} chars)")

        # Check aliases are lowercase
        for alias in tag.get("aliases", []):
            if alias != alias.lower():
                report.add_warning(f"Tag '{tag_id}' has non-lowercase alias: {alias}")


def validate_distribution(tags: List[Dict[str, Any]], report: ValidationReport):
    """Check tag distribution across categories and subcategories."""
    print("Validating distribution...")

    # Count tags per category
    category_counts = defaultdict(int)
    subcategory_counts = defaultdict(lambda: defaultdict(int))

    for tag in tags:
        category = tag.get("category")
        if category:
            category_counts[category] += 1

            subcategory = tag.get("subcategory")
            if subcategory:
                subcategory_counts[category][subcategory] += 1

    # Check for empty categories
    for category, count in category_counts.items():
        if count == 0:
            report.add_error(f"Category '{category}' has no tags")

    # Check for imbalanced subcategories
    for category, subcats in subcategory_counts.items():
        total = sum(subcats.values())
        for subcat, count in subcats.items():
            percentage = (count / total) * 100 if total > 0 else 0
            if percentage > 80:
                report.add_warning(f"Subcategory '{category}/{subcat}' has {percentage:.1f}% of tags (imbalanced)")

    # Add statistics
    report.add_stat("Total tags", len(tags))
    for category, count in sorted(category_counts.items()):
        report.add_stat(f"  {category}", count)


def main():
    parser = argparse.ArgumentParser(
        description="Validate capability taxonomy"
    )
    parser.add_argument(
        '--taxonomy',
        type=Path,
        default=Path('taxonomy.yaml'),
        help='Path to taxonomy.yaml'
    )
    parser.add_argument(
        '--tags-dir',
        type=Path,
        default=Path('taxonomy/tags'),
        help='Directory containing tag YAML files'
    )

    args = parser.parse_args()

    # Load taxonomy and tags
    print(f"Loading taxonomy from {args.taxonomy}...")
    taxonomy = load_taxonomy(args.taxonomy)

    print(f"Loading tags from {args.tags_dir}...")
    tags = load_tags(args.tags_dir)
    print(f"Loaded {len(tags)} tags\n")

    # Create report
    report = ValidationReport()

    # Run validations
    validate_category_orthogonality(tags, report)
    validate_tag_uniqueness(tags, report)
    validate_schema_compliance(tags, taxonomy, report)
    validate_referential_integrity(tags, taxonomy, report)
    validate_metadata_quality(tags, report)
    validate_distribution(tags, report)

    # Print report
    report.print_report()

    # Exit with appropriate code
    if report.has_errors():
        print("\n❌ Validation failed with errors")
        sys.exit(1)
    else:
        print("\n✅ Validation passed")
        sys.exit(0)


if __name__ == '__main__':
    main()
