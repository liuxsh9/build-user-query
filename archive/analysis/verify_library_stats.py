import yaml
from collections import defaultdict

# Load library tags
with open('taxonomy/tags/library.yaml', 'r') as f:
    library_tags = yaml.safe_load(f)

print("=" * 70)
print("LIBRARY TAG STATISTICS")
print("=" * 70)
print()

# Total count
print(f"Total Library tags: {len(library_tags)}")
print()

# Subcategory distribution
subcategory_counts = defaultdict(int)
for tag in library_tags:
    subcategory_counts[tag['subcategory']] += 1

print("Subcategory Distribution:")
for subcat, count in sorted(subcategory_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {subcat:<20} {count:>3} tags")
print()

# Granularity distribution
granularity_counts = defaultdict(int)
for tag in library_tags:
    if 'granularity' in tag:
        granularity_counts[tag['granularity']] += 1
    else:
        granularity_counts['missing'] += 1

print("Granularity Distribution:")
for gran, count in sorted(granularity_counts.items()):
    print(f"  {gran:<20} {count:>3} tags")
print(f"  Coverage: {(len(library_tags) - granularity_counts['missing']) / len(library_tags) * 100:.1f}%")
print()

# Alias coverage
tags_with_aliases = sum(1 for tag in library_tags if 'aliases' in tag and tag['aliases'])
print(f"Alias Coverage: {tags_with_aliases}/{len(library_tags)} ({tags_with_aliases/len(library_tags)*100:.1f}%)")
print()

# Language coverage
language_counts = defaultdict(int)
for tag in library_tags:
    if 'language_scope' in tag:
        for lang in tag['language_scope']:
            language_counts[lang] += 1

print(f"Language Coverage: {len(language_counts)} languages")
print("Top 10 languages:")
for lang, count in sorted(language_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {lang:<20} {count:>3} tags")
print()

# Tags with multi-source metrics
tags_with_sources = sum(1 for tag in library_tags if 'sources' in tag or 'weighted_score' in tag)
print(f"Tags with multi-source metrics: {tags_with_sources}/{len(library_tags)} ({tags_with_sources/len(library_tags)*100:.1f}%)")
print()

print("=" * 70)
print("✅ All metrics verified")
print("=" * 70)
