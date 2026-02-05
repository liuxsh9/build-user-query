import yaml

# Load domain tags
with open('taxonomy/tags/domain.yaml', 'r') as f:
    domain_tags = yaml.safe_load(f)

print("=" * 70)
print("CURRENT DOMAIN TAG ANALYSIS")
print("=" * 70)
print()

print(f"Total Domain tags: {len(domain_tags)}")
print()

print("Current Domain tags:")
for i, tag in enumerate(domain_tags, 1):
    name = tag.get('name', 'N/A')
    tag_id = tag.get('id', 'N/A')
    desc = tag.get('description', 'N/A')
    print(f"{i:2}. {name:<30} (id: {tag_id})")
    if desc != 'N/A':
        print(f"    {desc[:70]}...")

print()
print("=" * 70)
