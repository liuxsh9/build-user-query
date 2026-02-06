import yaml
import json

# Load the collected expansion file
with open('collected_domain_expansion.json', 'r') as f:
    new_domains = json.load(f)

# Load current domain.yaml to get the base 32
with open('taxonomy/tags/domain.yaml', 'r') as f:
    current = yaml.safe_load(f)

# Filter out the incorrectly named ones and keep only original 32
original_domains = [d for d in current if not d['id'].endswith('-domain') and d['id'] not in [nd['id'] for nd in new_domains]]

print(f"Original domains: {len(original_domains)}")
print(f"New domains: {len(new_domains)}")

# Add source to new domains
for d in new_domains:
    d['source'] = 'curated-list'

# Combine
all_domains = original_domains + new_domains
all_domains.sort(key=lambda x: x['id'])

print(f"Total: {len(all_domains)}")

# Save
with open('taxonomy/tags/domain.yaml', 'w') as f:
    yaml.dump(all_domains, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

print("✓ Restored domain.yaml with 57 domains")
