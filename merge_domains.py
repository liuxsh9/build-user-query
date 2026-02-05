import yaml
import json

# Load existing domain tags
with open('taxonomy/tags/domain.yaml', 'r') as f:
    existing_domains = yaml.safe_load(f)

# Load new domain tags
with open('collected_domain_expansion.json', 'r') as f:
    new_domains = json.load(f)

# Convert new domains to YAML format
for domain in new_domains:
    domain['source'] = 'curated-list'

# Combine and sort by id
all_domains = existing_domains + new_domains
all_domains.sort(key=lambda x: x['id'])

# Save to domain.yaml
with open('taxonomy/tags/domain.yaml', 'w') as f:
    yaml.dump(all_domains, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

print(f"✓ Merged {len(new_domains)} new domains")
print(f"✓ Total domains: {len(all_domains)}")
print(f"✓ Previous: {len(existing_domains)}, New: {len(new_domains)}")
