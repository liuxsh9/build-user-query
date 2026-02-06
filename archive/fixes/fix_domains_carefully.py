import yaml
import json

# The original 32 domains (from before expansion)
original_32 = [
    'api-development', 'automation', 'blockchain', 'cli-tool', 'cloud-computing',
    'compiler-development', 'computer-vision', 'cybersecurity', 'data-science',
    'database-administration', 'deep-learning', 'desktop-application', 'devops',
    'e-commerce', 'embedded-systems', 'etl', 'financial-technology', 'full-stack',
    'game-development', 'healthcare-technology', 'iot', 'machine-learning',
    'mobile-development', 'natural-language-processing', 'network-programming',
    'operating-systems', 'robotics', 'scientific-computing', 'smart-contracts',
    'systems-programming', 'web-backend', 'web-frontend'
]

# Load current to get original tags
with open('taxonomy/tags/domain.yaml', 'r') as f:
    current = yaml.safe_load(f)

# Get original 32
original_tags = [d for d in current if d['id'] in original_32]
print(f"Found {len(original_tags)} original tags")

# Load new 25
with open('collected_domain_expansion.json', 'r') as f:
    new_tags = json.load(f)

for tag in new_tags:
    tag['source'] = 'curated-list'

print(f"New tags: {len(new_tags)}")

# Combine
all_tags = original_tags + new_tags
all_tags.sort(key=lambda x: x['id'])

print(f"Total: {len(all_tags)}")

# Save
with open('taxonomy/tags/domain.yaml', 'w') as f:
    yaml.dump(all_tags, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

print("✓ Fixed domain.yaml")
