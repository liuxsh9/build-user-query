import yaml

# Load domain tags
with open('taxonomy/tags/domain.yaml', 'r') as f:
    domains = yaml.safe_load(f)

# Load concept tags to check conflicts
with open('taxonomy/tags/concept.yaml', 'r') as f:
    concepts = yaml.safe_load(f)

# Get all concept aliases
concept_aliases = set()
for concept in concepts:
    if 'aliases' in concept:
        concept_aliases.update(concept['aliases'])

# Fix conflicting aliases in domains
fixes = []
for domain in domains:
    if 'aliases' in domain:
        original_aliases = domain['aliases'].copy()
        # Remove aliases that conflict with concepts
        domain['aliases'] = [a for a in domain['aliases'] if a not in concept_aliases or a == domain['id']]
        if len(domain['aliases']) != len(original_aliases):
            removed = set(original_aliases) - set(domain['aliases'])
            fixes.append(f"{domain['id']}: removed conflicting aliases {removed}")

# Save updated domains
with open('taxonomy/tags/domain.yaml', 'w') as f:
    yaml.dump(domains, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

if fixes:
    print(f"Fixed {len(fixes)} alias conflicts:")
    for fix in fixes:
        print(f"  - {fix}")
else:
    print("No alias conflicts to fix")
