#!/usr/bin/env python3
"""
Optimize Constraint taxonomy tags for objectivity and verifiability.
Removes subjective tags, merges performance tags, adds objective constraints.
"""

import yaml
from pathlib import Path

CONSTRAINT_FILE = Path("taxonomy/tags/constraint.yaml")

def load_constraints():
    """Load constraint tags from YAML."""
    with open(CONSTRAINT_FILE, 'r') as f:
        return yaml.safe_load(f)

def save_constraints(tags):
    """Save constraint tags to YAML."""
    with open(CONSTRAINT_FILE, 'w') as f:
        yaml.dump(tags, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

def remove_tag_by_id(tags, tag_id):
    """Remove a tag by its ID."""
    return [tag for tag in tags if tag['id'] != tag_id]

def main():
    tags = load_constraints()
    original_count = len(tags)
    print(f"Original tag count: {original_count}")

    # Phase 1: Remove subjective tags
    print("\n=== Phase 1: Removing subjective tags ===")
    subjective_tags = ['readable', 'maintainable', 'testable']
    for tag_id in subjective_tags:
        tags = remove_tag_by_id(tags, tag_id)
        print(f"  Removed: {tag_id}")

    # Phase 2: Merge performance tags
    print("\n=== Phase 2: Merging performance tags ===")
    performance_tags = ['high-performance', 'low-latency', 'memory-efficient']
    for tag_id in performance_tags:
        tags = remove_tag_by_id(tags, tag_id)
        print(f"  Removed: {tag_id}")

    # Add unified performance-optimized tag
    performance_optimized = {
        'id': 'performance-optimized',
        'name': 'Performance Optimized',
        'category': 'Constraint',
        'aliases': ['high-performance', 'low-latency', 'memory-efficient', 'optimized', 'performance'],
        'description': 'Uses profiling/benchmarking tools, applies algorithmic optimizations, uses efficient data structures, or has documented performance characteristics',
        'source': 'constraint-optimization'
    }
    tags.append(performance_optimized)
    print(f"  Added: performance-optimized (merges 3 tags)")

    # Phase 3: Remove overly broad tags
    print("\n=== Phase 3: Removing overly broad tags ===")
    tags = remove_tag_by_id(tags, 'secure')
    print(f"  Removed: secure (too broad)")

    # Phase 4: Add state management constraints
    print("\n=== Phase 4: Adding state management constraints ===")
    stateless = {
        'id': 'stateless',
        'name': 'Stateless',
        'category': 'Constraint',
        'aliases': ['stateless', 'no-state'],
        'description': 'No global variables, no persistent state between function calls (detectable via static analysis)',
        'source': 'constraint-optimization'
    }
    tags.append(stateless)
    print(f"  Added: stateless")

    immutable = {
        'id': 'immutable',
        'name': 'Immutable',
        'category': 'Constraint',
        'aliases': ['immutable', 'immutability'],
        'description': 'No mutation operations, uses immutable data structures (detectable via static analysis)',
        'source': 'constraint-optimization'
    }
    tags.append(immutable)
    print(f"  Added: immutable")

    # Phase 5: Add concurrency model constraints
    print("\n=== Phase 5: Adding concurrency constraints ===")
    lock_free = {
        'id': 'lock-free',
        'name': 'Lock Free',
        'category': 'Constraint',
        'aliases': ['lock-free', 'lockless'],
        'description': 'No mutex, lock, or semaphore primitives (detectable via static analysis)',
        'source': 'constraint-optimization'
    }
    tags.append(lock_free)
    print(f"  Added: lock-free")

    async_tag = {
        'id': 'async',
        'name': 'Async',
        'category': 'Constraint',
        'aliases': ['async', 'asynchronous'],
        'description': 'Uses async/await, Promises, coroutines, or async frameworks (detectable via static analysis)',
        'source': 'constraint-optimization'
    }
    tags.append(async_tag)
    print(f"  Added: async")

    # Phase 6: Add observability constraint
    print("\n=== Phase 6: Adding observability constraint ===")
    observable = {
        'id': 'observable',
        'name': 'Observable',
        'category': 'Constraint',
        'aliases': ['observable', 'instrumented', 'observability'],
        'description': 'Uses logging frameworks, implements metrics/monitoring, has distributed tracing, or uses structured logging (detectable via library imports)',
        'source': 'constraint-optimization'
    }
    tags.append(observable)
    print(f"  Added: observable")

    # Sort tags by id
    tags.sort(key=lambda x: x['id'])

    # Save updated tags
    save_constraints(tags)

    final_count = len(tags)
    print(f"\n=== Summary ===")
    print(f"Original count: {original_count}")
    print(f"Final count: {final_count}")
    print(f"Net change: {final_count - original_count:+d}")
    print(f"\nRemoved (7): readable, maintainable, testable, secure, high-performance, low-latency, memory-efficient")
    print(f"Added (5): performance-optimized, stateless, immutable, lock-free, async, observable")
    print(f"\nUpdated: {CONSTRAINT_FILE}")

if __name__ == '__main__':
    main()
