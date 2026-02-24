#!/usr/bin/env python3
"""
Inter-Annotator Agreement (IAA) Calculator for Taxonomy v2.0

Computes Fleiss' kappa for multi-rater agreement across all 9 taxonomy categories.
Supports both multi-select (Language, Domain, Concept, Task, Constraint, Agentic)
and single-select (Context, Difficulty, Intent) categories.

Usage:
    python3 scripts/compute_iaa.py data/iaa/annotations_A1.yaml data/iaa/annotations_A2.yaml data/iaa/annotations_A3.yaml
    python3 scripts/compute_iaa.py data/iaa/annotations_*.yaml --report-dir data/iaa/reports
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml


# ──────────────────────────────────────────────────────────
# Fleiss' Kappa Implementation
# ──────────────────────────────────────────────────────────

def fleiss_kappa(matrix):
    """
    Compute Fleiss' kappa for a rating matrix.

    Args:
        matrix: list of dicts, where each dict maps category -> count of raters
                who assigned that category for a given subject.
                e.g., [{"beginner": 2, "intermediate": 1}, ...]

    Returns:
        kappa value (float), or None if undefined (all raters agree perfectly
        and there's no chance agreement variance).
    """
    if not matrix:
        return None

    n_subjects = len(matrix)
    all_categories = set()
    for row in matrix:
        all_categories.update(row.keys())
    categories = sorted(all_categories)

    if len(categories) <= 1:
        return 1.0  # perfect agreement (only one category used)

    # n = number of raters per subject (should be consistent)
    n_raters = sum(matrix[0].values())
    if n_raters < 2:
        return None

    # Build numeric matrix: subjects × categories
    table = []
    for row in matrix:
        table.append([row.get(cat, 0) for cat in categories])

    # P_i: proportion of agreeing pairs for subject i
    P_i_values = []
    for row in table:
        n = sum(row)
        if n < 2:
            continue
        P_i = (sum(x * x for x in row) - n) / (n * (n - 1))
        P_i_values.append(P_i)

    if not P_i_values:
        return None

    P_bar = sum(P_i_values) / len(P_i_values)

    # P_j: proportion of all assignments to category j
    total_assignments = sum(sum(row) for row in table)
    p_j_values = []
    for j in range(len(categories)):
        col_sum = sum(row[j] for row in table)
        p_j_values.append(col_sum / total_assignments)

    P_e_bar = sum(p_j ** 2 for p_j in p_j_values)

    if abs(1.0 - P_e_bar) < 1e-10:
        # Perfect chance agreement — kappa undefined
        return 1.0 if abs(P_bar - 1.0) < 1e-10 else None

    kappa = (P_bar - P_e_bar) / (1.0 - P_e_bar)
    return kappa


# ──────────────────────────────────────────────────────────
# Data Loading
# ──────────────────────────────────────────────────────────

def load_annotations(filepath):
    """Load a single annotator's YAML file."""
    with open(filepath) as f:
        data = yaml.safe_load(f)

    annotator_id = data.get("annotator_id", Path(filepath).stem)
    annotations = {}
    for item in data.get("annotations", []):
        sid = item["sample_id"]
        annotations[sid] = {
            "language": set(item.get("language") or []),
            "domain": set(item.get("domain") or []),
            "concept": set(item.get("concept") or []),
            "task": set(item.get("task") or []),
            "constraint": set(item.get("constraint") or []),
            "agentic": set(item.get("agentic") or []),
            "context": item.get("context", ""),
            "difficulty": item.get("difficulty", ""),
            "intent": item.get("intent", ""),
        }
    return annotator_id, annotations


def load_taxonomy_tags(tags_dir="taxonomy/tags"):
    """Load all valid tag IDs from the taxonomy."""
    tags_by_category = {}
    tags_dir = Path(tags_dir)
    for yaml_file in sorted(tags_dir.glob("*.yaml")):
        if "removed" in yaml_file.name:
            continue
        with open(yaml_file) as f:
            tags = yaml.safe_load(f) or []
        for tag in tags:
            cat = tag.get("category", "").lower().replace(" ", "-")
            cat_key = cat.lower()
            if cat_key not in tags_by_category:
                tags_by_category[cat_key] = set()
            tags_by_category[cat_key].add(tag["id"])
    return tags_by_category


# ──────────────────────────────────────────────────────────
# IAA Computation
# ──────────────────────────────────────────────────────────

MULTI_SELECT = ["language", "domain", "concept", "task", "constraint", "agentic"]
SINGLE_SELECT = ["context", "difficulty", "intent"]


def compute_single_select_kappa(all_annotations, category, sample_ids):
    """
    Compute Fleiss' kappa for a single-select category.

    For each sample, create a row: {label: count_of_raters_who_chose_it}
    """
    matrix = []
    for sid in sample_ids:
        row = Counter()
        for annotator_data in all_annotations.values():
            if sid in annotator_data:
                label = annotator_data[sid][category]
                if label:  # skip empty
                    row[label] += 1
        if sum(row.values()) >= 2:  # need at least 2 raters
            matrix.append(dict(row))

    if not matrix:
        return None, 0
    return fleiss_kappa(matrix), len(matrix)


def compute_multi_select_kappa(all_annotations, category, sample_ids, valid_tags=None):
    """
    Compute Fleiss' kappa for a multi-select category.

    For each tag in the category, create a binary presence/absence matrix
    across all samples, then compute kappa for each tag and average.

    Returns: (average_kappa, per_tag_kappas dict, n_tags_evaluated)
    """
    # Collect all tags used across annotators for this category
    all_tags = set()
    for annotator_data in all_annotations.values():
        for sid in sample_ids:
            if sid in annotator_data:
                all_tags.update(annotator_data[sid][category])

    if not all_tags:
        return None, {}, 0

    per_tag_kappas = {}
    for tag in sorted(all_tags):
        # For this tag: binary matrix across samples
        # Each sample is a row: {"present": n_raters_yes, "absent": n_raters_no}
        matrix = []
        for sid in sample_ids:
            present = 0
            absent = 0
            for annotator_data in all_annotations.values():
                if sid in annotator_data:
                    if tag in annotator_data[sid][category]:
                        present += 1
                    else:
                        absent += 1
            if present + absent >= 2:
                matrix.append({"present": present, "absent": absent})

        if matrix:
            k = fleiss_kappa(matrix)
            if k is not None:
                per_tag_kappas[tag] = k

    if not per_tag_kappas:
        return None, per_tag_kappas, 0

    avg_kappa = sum(per_tag_kappas.values()) / len(per_tag_kappas)
    return avg_kappa, per_tag_kappas, len(per_tag_kappas)


def compute_confusion_matrix(all_annotations, category, sample_ids):
    """
    Compute pairwise confusion matrix for single-select categories.
    Returns a dict of {(label_a, label_b): count} for disagreements.
    """
    annotator_ids = list(all_annotations.keys())
    confusion = Counter()
    total_pairs = 0
    agree_pairs = 0

    for sid in sample_ids:
        labels = []
        for aid in annotator_ids:
            if sid in all_annotations[aid]:
                label = all_annotations[aid][sid][category]
                if label:
                    labels.append(label)

        # Count all pairwise comparisons
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                total_pairs += 1
                if labels[i] == labels[j]:
                    agree_pairs += 1
                else:
                    pair = tuple(sorted([labels[i], labels[j]]))
                    confusion[pair] += 1

    return confusion, total_pairs, agree_pairs


def compute_difficulty_stratified_kappa(all_annotations, sample_ids, difficulty_ground_truth=None):
    """
    Compute kappa for each difficulty level stratum.
    Uses majority vote from annotators to determine difficulty if no ground truth.
    """
    # Determine difficulty per sample by majority vote
    difficulty_map = {}
    for sid in sample_ids:
        votes = Counter()
        for annotator_data in all_annotations.values():
            if sid in annotator_data:
                d = annotator_data[sid]["difficulty"]
                if d:
                    votes[d] += 1
        if votes:
            difficulty_map[sid] = votes.most_common(1)[0][0]

    # Stratify
    strata = defaultdict(list)
    for sid, diff in difficulty_map.items():
        strata[diff].append(sid)

    results = {}
    for diff_level in ["beginner", "intermediate", "advanced", "expert"]:
        stratum_sids = strata.get(diff_level, [])
        if len(stratum_sids) < 3:
            results[diff_level] = {"kappa": None, "n_samples": len(stratum_sids),
                                   "note": "Too few samples for reliable κ"}
            continue

        # Compute kappa across all categories for this stratum
        stratum_kappas = {}
        for cat in SINGLE_SELECT:
            k, n = compute_single_select_kappa(all_annotations, cat, stratum_sids)
            stratum_kappas[cat] = k
        for cat in MULTI_SELECT:
            k, _, _ = compute_multi_select_kappa(all_annotations, cat, stratum_sids)
            stratum_kappas[cat] = k

        results[diff_level] = {"kappas": stratum_kappas, "n_samples": len(stratum_sids)}

    return results


def find_disagreement_samples(all_annotations, category, sample_ids):
    """Find samples where annotators disagree on a single-select category."""
    disagreements = []
    annotator_ids = list(all_annotations.keys())

    for sid in sample_ids:
        labels = {}
        for aid in annotator_ids:
            if sid in all_annotations[aid]:
                label = all_annotations[aid][sid][category]
                if label:
                    labels[aid] = label

        unique_labels = set(labels.values())
        if len(unique_labels) > 1:
            disagreements.append({
                "sample_id": sid,
                "labels": labels,
            })

    return disagreements


# ──────────────────────────────────────────────────────────
# Report Generation
# ──────────────────────────────────────────────────────────

KAPPA_THRESHOLDS = {
    "excellent": 0.8,
    "acceptable": 0.7,
    "needs_improvement": 0.6,
}


def classify_kappa(k):
    if k is None:
        return "undefined"
    if k >= KAPPA_THRESHOLDS["excellent"]:
        return "excellent"
    if k >= KAPPA_THRESHOLDS["acceptable"]:
        return "acceptable"
    if k >= KAPPA_THRESHOLDS["needs_improvement"]:
        return "needs_improvement"
    return "unacceptable"


def format_kappa(k):
    if k is None:
        return "N/A"
    return f"{k:.3f}"


def generate_report(all_annotations, sample_ids, report_dir=None):
    """Generate the full IAA report."""
    n_annotators = len(all_annotations)
    n_samples = len(sample_ids)

    lines = []
    lines.append("=" * 70)
    lines.append("INTER-ANNOTATOR AGREEMENT (IAA) REPORT")
    lines.append(f"Taxonomy v2.0 | {n_annotators} annotators | {n_samples} samples")
    lines.append("=" * 70)
    lines.append("")

    # ── Summary Table ──
    lines.append("## Category-Level Kappa Summary")
    lines.append("")
    lines.append(f"{'Category':<15} {'Type':<15} {'κ':>8} {'Status':<18} {'Details'}")
    lines.append("-" * 80)

    all_kappas = {}
    all_details = {}

    for cat in SINGLE_SELECT:
        k, n = compute_single_select_kappa(all_annotations, cat, sample_ids)
        status = classify_kappa(k)
        all_kappas[cat] = k
        lines.append(f"{cat:<15} {'single-select':<15} {format_kappa(k):>8} {status:<18} n={n} samples")

    for cat in MULTI_SELECT:
        avg_k, per_tag, n_tags = compute_multi_select_kappa(all_annotations, cat, sample_ids)
        all_kappas[cat] = avg_k
        all_details[cat] = per_tag
        status = classify_kappa(avg_k)
        lines.append(f"{cat:<15} {'multi-select':<15} {format_kappa(avg_k):>8} {status:<18} avg over {n_tags} tags")

    lines.append("")

    # ── Overall Score ──
    valid_kappas = [k for k in all_kappas.values() if k is not None]
    overall = sum(valid_kappas) / len(valid_kappas) if valid_kappas else None
    lines.append(f"Overall average κ: {format_kappa(overall)}")
    lines.append(f"Pass threshold: κ ≥ 0.7 for all categories")
    lines.append("")

    failing = [cat for cat, k in all_kappas.items()
               if k is not None and k < KAPPA_THRESHOLDS["acceptable"]]
    if failing:
        lines.append(f"⚠️  FAILING categories (κ < 0.7): {', '.join(failing)}")
    else:
        lines.append("✅ All categories pass κ ≥ 0.7 threshold")
    lines.append("")

    # ── Confusion Matrices for Single-Select ──
    lines.append("=" * 70)
    lines.append("## Confusion Analysis (Single-Select Categories)")
    lines.append("")

    for cat in SINGLE_SELECT:
        confusion, total_pairs, agree_pairs = compute_confusion_matrix(
            all_annotations, cat, sample_ids
        )
        pct = (agree_pairs / total_pairs * 100) if total_pairs > 0 else 0
        lines.append(f"### {cat.title()}")
        lines.append(f"  Agreement: {agree_pairs}/{total_pairs} pairs ({pct:.1f}%)")
        if confusion:
            lines.append(f"  Most confused pairs:")
            for pair, count in confusion.most_common(5):
                lines.append(f"    {pair[0]} ↔ {pair[1]}: {count} disagreements")
        lines.append("")

    # ── Per-Tag Kappas for Multi-Select ──
    lines.append("=" * 70)
    lines.append("## Per-Tag Kappa Details (Multi-Select Categories)")
    lines.append("")

    for cat in MULTI_SELECT:
        if cat in all_details and all_details[cat]:
            lines.append(f"### {cat.title()}")
            # Sort by kappa ascending (worst first)
            sorted_tags = sorted(all_details[cat].items(), key=lambda x: x[1])
            for tag, k in sorted_tags:
                status = classify_kappa(k)
                marker = "⚠️" if k < KAPPA_THRESHOLDS["acceptable"] else "  "
                lines.append(f"  {marker} {tag:<35} κ={k:.3f}  ({status})")
            lines.append("")

    # ── Difficulty-Stratified Analysis ──
    lines.append("=" * 70)
    lines.append("## Difficulty-Stratified Kappa")
    lines.append("")

    strat_results = compute_difficulty_stratified_kappa(all_annotations, sample_ids)
    for diff_level in ["beginner", "intermediate", "advanced", "expert"]:
        result = strat_results.get(diff_level, {})
        n = result.get("n_samples", 0)
        lines.append(f"### {diff_level} (n={n})")
        if "kappas" in result:
            for cat, k in result["kappas"].items():
                lines.append(f"  {cat:<15} κ={format_kappa(k)}")
        elif "note" in result:
            lines.append(f"  {result['note']}")
        lines.append("")

    # ── Disagreement Samples ──
    lines.append("=" * 70)
    lines.append("## Disagreement Samples (for guideline updates)")
    lines.append("")

    for cat in SINGLE_SELECT:
        disagreements = find_disagreement_samples(all_annotations, cat, sample_ids)
        if disagreements:
            lines.append(f"### {cat.title()} ({len(disagreements)} disagreements)")
            for d in disagreements:
                labels_str = ", ".join(f"{aid}={lbl}" for aid, lbl in d["labels"].items())
                lines.append(f"  {d['sample_id']}: {labels_str}")
            lines.append("")

    report_text = "\n".join(lines)

    # Output
    print(report_text)

    if report_dir:
        report_dir = Path(report_dir)
        report_dir.mkdir(parents=True, exist_ok=True)

        # Save text report
        report_path = report_dir / "iaa_report.txt"
        with open(report_path, "w") as f:
            f.write(report_text)
        print(f"\nReport saved to: {report_path}")

        # Save JSON data
        json_data = {
            "n_annotators": n_annotators,
            "n_samples": n_samples,
            "category_kappas": {k: v for k, v in all_kappas.items()},
            "overall_kappa": overall,
            "per_tag_kappas": {k: v for k, v in all_details.items()},
            "passing": len(failing) == 0,
            "failing_categories": failing,
        }
        json_path = report_dir / "iaa_results.json"
        with open(json_path, "w") as f:
            json.dump(json_data, f, indent=2)
        print(f"JSON results saved to: {json_path}")

    return all_kappas, overall


# ──────────────────────────────────────────────────────────
# Validation
# ──────────────────────────────────────────────────────────

def validate_annotations(all_annotations, tags_by_category):
    """Validate that all annotation tag IDs exist in the taxonomy."""
    errors = []
    category_to_tag_key = {
        "language": "language",
        "domain": "domain",
        "concept": "concept",
        "task": "task",
        "constraint": "constraint",
        "agentic": "agentic",
        "context": "context",
        "difficulty": "difficulty",
        "intent": "intent",
    }

    for annotator_id, annotations in all_annotations.items():
        for sid, ann in annotations.items():
            for cat in MULTI_SELECT:
                tag_key = category_to_tag_key[cat]
                valid = tags_by_category.get(tag_key, set())
                for tag in ann[cat]:
                    if valid and tag not in valid:
                        errors.append(f"[{annotator_id}] {sid}.{cat}: unknown tag '{tag}'")

            for cat in SINGLE_SELECT:
                tag_key = category_to_tag_key[cat]
                valid = tags_by_category.get(tag_key, set())
                val = ann[cat]
                if val and valid and val not in valid:
                    errors.append(f"[{annotator_id}] {sid}.{cat}: unknown tag '{val}'")

    return errors


# ──────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Compute Inter-Annotator Agreement (Fleiss' κ) for taxonomy annotations"
    )
    parser.add_argument(
        "annotation_files", nargs="+",
        help="YAML annotation files (one per annotator)"
    )
    parser.add_argument(
        "--report-dir", default=None,
        help="Directory to save report files (default: print to stdout only)"
    )
    parser.add_argument(
        "--tags-dir", default="taxonomy/tags",
        help="Directory containing taxonomy tag YAML files"
    )
    parser.add_argument(
        "--validate", action="store_true", default=True,
        help="Validate tag IDs against taxonomy (default: True)"
    )
    parser.add_argument(
        "--no-validate", action="store_false", dest="validate",
        help="Skip tag ID validation"
    )

    args = parser.parse_args()

    if len(args.annotation_files) < 2:
        print("Error: Need at least 2 annotator files to compute agreement.", file=sys.stderr)
        sys.exit(1)

    # Load annotations
    all_annotations = {}
    for filepath in args.annotation_files:
        aid, anns = load_annotations(filepath)
        if aid in all_annotations:
            print(f"Warning: Duplicate annotator ID '{aid}', using filename as ID",
                  file=sys.stderr)
            aid = Path(filepath).stem
        all_annotations[aid] = anns
        print(f"Loaded {len(anns)} annotations from {aid} ({filepath})")

    # Get common sample IDs
    all_sample_sets = [set(anns.keys()) for anns in all_annotations.values()]
    sample_ids = sorted(set.intersection(*all_sample_sets))
    print(f"\nCommon samples across all annotators: {len(sample_ids)}")

    if not sample_ids:
        print("Error: No common samples found across annotators.", file=sys.stderr)
        sys.exit(1)

    # Validate
    if args.validate:
        tags_dir = Path(args.tags_dir)
        if tags_dir.exists():
            tags_by_category = load_taxonomy_tags(str(tags_dir))
            errors = validate_annotations(all_annotations, tags_by_category)
            if errors:
                print(f"\n⚠️  Validation warnings ({len(errors)}):", file=sys.stderr)
                for e in errors[:20]:
                    print(f"  {e}", file=sys.stderr)
                if len(errors) > 20:
                    print(f"  ... and {len(errors) - 20} more", file=sys.stderr)

    # Generate report
    print()
    kappas, overall = generate_report(all_annotations, sample_ids, args.report_dir)

    # Exit code
    failing = [cat for cat, k in kappas.items()
               if k is not None and k < KAPPA_THRESHOLDS["acceptable"]]
    sys.exit(1 if failing else 0)


if __name__ == "__main__":
    main()
