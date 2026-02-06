// 3.1 Validation rules constants
export const VALIDATION_RULES = {
  // Categories
  CATEGORIES: [
    'Concept', 'Library', 'Language', 'Domain',
    'Constraint', 'Task', 'Agentic', 'Context'
  ],

  // Subcategories by category
  SUBCATEGORIES: {
    Concept: ['Fundamentals', 'Advanced', 'Engineering'],
    Library: ['Web', 'Database', 'Data', 'Testing', 'Other']
  },

  // Difficulty levels
  DIFFICULTIES: ['basic', 'intermediate', 'advanced'],

  // Source types
  SOURCES: [
    'curated-list',
    'educational-sources',
    'TIOBE',
    'GitHub',
    'manual'
  ],

  // Required fields (all categories)
  REQUIRED_FIELDS: ['id', 'name', 'category', 'source'],

  // Category-specific required fields
  CATEGORY_REQUIRED: {
    Concept: ['subcategory', 'difficulty'],
    Library: ['subcategory', 'language_scope', 'granularity'],
    Language: ['aliases'],
    Domain: ['description', 'aliases']
  },

  // Field patterns
  FIELD_PATTERNS: {
    id: /^[a-z0-9-]+$/,
    url: /^https?:\/\/.+/
  }
};

// 3.2 Main validation function with all rules
export function validateTag(tag, allTags = []) {
  const errors = [];

  // 3.3 Required field validation
  for (const field of VALIDATION_RULES.REQUIRED_FIELDS) {
    if (!tag[field]) {
      errors.push(`Missing required field: ${field}`);
    }
  }

  // 3.4 Field format validation - ID pattern
  if (tag.id && !VALIDATION_RULES.FIELD_PATTERNS.id.test(tag.id)) {
    errors.push('ID must contain only lowercase letters, numbers, and hyphens');
  }

  // 3.5 ID uniqueness validation
  const duplicateId = allTags.find(t =>
    t.id === tag.id &&
    t !== tag &&
    (t.category !== tag.category || t !== tag)
  );
  if (duplicateId) {
    errors.push(`Duplicate ID: ${tag.id} already exists in ${duplicateId.category}`);
  }

  // Category validity
  if (tag.category && !VALIDATION_RULES.CATEGORIES.includes(tag.category)) {
    errors.push(`Invalid category: ${tag.category}`);
  }

  // 3.6 Category-specific required fields
  if (tag.category) {
    const required = VALIDATION_RULES.CATEGORY_REQUIRED[tag.category] || [];
    for (const field of required) {
      if (!tag[field] || (Array.isArray(tag[field]) && tag[field].length === 0)) {
        errors.push(`${tag.category} requires field: ${field}`);
      }
    }
  }

  // 3.7 Subcategory consistency validation
  if (tag.subcategory && tag.category) {
    const validSubs = VALIDATION_RULES.SUBCATEGORIES[tag.category];
    if (validSubs && !validSubs.includes(tag.subcategory)) {
      errors.push(`Invalid subcategory for ${tag.category}: ${tag.subcategory}`);
    }
  }

  // Difficulty validation
  if (tag.difficulty && !VALIDATION_RULES.DIFFICULTIES.includes(tag.difficulty)) {
    errors.push(`Invalid difficulty: ${tag.difficulty}`);
  }

  // Source validation
  if (tag.source && !VALIDATION_RULES.SOURCES.includes(tag.source)) {
    errors.push(`Invalid source: ${tag.source}`);
  }

  // 3.8 Language scope validation
  if (tag.language_scope && Array.isArray(tag.language_scope)) {
    const validLanguages = allTags
      .filter(t => t.category === 'Language')
      .map(t => t.id);

    for (const lang of tag.language_scope) {
      if (validLanguages.length > 0 && !validLanguages.includes(lang)) {
        errors.push(`Invalid language_scope: ${lang} is not a valid Language tag`);
      }
    }
  }

  // Weighted score range
  if (tag.weighted_score !== undefined) {
    const score = Number(tag.weighted_score);
    if (isNaN(score) || score < 0 || score > 1) {
      errors.push('weighted_score must be a number between 0 and 1');
    }
  }

  // 3.9 Aliases uniqueness validation
  if (tag.aliases && Array.isArray(tag.aliases)) {
    const unique = new Set(tag.aliases);
    if (unique.size !== tag.aliases.length) {
      errors.push('Aliases must be unique');
    }
  }

  // 3.10 Relationship field validation (prerequisites, related)
  if (tag.prerequisites && Array.isArray(tag.prerequisites)) {
    if (tag.prerequisites.includes(tag.id)) {
      errors.push('Tag cannot be a prerequisite of itself');
    }

    const validIds = allTags.map(t => t.id);
    for (const prereq of tag.prerequisites) {
      if (validIds.length > 0 && !validIds.includes(prereq)) {
        errors.push(`Invalid prerequisite: ${prereq} does not exist`);
      }
    }
  }

  if (tag.related && Array.isArray(tag.related)) {
    if (tag.related.includes(tag.id)) {
      errors.push('Tag cannot be related to itself');
    }

    const validIds = allTags.map(t => t.id);
    for (const rel of tag.related) {
      if (validIds.length > 0 && !validIds.includes(rel)) {
        errors.push(`Invalid related tag: ${rel} does not exist`);
      }
    }
  }

  // 3.12 Return structured error messages
  return {
    valid: errors.length === 0,
    errors
  };
}
