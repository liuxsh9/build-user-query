# Before expansion (from analysis)
before = {
    'javascript': 105,
    'python': 100,
    'typescript': 82,
    'go': 39,
    'java': 15,
    'csharp': 4,
    'ruby': 6,
    'php': 1,
    'rust': 6,
    'kotlin': 0,
    'swift': 0,
    'scala': 4,
    'elixir': 1,
    'c++': 3
}

# After expansion (current)
after = {
    'javascript': 104,
    'python': 100,
    'typescript': 81,
    'go': 39,
    'java': 25,
    'csharp': 12,
    'ruby': 9,
    'php': 9,
    'rust': 8,
    'kotlin': 6,
    'swift': 3,
    'scala': 6,
    'elixir': 2,
    'c++': 6
}

print("Language Coverage Improvement")
print("=" * 70)
print(f"{'Language':<15} {'Before':<10} {'After':<10} {'Change':<10} {'Status':<15}")
print("-" * 70)

for lang in sorted(set(list(before.keys()) + list(after.keys()))):
    before_count = before.get(lang, 0)
    after_count = after.get(lang, 0)
    change = after_count - before_count
    
    if change > 0:
        status = f"+{change} ✓"
    elif change < 0:
        status = f"{change}"
    else:
        status = "—"
    
    print(f"{lang:<15} {before_count:<10} {after_count:<10} {change:>+4}      {status:<15}")

print("-" * 70)
total_before = sum(before.values())
total_after = sum(after.values())
print(f"{'TOTAL':<15} {total_before:<10} {total_after:<10} {total_after - total_before:>+4}")
print()
print("Key improvements:")
print("  • Java: 15 → 25 (+10 tags, +67%)")
print("  • C#: 4 → 12 (+8 tags, +200%)")
print("  • PHP: 1 → 9 (+8 tags, +800%)")
print("  • Kotlin: 0 → 6 (+6 tags, new coverage)")
print("  • Swift: 0 → 3 (+3 tags, new coverage)")
print("  • Ruby: 6 → 9 (+3 tags, +50%)")
print("  • Rust: 6 → 8 (+2 tags, +33%)")
print("  • C++: 3 → 6 (+3 tags, +100%)")
print("  • Scala: 4 → 6 (+2 tags, +50%)")
print("  • Elixir: 1 → 2 (+1 tag, +100%)")
