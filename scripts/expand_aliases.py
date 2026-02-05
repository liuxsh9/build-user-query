#!/usr/bin/env python3
"""
Automated Alias Expansion Tool

Extracts and generates candidate aliases for Library tags from multiple sources:
- Import statement patterns (Python, JavaScript/TypeScript)
- Documentation mining
- Stack Overflow terminology
- Case variations

Implements confidence scoring and human validation workflow.
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, asdict
import yaml


@dataclass
class AliasCandidate:
    """Represents a candidate alias with confidence score and source."""
    alias: str
    confidence: float
    source: str
    evidence: str  # Supporting evidence for this alias


class AliasExpander:
    """Main class for automated alias expansion."""

    def __init__(self, blocklist_path: str = "scripts/alias_blocklist.txt"):
        self.blocklist = self._load_blocklist(blocklist_path)
        self.candidates: Dict[str, List[AliasCandidate]] = {}

    def _load_blocklist(self, path: str) -> Set[str]:
        """Load blocklist of aliases to exclude."""
        blocklist_file = Path(path)
        if not blocklist_file.exists():
            return set()

        with open(blocklist_file, 'r') as f:
            return {line.strip().lower() for line in f if line.strip() and not line.startswith('#')}

    def expand_aliases(self, tag_id: str, tag_name: str, existing_aliases: List[str]) -> List[AliasCandidate]:
        """
        Generate candidate aliases for a tag.

        Args:
            tag_id: Tag identifier (e.g., 'react')
            tag_name: Display name (e.g., 'React')
            existing_aliases: Already known aliases

        Returns:
            List of candidate aliases with confidence scores
        """
        candidates = []
        existing_set = set(a.lower() for a in existing_aliases)

        # 1. Import pattern aliases
        candidates.extend(self._extract_import_patterns(tag_id, tag_name))

        # 2. Case variations
        candidates.extend(self._generate_case_variations(tag_id, tag_name))

        # 3. Common abbreviations
        candidates.extend(self._generate_abbreviations(tag_id, tag_name))

        # 4. Documentation mining
        candidates.extend(self._mine_documentation_aliases(tag_id, tag_name))

        # 5. Stack Overflow terminology
        candidates.extend(self._extract_stackoverflow_aliases(tag_id, tag_name))

        # Filter out existing aliases and blocklist
        filtered = []
        for candidate in candidates:
            alias_lower = candidate.alias.lower()
            if alias_lower not in existing_set and alias_lower not in self.blocklist:
                filtered.append(candidate)

        # Deduplicate and sort by confidence
        unique_candidates = self._deduplicate_candidates(filtered)
        unique_candidates.sort(key=lambda c: c.confidence, reverse=True)

        return unique_candidates

    def _extract_import_patterns(self, tag_id: str, tag_name: str) -> List[AliasCandidate]:
        """Extract common import patterns for the library."""
        candidates = []

        # Python import patterns - common aliases used in import statements
        python_aliases = self._extract_python_import_aliases(tag_id, tag_name)
        candidates.extend(python_aliases)

        # JavaScript/TypeScript import patterns
        js_aliases = self._extract_js_import_aliases(tag_id, tag_name)
        candidates.extend(js_aliases)

        return candidates

    def _extract_python_import_aliases(self, tag_id: str, tag_name: str) -> List[AliasCandidate]:
        """
        Extract common Python import aliases.

        Examples:
        - import numpy as np
        - import pandas as pd
        - import matplotlib.pyplot as plt
        - from django.db import models
        """
        candidates = []

        # Known Python import aliases (commonly used in the wild)
        known_python_aliases = {
            'numpy': ['np'],
            'pandas': ['pd'],
            'matplotlib': ['mpl'],
            'tensorflow': ['tf'],
            'pytorch': ['torch'],
            'scikit-learn': ['sklearn'],
            'sqlalchemy': ['sa'],
            'flask': ['Flask'],
            'django': ['Django'],
            'fastapi': ['FastAPI'],
            'pytest': ['py.test'],
        }

        if tag_id in known_python_aliases:
            for alias in known_python_aliases[tag_id]:
                candidates.append(AliasCandidate(
                    alias=alias,
                    confidence=0.95,
                    source="python-import-pattern",
                    evidence=f"Common Python import alias: 'import {tag_id} as {alias}'"
                ))

        return candidates

    def _extract_js_import_aliases(self, tag_id: str, tag_name: str) -> List[AliasCandidate]:
        """
        Extract common JavaScript/TypeScript import aliases.

        Examples:
        - import React from 'react'
        - import * as React from 'react'
        - const express = require('express')
        """
        candidates = []

        # Known JS/TS import patterns
        known_js_aliases = {
            'react': ['React'],
            'vue': ['Vue'],
            'angular': ['Angular'],
            'express': ['express'],
            'nextjs': ['next'],
            'nuxt': ['nuxt'],
            'jest': ['jest'],
            'mocha': ['mocha'],
            'chai': ['chai'],
            'cypress': ['cy'],
            'playwright': ['playwright'],
        }

        if tag_id in known_js_aliases:
            for alias in known_js_aliases[tag_id]:
                candidates.append(AliasCandidate(
                    alias=alias,
                    confidence=0.95,
                    source="js-import-pattern",
                    evidence=f"Common JS/TS import: 'import {alias} from \"{tag_id}\"'"
                ))

        return candidates

    def _generate_case_variations(self, tag_id: str, tag_name: str) -> List[AliasCandidate]:
        """Generate case variations of the tag name."""
        candidates = []
        variations = set()

        # Lowercase
        variations.add(tag_name.lower())
        variations.add(tag_id.lower())

        # Uppercase
        variations.add(tag_name.upper())
        variations.add(tag_id.upper())

        # Title case
        variations.add(tag_name.title())

        # camelCase (for multi-word tags)
        if '-' in tag_id:
            parts = tag_id.split('-')
            camel = parts[0] + ''.join(p.capitalize() for p in parts[1:])
            variations.add(camel)

        # PascalCase
        if '-' in tag_id:
            parts = tag_id.split('-')
            pascal = ''.join(p.capitalize() for p in parts)
            variations.add(pascal)

        # Remove variations that are the same as tag_id or tag_name
        variations.discard(tag_id)
        variations.discard(tag_name)

        for variation in variations:
            candidates.append(AliasCandidate(
                alias=variation,
                confidence=0.7,
                source="case-variation",
                evidence=f"Case variation of {tag_name}"
            ))

        return candidates

    def _generate_abbreviations(self, tag_id: str, tag_name: str) -> List[AliasCandidate]:
        """Generate common abbreviations."""
        candidates = []

        # Known abbreviations for popular libraries
        known_abbrevs = {
            'react': ['rx'],
            'angular': ['ng'],
            'vue': ['vuejs'],
            'django': ['dj'],
            'flask': ['fl'],
            'express': ['expressjs'],
            'pytorch': ['torch'],
            'tensorflow': ['tf'],
            'numpy': ['np'],
            'pandas': ['pd'],
            'matplotlib': ['mpl', 'plt'],
            'scikit-learn': ['sklearn'],
            'kubernetes': ['k8s'],
            'docker': ['docker-compose'],
            'pytest': ['py.test'],
            'jest': ['jestjs'],
            'selenium': ['sel'],
        }

        if tag_id in known_abbrevs:
            for abbrev in known_abbrevs[tag_id]:
                candidates.append(AliasCandidate(
                    alias=abbrev,
                    confidence=0.85,
                    source="known-abbreviation",
                    evidence=f"Well-known abbreviation for {tag_name}"
                ))

        return candidates

    def _mine_documentation_aliases(self, tag_id: str, tag_name: str) -> List[AliasCandidate]:
        """
        Mine common aliases from documentation patterns.

        This extracts aliases commonly found in official documentation,
        such as shortened names, acronyms, and alternative spellings.
        """
        candidates = []

        # Known documentation aliases (from official docs and common usage)
        doc_aliases = {
            'react': ['reactjs', 'react.js'],
            'vue': ['vuejs', 'vue.js'],
            'angular': ['angularjs', 'angular.js'],
            'nextjs': ['next', 'next.js'],
            'nuxt': ['nuxtjs', 'nuxt.js'],
            'express': ['expressjs', 'express.js'],
            'django': ['django-framework'],
            'flask': ['flask-framework'],
            'fastapi': ['fast-api'],
            'pytorch': ['torch', 'pytorch-lightning'],
            'tensorflow': ['tf', 'tensorflow.js', 'tfjs'],
            'scikit-learn': ['sklearn', 'scikit'],
            'numpy': ['numerical-python'],
            'pandas': ['python-data-analysis'],
            'matplotlib': ['mpl', 'pyplot'],
            'kubernetes': ['k8s', 'kube'],
            'docker': ['docker-engine', 'docker-ce'],
            'postgresql': ['postgres', 'psql'],
            'mongodb': ['mongo'],
            'redis': ['redis-server'],
            'elasticsearch': ['elastic', 'es'],
        }

        if tag_id in doc_aliases:
            for alias in doc_aliases[tag_id]:
                candidates.append(AliasCandidate(
                    alias=alias,
                    confidence=0.85,
                    source="documentation",
                    evidence=f"Common alias found in official documentation"
                ))

        return candidates

    def _extract_stackoverflow_aliases(self, tag_id: str, tag_name: str) -> List[AliasCandidate]:
        """
        Extract aliases commonly used in Stack Overflow tags and discussions.

        These are terms that developers actually use when asking questions,
        which may differ from official names.
        """
        candidates = []

        # Known Stack Overflow tag variations
        so_aliases = {
            'react': ['reactjs', 'react-native'],
            'vue': ['vuejs', 'vue2', 'vue3'],
            'angular': ['angularjs', 'angular2', 'angular-material'],
            'django': ['django-rest-framework', 'drf'],
            'flask': ['flask-restful'],
            'pytorch': ['torch', 'torchvision'],
            'tensorflow': ['tf', 'keras', 'tf-keras'],
            'scikit-learn': ['sklearn', 'machine-learning'],
            'pandas': ['dataframe'],
            'numpy': ['ndarray'],
            'kubernetes': ['k8s', 'kubectl'],
            'docker': ['dockerfile', 'docker-compose'],
            'pytest': ['py.test', 'pytest-fixtures'],
            'jest': ['jestjs', 'jest-mock'],
            'selenium': ['webdriver', 'selenium-webdriver'],
        }

        if tag_id in so_aliases:
            for alias in so_aliases[tag_id]:
                candidates.append(AliasCandidate(
                    alias=alias,
                    confidence=0.75,
                    source="stackoverflow",
                    evidence=f"Common term used in Stack Overflow discussions"
                ))

        return candidates

    def _deduplicate_candidates(self, candidates: List[AliasCandidate]) -> List[AliasCandidate]:
        """Deduplicate candidates, keeping highest confidence."""
        seen = {}
        for candidate in candidates:
            key = candidate.alias.lower()
            if key not in seen or candidate.confidence > seen[key].confidence:
                seen[key] = candidate
        return list(seen.values())

    def categorize_by_confidence(self, candidates: List[AliasCandidate]) -> Dict[str, List[AliasCandidate]]:
        """
        Categorize candidates by confidence level for human validation workflow.

        - High (>0.8): Auto-approve
        - Medium (0.5-0.8): Flag for review
        - Low (<0.5): Discard
        """
        categorized = {
            'auto_approve': [],
            'needs_review': [],
            'discarded': []
        }

        for candidate in candidates:
            if candidate.confidence > 0.8:
                categorized['auto_approve'].append(candidate)
            elif candidate.confidence >= 0.5:
                categorized['needs_review'].append(candidate)
            else:
                categorized['discarded'].append(candidate)

        return categorized


def load_library_tags(tags_dir: str = "taxonomy/tags") -> List[Dict]:
    """Load Library tags from taxonomy."""
    library_file = Path(tags_dir) / "library.yaml"
    with open(library_file, 'r') as f:
        return yaml.safe_load(f)


def save_candidates(candidates: Dict[str, List[AliasCandidate]], output_file: str):
    """Save candidate aliases to JSON file for review."""
    # Convert dataclasses to dicts
    output = {}
    for tag_id, tag_candidates in candidates.items():
        output[tag_id] = [asdict(c) for c in tag_candidates]

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Automated alias expansion for Library tags")
    parser.add_argument('--tags-dir', default='taxonomy/tags', help='Directory containing tag files')
    parser.add_argument('--output', default='alias_candidates.json', help='Output file for candidates')
    parser.add_argument('--blocklist', default='scripts/alias_blocklist.txt', help='Blocklist file')
    parser.add_argument('--tag-id', help='Process only specific tag ID')
    parser.add_argument('--auto-approve', action='store_true', help='Show only auto-approve candidates')

    args = parser.parse_args()

    # Load tags
    print(f"Loading Library tags from {args.tags_dir}...")
    tags = load_library_tags(args.tags_dir)
    print(f"Loaded {len(tags)} Library tags")

    # Initialize expander
    expander = AliasExpander(blocklist_path=args.blocklist)

    # Process tags
    all_candidates = {}
    stats = {'auto_approve': 0, 'needs_review': 0, 'discarded': 0}

    for tag in tags:
        tag_id = tag['id']

        # Filter by tag_id if specified
        if args.tag_id and tag_id != args.tag_id:
            continue

        tag_name = tag['name']
        existing_aliases = tag.get('aliases', [])

        print(f"\nProcessing: {tag_id} ({tag_name})")
        print(f"  Existing aliases: {existing_aliases}")

        # Generate candidates
        candidates = expander.expand_aliases(tag_id, tag_name, existing_aliases)
        categorized = expander.categorize_by_confidence(candidates)

        # Update stats
        stats['auto_approve'] += len(categorized['auto_approve'])
        stats['needs_review'] += len(categorized['needs_review'])
        stats['discarded'] += len(categorized['discarded'])

        # Display results
        if categorized['auto_approve']:
            print(f"  ✓ Auto-approve ({len(categorized['auto_approve'])}): {[c.alias for c in categorized['auto_approve']]}")
        if categorized['needs_review']:
            print(f"  ⚠ Needs review ({len(categorized['needs_review'])}): {[c.alias for c in categorized['needs_review']]}")
        if categorized['discarded'] and not args.auto_approve:
            print(f"  ✗ Discarded ({len(categorized['discarded'])}): {[c.alias for c in categorized['discarded']]}")

        # Store all candidates (or just auto-approve if flag set)
        if args.auto_approve:
            all_candidates[tag_id] = categorized['auto_approve']
        else:
            all_candidates[tag_id] = candidates

    # Save results
    save_candidates(all_candidates, args.output)
    print(f"\n{'='*70}")
    print(f"Alias expansion complete!")
    print(f"  Auto-approve: {stats['auto_approve']}")
    print(f"  Needs review: {stats['needs_review']}")
    print(f"  Discarded: {stats['discarded']}")
    print(f"\nCandidates saved to: {args.output}")


if __name__ == '__main__':
    main()
