#!/usr/bin/env python3
"""
Multi-Source Tag Collection Script

Collects Library tags from multiple data sources with weighted prioritization:
- Stack Overflow API (weight: 0.4)
- npm registry API (weight: 0.3)
- PyPI API (weight: 0.3)
- GitHub Topics API (weight: 0.2)
- Academic databases (weight: 0.1)

Each tag includes source-specific metrics and weighted scores.
"""

import argparse
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import urllib.request
import urllib.parse
import urllib.error


@dataclass
class SourceMetrics:
    """Metrics from a specific data source."""
    source: str
    weight: float
    score: float  # Normalized 0-1 score from this source
    raw_metrics: Dict[str, Any]  # Source-specific raw data
    collected_at: str


@dataclass
class LibraryTag:
    """Library tag with multi-source metadata."""
    name: str
    tag_id: str
    category: str = "Library"
    subcategory: str = ""
    sources: List[SourceMetrics] = None
    weighted_score: float = 0.0
    language_scope: List[str] = None
    aliases: List[str] = None

    def __post_init__(self):
        if self.sources is None:
            self.sources = []
        if self.language_scope is None:
            self.language_scope = []
        if self.aliases is None:
            self.aliases = []


class StackOverflowCollector:
    """Collect tags from Stack Overflow API."""

    BASE_URL = "https://api.stackexchange.com/2.3"
    WEIGHT = 0.4

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def collect_tags(self, subcategory: str, min_count: int = 1000) -> List[Dict[str, Any]]:
        """
        Collect library tags from Stack Overflow.

        Args:
            subcategory: Library subcategory (Web, Data, Infrastructure, Testing, Database)
            min_count: Minimum question count threshold

        Returns:
            List of tags with SO metrics
        """
        print(f"Collecting from Stack Overflow for {subcategory}...")

        # Map subcategories to SO tag filters
        tag_filters = {
            "Web": ["javascript", "python", "web", "framework", "react", "vue", "angular"],
            "Data": ["python", "data-science", "machine-learning", "pandas", "numpy"],
            "Infrastructure": ["docker", "kubernetes", "devops", "terraform", "ansible"],
            "Testing": ["testing", "unit-testing", "pytest", "jest", "selenium"],
            "Database": ["database", "orm", "sql", "mongodb", "postgresql"]
        }

        if subcategory not in tag_filters:
            print(f"Warning: No SO filter for subcategory '{subcategory}'")
            return []

        # For demo purposes, return mock data
        # In production, this would call the actual SO API
        mock_tags = self._get_mock_so_data(subcategory)

        print(f"  Collected {len(mock_tags)} tags from Stack Overflow")
        return mock_tags

    def _get_mock_so_data(self, subcategory: str) -> List[Dict[str, Any]]:
        """Mock Stack Overflow data for demonstration."""
        mock_data = {
            "Web": [
                {"name": "react", "count": 450000, "related": ["reactjs", "react-hooks"]},
                {"name": "vue.js", "count": 85000, "related": ["vuejs", "vue"]},
                {"name": "angular", "count": 280000, "related": ["angularjs", "angular2"]},
            ],
            "Data": [
                {"name": "pandas", "count": 120000, "related": ["dataframe", "python"]},
                {"name": "numpy", "count": 95000, "related": ["python", "array"]},
                {"name": "pytorch", "count": 45000, "related": ["deep-learning", "torch"]},
            ],
        }
        return mock_data.get(subcategory, [])


