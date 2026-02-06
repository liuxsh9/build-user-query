// 3.11 Client-side validator with same rules
// Shares logic with server-side validation for consistency

const VALIDATION_RULES = {
  CATEGORIES: [
    'Concept', 'Library', 'Language', 'Domain',
    'Constraint', 'Task', 'Agentic', 'Context'
  ],
  SUBCATEGORIES: {
    Concept: ['Fundamentals', 'Advanced', 'Engineering'],
    Library: ['Web', 'Database', 'Data', 'Testing', 'Other']
  },
  DIFFICULTIES: ['basic', 'intermediate', 'advanced'],
  SOURCES: [
    'curated-list',
    'educational-sources',
    'TIOBE',
    'GitHub',
    'manual'
  ],
  REQUIRED_FIELDS: ['id', 'name', 'category', 'source'],
  CATEGORY_REQUIRED: {
    Concept: ['subcategory', 'difficulty'],
    Library: ['subcategory', 'language_scope', 'granularity'],
    Language: ['aliases'],
    Domain: ['description', 'aliases']
  },
  FIELD_PATTERNS: {
    id: /^[a-z0-9-]+$/,
    url: /^https?:\/\/.+/
  }
};

export function validateTag(tag, allTags = []) {
  const errors = [];

  // Required fields
  for (const field of VALIDATION_RULES.REQUIRED_FIELDS) {
    if (!tag[field]) {
      errors.push(`Missing required field: ${field}`);
    }
  }

  // ID format
  if (tag.id && !VALIDATION_RULES.FIELD_PATTERNS.id.test(tag.id)) {
    errors.push('ID must contain only lowercase letters, numbers, and hyphens');
  }

  // ID uniqueness
  const duplicateId = allTags.find(t =>
    t.id === tag.id &&
    t !== tag &&
    (t.category !== tag.category || t !== tag)
  );
  if (duplicateId) {
    errors.push(`Duplicate ID: ${tag.id} already exists`);
  }

  // Category validity
  if (tag.category && !VALIDATION_RULES.CATEGORIES.includes(tag.category)) {
    errors.push(`Invalid category: ${tag.category}`);
  }

  // Category-specific required fields
  if (tag.category) {
    const required = VALIDATION_RULES.CATEGORY_REQUIRED[tag.category] || [];
    for (const field of required) {
      if (!tag[field] || (Array.isArray(tag[field]) && tag[field].length === 0)) {
        errors.push(`${tag.category} requires field: ${field}`);
      }
    }
  }

  // Subcategory consistency
  if (tag.subcategory && tag.category) {
    const validSubs = VALIDATION_RULES.SUBCATEGORIES[tag.category];
    if (validSubs && !validSubs.includes(tag.subcategory)) {
      errors.push(`Invalid subcategory for ${tag.category}: ${tag.subcategory}`);
    }
  }

  // Difficulty
  if (tag.difficulty && !VALIDATION_RULES.DIFFICULTIES.includes(tag.difficulty)) {
    errors.push(`Invalid difficulty: ${tag.difficulty}`);
  }

  // Source
  if (tag.source && !VALIDATION_RULES.SOURCES.includes(tag.source)) {
    errors.push(`Invalid source: ${tag.source}`);
  }

  // Language scope
  if (tag.language_scope && Array.isArray(tag.language_scope)) {
    const validLanguages = allTags
      .filter(t => t.category === 'Language')
      .map(t => t.id);

    for (const lang of tag.language_scope) {
      if (validLanguages.length > 0 && !validLanguages.includes(lang)) {
        errors.push(`Invalid language_scope: ${lang}`);
      }
    }
  }

  // Aliases uniqueness
  if (tag.aliases && Array.isArray(tag.aliases)) {
    const unique = new Set(tag.aliases);
    if (unique.size !== tag.aliases.length) {
      errors.push('Aliases must be unique');
    }
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

export { VALIDATION_RULES };
