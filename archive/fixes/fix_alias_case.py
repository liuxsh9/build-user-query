import yaml

# Load library tags
with open('taxonomy/tags/library.yaml', 'r') as f:
    library_tags = yaml.safe_load(f)

# Fix alias case issues
changes = []
for tag in library_tags:
    if 'aliases' in tag:
        original = tag['aliases'].copy()
        updated = []
        for alias in tag['aliases']:
            if alias != alias.lower():
                updated.append(alias.lower())
                changes.append(f"{tag['id']}: {alias} -> {alias.lower()}")
            else:
                updated.append(alias)
        tag['aliases'] = updated

# Save updated tags
with open('taxonomy/tags/library.yaml', 'w') as f:
    yaml.dump(library_tags, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

print(f"Fixed {len(changes)} alias case issues:")
for change in changes:
    print(f"  - {change}")
