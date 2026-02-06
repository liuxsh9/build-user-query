import yaml
import json

# Load existing concept tags
with open('taxonomy/tags/concept.yaml', 'r') as f:
    existing_concepts = yaml.safe_load(f)

# Load new concept tags
with open('concept_gap_filling.json', 'r') as f:
    new_concepts = json.load(f)

# Add source field
for concept in new_concepts:
    concept['source'] = 'curated-list'

# Combine and sort by id
all_concepts = existing_concepts + new_concepts
all_concepts.sort(key=lambda x: x['id'])

# Save to concept.yaml
with open('taxonomy/tags/concept.yaml', 'w') as f:
    yaml.dump(all_concepts, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

print(f"✓ Merged {len(new_concepts)} new concepts")
print(f"✓ Total concepts: {len(all_concepts)}")
print(f"✓ Previous: {len(existing_concepts)}, New: {len(new_concepts)}")
print()
print("Added concepts:")
for c in new_concepts:
    print(f"  - {c['name']} ({c['subcategory']}, {c['difficulty']})")