class NpmCollector:
    """Collect tags from npm registry."""

    BASE_URL = "https://registry.npmjs.org"
    WEIGHT = 0.3

    def collect_tags(self, subcategory: str, min_downloads: int = 100000) -> List[Dict[str, Any]]:
        """
        Collect JavaScript/TypeScript library tags from npm.

        Args:
            subcategory: Library subcategory
            min_downloads: Minimum weekly download threshold

        Returns:
            List of tags with npm metrics
        """
        print(f"Collecting from npm registry for {subcategory}...")

        # For demo purposes, return mock data
        mock_tags = self._get_mock_npm_data(subcategory)

        print(f"  Collected {len(mock_tags)} tags from npm")
        return mock_tags

    def _get_mock_npm_data(self, subcategory: str) -> List[Dict[str, Any]]:
        """Mock npm data for demonstration."""
        mock_data = {
            "Web": [
                {"name": "react", "downloads": 18000000, "version": "18.2.0"},
                {"name": "vue", "downloads": 3500000, "version": "3.3.4"},
                {"name": "express", "downloads": 25000000, "version": "4.18.2"},
            ],
            "Testing": [
                {"name": "jest", "downloads": 22000000, "version": "29.5.0"},
                {"name": "mocha", "downloads": 8000000, "version": "10.2.0"},
                {"name": "cypress", "downloads": 5000000, "version": "12.17.0"},
            ],
        }
        return mock_data.get(subcategory, [])


class PyPICollector:
    """Collect tags from PyPI (Python Package Index)."""

    BASE_URL = "https://pypi.org/pypi"
    WEIGHT = 0.3

    def collect_tags(self, subcategory: str, min_downloads: int = 50000) -> List[Dict[str, Any]]:
        """
        Collect Python library tags from PyPI.

        Args:
            subcategory: Library subcategory
            min_downloads: Minimum monthly download threshold

        Returns:
            List of tags with PyPI metrics
        """
        print(f"Collecting from PyPI for {subcategory}...")

        # For demo purposes, return mock data
        mock_tags = self._get_mock_pypi_data(subcategory)

        print(f"  Collected {len(mock_tags)} tags from PyPI")
        return mock_tags

    def _get_mock_pypi_data(self, subcategory: str) -> List[Dict[str, Any]]:
        """Mock PyPI data for demonstration."""
        mock_data = {
            "Web": [
                {"name": "django", "downloads": 5000000, "version": "4.2.3"},
                {"name": "flask", "downloads": 8000000, "version": "2.3.2"},
                {"name": "fastapi", "downloads": 12000000, "version": "0.100.0"},
            ],
            "Data": [
                {"name": "pandas", "downloads": 45000000, "version": "2.0.3"},
                {"name": "numpy", "downloads": 80000000, "version": "1.25.0"},
                {"name": "scikit-learn", "downloads": 35000000, "version": "1.3.0"},
            ],
        }
        return mock_data.get(subcategory, [])


class GitHubTopicsCollector:
    """Collect tags from GitHub Topics."""

    BASE_URL = "https://api.github.com"
    WEIGHT = 0.2

    def __init__(self, token: Optional[str] = None):
        self.token = token

    def collect_tags(self, subcategory: str, min_repos: int = 1000) -> List[Dict[str, Any]]:
        """
        Collect library tags from GitHub Topics.

        Args:
            subcategory: Library subcategory
            min_repos: Minimum repository count threshold

        Returns:
            List of tags with GitHub metrics
        """
        print(f"Collecting from GitHub Topics for {subcategory}...")

        # For demo purposes, return mock data
        mock_tags = self._get_mock_github_data(subcategory)

        print(f"  Collected {len(mock_tags)} tags from GitHub Topics")
        return mock_tags

    def _get_mock_github_data(self, subcategory: str) -> List[Dict[str, Any]]:
        """Mock GitHub data for demonstration."""
        mock_data = {
            "Web": [
                {"name": "react", "repos": 250000, "stars": 2100000},
                {"name": "vue", "repos": 180000, "stars": 450000},
                {"name": "nextjs", "repos": 95000, "stars": 110000},
            ],
            "Infrastructure": [
                {"name": "kubernetes", "repos": 85000, "stars": 105000},
                {"name": "docker", "repos": 120000, "stars": 95000},
                {"name": "terraform", "repos": 45000, "stars": 40000},
            ],
        }
        return mock_data.get(subcategory, [])


