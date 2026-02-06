// 4.1 GET all tags
import { json } from '@sveltejs/kit';
import { yamlService } from '$lib/server/yaml-service.js';

export async function GET() {
  try {
    const tags = await yamlService.getAllTags();
    return json({ tags });
  } catch (error) {
    // 4.6 Error handling with proper status codes
    return json({ error: error.message }, { status: 500 });
  }
}

// 4.4 POST endpoint for creating new tags
export async function POST({ request }) {
  try {
    const { category, tag } = await request.json();

    if (!category || !tag) {
      return json({ error: 'Category and tag data required' }, { status: 400 });
    }

    // 4.5 Integrate validation
    const { validateTag } = await import('$lib/server/validation-rules.js');
    const allTags = await yamlService.getAllTags();
    const validation = validateTag(tag, allTags);

    if (!validation.valid) {
      return json({
        error: 'Validation failed',
        errors: validation.errors
      }, { status: 400 });
    }

    const createdTag = await yamlService.createTag(category, tag);
    return json({ tag: createdTag }, { status: 201 });
  } catch (error) {
    return json({ error: error.message }, { status: 400 });
  }
}
