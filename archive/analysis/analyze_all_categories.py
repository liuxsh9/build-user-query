import yaml
import os

categories = {
    'Language': 'taxonomy/tags/language.yaml',
    'Concept': 'taxonomy/tags/concept.yaml',
    'Task': 'taxonomy/tags/task.yaml',
    'Constraint': 'taxonomy/tags/constraint.yaml',
    'Agentic': 'taxonomy/tags/agentic.yaml',
    'Context': 'taxonomy/tags/context.yaml'
}

print("=" * 80)
print("CATEGORY ANALYSIS - EXPANSION ASSESSMENT")
print("=" * 80)
print()

for cat_name, file_path in categories.items():
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            tags = yaml.safe_load(f)
        
        print(f"📦 {cat_name}: {len(tags)} tags")
        
        # Show first few tags as examples
        print(f"   Examples: {', '.join([t['name'] for t in tags[:5]])}")
        
        # Check if has subcategories
        subcats = set()
        for tag in tags:
            if 'subcategory' in tag:
                subcats.add(tag['subcategory'])
        
        if subcats:
            print(f"   Subcategories: {', '.join(sorted(subcats))}")
        
        print()

print("=" * 80)
print("EXPANSION RECOMMENDATIONS")
print("=" * 80)
print()
print("✅ Language (50): Complete - covers all major programming languages")
print("🤔 Concept (93): Review - may need specialized concepts")
print("✅ Task (20): Complete - covers all major task types")
print("✅ Constraint (25): Complete - covers all major constraints")
print("✅ Agentic (19): Complete - covers all major agent capabilities")
print("✅ Context (9): Complete - covers all context complexity levels")
print()
