import yaml

# Load library tags
with open('taxonomy/tags/library.yaml', 'r') as f:
    library_tags = yaml.safe_load(f)

# Fix language_scope issues
changes = []
for tag in library_tags:
    if 'language_scope' in tag:
        original = tag['language_scope'].copy()
        updated = []
        for lang in tag['language_scope']:
            if lang == 'c++':
                updated.append('cpp')
                changes.append(f"{tag['id']}: c++ -> cpp")
            elif lang in ['yaml', 'json', 'hcl']:
                # Remove these as they're not in Language category
                changes.append(f"{tag['id']}: removed {lang} (not in Language category)")
            else:
                updated.append(lang)
        tag['language_scope'] = updated

# Save updated tags
with open('taxonomy/tags/library.yaml', 'w') as f:
    yaml.dump(library_tags, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

print(f"Fixed {len(changes)} language_scope issues:")
for change in changes:
    print(f"  - {change}")
