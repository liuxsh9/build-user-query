import yaml
from collections import defaultdict

# Load library tags
with open('taxonomy/tags/library.yaml', 'r') as f:
    library_tags = yaml.safe_load(f)

# Count by language
language_counts = defaultdict(int)
for tag in library_tags:
    if 'language_scope' in tag:
        for lang in tag['language_scope']:
            language_counts[lang] += 1

# Sort by count
sorted_langs = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)

print("Language Coverage Analysis (342 Library tags)")
print("=" * 60)
print(f"{'Language':<20} {'Count':<10} {'Percentage':<10}")
print("-" * 60)

for lang, count in sorted_langs:
    percentage = (count / 342) * 100
    print(f"{lang:<20} {count:<10} {percentage:>6.1f}%")

print("-" * 60)
print(f"{'Total unique languages':<20} {len(language_counts):<10}")
print(f"{'Tags with language_scope':<20} {sum(1 for t in library_tags if 'language_scope' in t):<10}")
