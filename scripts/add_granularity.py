#!/usr/bin/env python3
"""
Add granularity metadata to existing Library tags.
"""

import yaml
from pathlib import Path

# Granularity classifications based on GRANULARITY_GUIDELINES.md
GRANULARITY_MAP = {
    # Web - Library level (full frameworks)
    'actix': 'library',
    'angular': 'library',
    'aspnet': 'library',
    'axum': 'library',
    'bootstrap': 'library',
    'django': 'library',
    'echo': 'library',
    'express': 'library',
    'fastapi': 'library',
    'flask': 'library',
    'gin': 'library',
    'laravel': 'library',
    'nextjs': 'library',
    'nuxt': 'library',
    'phoenix': 'library',
    'react': 'library',
    'rocket': 'library',
    'ruby-on-rails': 'library',
    'spring-boot': 'library',
    'svelte': 'library',
    'vue': 'library',
    'ant-design': 'library',  # UI component library
    'material-ui': 'library',  # UI component library
    'tailwind-css': 'library',  # CSS framework

    # Data - Library level (full frameworks/libraries)
    'apache-spark': 'library',
    'dask': 'library',
    'hugging-face-transformers': 'library',
    'langchain': 'library',
    'matplotlib': 'library',
    'nltk': 'library',
    'numpy': 'library',
    'opencv': 'library',
    'pandas': 'library',
    'plotly': 'library',
    'polars': 'library',
    'pytorch': 'library',
    'ray': 'library',
    'scikit-learn': 'library',
    'seaborn': 'library',
    'spacy': 'library',
    'tensorflow': 'library',

    # Infrastructure - Library level (tools used as whole)
    'ansible': 'library',
    'apache': 'library',
    'aws-cdk': 'library',
    'circleci': 'library',
    'docker': 'library',
    'github-actions': 'library',
    'gitlab-ci': 'library',
    'grafana': 'library',
    'helm': 'library',
    'jenkins': 'library',
    'kafka': 'library',
    'kubernetes': 'library',
    'nginx': 'library',
    'prometheus': 'library',
    'pulumi': 'library',
    'rabbitmq': 'library',
    'redis': 'library',
    'terraform': 'library',

    # Testing - Library level (testing frameworks)
    'chai': 'library',
    'cypress': 'library',
    'jest': 'library',
    'junit': 'library',
    'mocha': 'library',
    'mock': 'library',
    'mockito': 'library',
    'playwright': 'library',
    'pytest': 'library',
    'rspec': 'library',
    'selenium': 'library',
    'testng': 'library',
    'unittest': 'library',
    'vitest': 'library',

    # Database - Library level (ORMs and drivers)
    'alembic': 'library',
    'diesel': 'library',
    'gorm': 'library',
    'hibernate': 'library',
    'mongoose': 'library',
    'prisma': 'library',
    'psycopg2': 'library',
    'pymongo': 'library',
    'redis-py': 'library',
    'sequelize': 'library',
    'sqlalchemy': 'library',
    'typeorm': 'library',
}

def add_granularity_to_tags():
    """Add granularity field to all Library tags."""
    library_file = Path('taxonomy/tags/library.yaml')

    # Load existing tags
    with open(library_file, 'r') as f:
        tags = yaml.safe_load(f)

    # Add granularity to each tag
    updated_count = 0
    for tag in tags:
        tag_id = tag['id']
        if tag_id in GRANULARITY_MAP:
            tag['granularity'] = GRANULARITY_MAP[tag_id]
            updated_count += 1
        else:
            print(f"Warning: No granularity mapping for tag '{tag_id}'")

    # Write back to file
    with open(library_file, 'w') as f:
        yaml.dump(tags, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"✓ Updated {updated_count} tags with granularity metadata")
    print(f"  Total tags: {len(tags)}")

if __name__ == '__main__':
    add_granularity_to_tags()