class MultiSourceCollector:
    """Orchestrates collection from multiple sources."""

    def __init__(self):
        self.so_collector = StackOverflowCollector()
        self.npm_collector = NpmCollector()
        self.pypi_collector = PyPICollector()
        self.github_collector = GitHubTopicsCollector()

    def collect_library_tags(self, subcategory: str) -> List[LibraryTag]:
        """
        Collect library tags from all sources and compute weighted scores.

        Args:
            subcategory: Library subcategory (Web, Data, Infrastructure, Testing, Database)

        Returns:
            List of LibraryTag objects with multi-source metrics
        """
        print(f"\n{'='*70}")
        print(f"Multi-Source Collection: Library/{subcategory}")
        print(f"{'='*70}\n")

        # Collect from all sources
        so_tags = self.so_collector.collect_tags(subcategory)
        npm_tags = self.npm_collector.collect_tags(subcategory)
        pypi_tags = self.pypi_collector.collect_tags(subcategory)
        github_tags = self.github_collector.collect_tags(subcategory)

        # Merge tags by name
        merged_tags = self._merge_sources(
            subcategory,
            so_tags,
            npm_tags,
            pypi_tags,
            github_tags
        )

        # Calculate weighted scores
        for tag in merged_tags:
            tag.weighted_score = self._calculate_weighted_score(tag)

        # Sort by weighted score
        merged_tags.sort(key=lambda t: t.weighted_score, reverse=True)

        print(f"\n{'='*70}")
        print(f"Collection Summary:")
        print(f"  Total unique tags: {len(merged_tags)}")
        print(f"  Tags from Stack Overflow: {len(so_tags)}")
        print(f"  Tags from npm: {len(npm_tags)}")
        print(f"  Tags from PyPI: {len(pypi_tags)}")
        print(f"  Tags from GitHub: {len(github_tags)}")
        print(f"{'='*70}\n")

        return merged_tags

    def _merge_sources(
        self,
        subcategory: str,
        so_tags: List[Dict],
        npm_tags: List[Dict],
        pypi_tags: List[Dict],
        github_tags: List[Dict]
    ) -> List[LibraryTag]:
        """Merge tags from different sources."""
        tag_map = {}
        timestamp = datetime.now().isoformat()

        # Process Stack Overflow tags
        for tag in so_tags:
            name = tag["name"]
            tag_id = name.lower().replace(".", "-").replace(" ", "-")

            if tag_id not in tag_map:
                tag_map[tag_id] = LibraryTag(
                    name=name,
                    tag_id=tag_id,
                    subcategory=subcategory
                )

            # Normalize SO score (question count)
            normalized_score = min(tag["count"] / 500000, 1.0)

            tag_map[tag_id].sources.append(SourceMetrics(
                source="stackoverflow",
                weight=StackOverflowCollector.WEIGHT,
                score=normalized_score,
                raw_metrics={"question_count": tag["count"], "related_tags": tag.get("related", [])},
                collected_at=timestamp
            ))

        # Process npm tags
        for tag in npm_tags:
            name = tag["name"]
            tag_id = name.lower().replace(".", "-").replace(" ", "-")

            if tag_id not in tag_map:
                tag_map[tag_id] = LibraryTag(
                    name=name,
                    tag_id=tag_id,
                    subcategory=subcategory,
                    language_scope=["javascript", "typescript"]
                )

            # Normalize npm score (weekly downloads)
            normalized_score = min(tag["downloads"] / 30000000, 1.0)

            tag_map[tag_id].sources.append(SourceMetrics(
                source="npm",
                weight=NpmCollector.WEIGHT,
                score=normalized_score,
                raw_metrics={"weekly_downloads": tag["downloads"], "version": tag["version"]},
                collected_at=timestamp
            ))

            if "javascript" not in tag_map[tag_id].language_scope:
                tag_map[tag_id].language_scope.extend(["javascript", "typescript"])

        # Process PyPI tags
        for tag in pypi_tags:
            name = tag["name"]
            tag_id = name.lower().replace(".", "-").replace(" ", "-")

            if tag_id not in tag_map:
                tag_map[tag_id] = LibraryTag(
                    name=name,
                    tag_id=tag_id,
                    subcategory=subcategory,
                    language_scope=["python"]
                )

            # Normalize PyPI score (monthly downloads)
            normalized_score = min(tag["downloads"] / 100000000, 1.0)

            tag_map[tag_id].sources.append(SourceMetrics(
                source="pypi",
                weight=PyPICollector.WEIGHT,
                score=normalized_score,
                raw_metrics={"monthly_downloads": tag["downloads"], "version": tag["version"]},
                collected_at=timestamp
            ))

            if "python" not in tag_map[tag_id].language_scope:
                tag_map[tag_id].language_scope.append("python")

        # Process GitHub tags
        for tag in github_tags:
            name = tag["name"]
            tag_id = name.lower().replace(".", "-").replace(" ", "-")

            if tag_id not in tag_map:
                tag_map[tag_id] = LibraryTag(
                    name=name,
                    tag_id=tag_id,
                    subcategory=subcategory
                )

            # Normalize GitHub score (repository count)
            normalized_score = min(tag["repos"] / 300000, 1.0)

            tag_map[tag_id].sources.append(SourceMetrics(
                source="github",
                weight=GitHubTopicsCollector.WEIGHT,
                score=normalized_score,
                raw_metrics={"repo_count": tag["repos"], "total_stars": tag["stars"]},
                collected_at=timestamp
            ))

        return list(tag_map.values())

    def _calculate_weighted_score(self, tag: LibraryTag) -> float:
        """
        Calculate weighted score from all sources.

        Formula: weighted_score = Σ(source_score * source_weight)
        """
        total_score = 0.0
        for source_metrics in tag.sources:
            total_score += source_metrics.score * source_metrics.weight
        return total_score


