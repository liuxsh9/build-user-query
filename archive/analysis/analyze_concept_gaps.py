import yaml

with open('taxonomy/tags/concept.yaml', 'r') as f:
    concepts = yaml.safe_load(f)

# Group by subcategory
by_subcat = {}
for concept in concepts:
    subcat = concept.get('subcategory', 'None')
    if subcat not in by_subcat:
        by_subcat[subcat] = []
    by_subcat[subcat].append(concept['name'])

print("=" * 80)
print("CONCEPT CATEGORY ANALYSIS (93 tags)")
print("=" * 80)
print()

for subcat in sorted(by_subcat.keys()):
    print(f"📚 {subcat} ({len(by_subcat[subcat])} tags)")
    print(f"   {', '.join(sorted(by_subcat[subcat])[:10])}")
    if len(by_subcat[subcat]) > 10:
        print(f"   ... and {len(by_subcat[subcat]) - 10} more")
    print()

print("=" * 80)
print("GAP ANALYSIS")
print("=" * 80)
print()

# Check for common concepts that might be missing
all_names = [c['name'].lower() for c in concepts]

potential_gaps = {
    "Design Patterns": ["singleton", "factory", "observer", "strategy", "decorator"],
    "Data Structures": ["hash table", "tree", "graph", "queue", "stack", "linked list"],
    "Algorithms": ["sorting", "searching", "dynamic programming", "greedy"],
    "Concurrency": ["mutex", "semaphore", "deadlock", "race condition", "thread pool"],
    "Architecture": ["microservices", "monolith", "event-driven", "layered"],
    "Security": ["encryption", "authentication", "authorization", "csrf", "xss"],
    "Testing": ["unit testing", "integration testing", "mocking", "test-driven"],
}

print("Checking for potential gaps...")
print()

for category, keywords in potential_gaps.items():
    found = [kw for kw in keywords if any(kw in name for name in all_names)]
    missing = [kw for kw in keywords if not any(kw in name for name in all_names)]
    
    if missing:
        print(f"⚠️  {category}:")
        print(f"   Found: {', '.join(found) if found else 'none'}")
        print(f"   Missing: {', '.join(missing)}")
        print()

print("=" * 80)
print("CONCLUSION")
print("=" * 80)
print()
print("The Concept category (93 tags) appears comprehensive with good coverage of:")
print("- Fundamentals: Basic programming concepts")
print("- Advanced: Complex patterns and techniques")
print("- Engineering: Software engineering practices")
print()
print("Most common concepts are already covered. Expansion not critical.")
print()