def save_collected_tags(tags: List[LibraryTag], output_path: Path):
    """Save collected tags to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert to dict format
    tags_data = []
    for tag in tags:
        tag_dict = {
            "name": tag.name,
            "id": tag.tag_id,
            "category": tag.category,
            "subcategory": tag.subcategory,
            "weighted_score": tag.weighted_score,
            "language_scope": tag.language_scope,
            "aliases": tag.aliases,
            "sources": [asdict(s) for s in tag.sources]
        }
        tags_data.append(tag_dict)

    with open(output_path, 'w') as f:
        json.dump(tags_data, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(tags)} tags to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Multi-source Library tag collection with weighted prioritization"
    )
    parser.add_argument(
        '--subcategory',
        required=True,
        choices=['Web', 'Data', 'Infrastructure', 'Testing', 'Database'],
        help='Library subcategory to collect'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('collected_tags_multisource.json'),
        help='Output JSON file path'
    )
    parser.add_argument(
        '--min-score',
        type=float,
        default=0.1,
        help='Minimum weighted score threshold (0.0-1.0)'
    )

    args = parser.parse_args()

    # Collect tags
    collector = MultiSourceCollector()
    tags = collector.collect_library_tags(args.subcategory)

    # Filter by minimum score
    filtered_tags = [t for t in tags if t.weighted_score >= args.min_score]

    print(f"Filtered to {len(filtered_tags)} tags with score >= {args.min_score}")

    # Display top tags
    print(f"\nTop 10 tags by weighted score:")
    for i, tag in enumerate(filtered_tags[:10], 1):
        sources_str = ", ".join([s.source for s in tag.sources])
        print(f"  {i}. {tag.name} (score: {tag.weighted_score:.3f}, sources: {sources_str})")

    # Save results
    save_collected_tags(filtered_tags, args.output)

    print(f"\nCollection complete!")
    print(f"Next step: Review {args.output} and run normalize_tags.py")


if __name__ == '__main__':
    main()
