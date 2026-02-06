// 4.3 PUT and DELETE for specific tag
import { json } from '@sveltejs/kit';
import { yamlService } from '$lib/server/yaml-service.js';

export async function PUT({ params, request }) {
  try {
    const { category, id } = params;
    const updates = await request.json();

    // 4.5 Integrate validation
    const { validateTag } = await import('$lib/server/validation-rules.js');
    const allTags = await yamlService.getAllTags();

    // Get current tag and merge with updates
    const currentTags = await yamlService.readCategory(category);
    const currentTag = currentTags.find(t => t.id === id);
    if (!currentTag) {
      return json({ error: 'Tag not found' }, { status: 404 });
    }

    const updatedTag = { ...currentTag, ...updates };
    const validation = validateTag(updatedTag, allTags);

    if (!validation.valid) {
      return json({
        error: 'Validation failed',
        errors: validation.errors
      }, { status: 400 });
    }

    const result = await yamlService.updateTag(category, id, updates);
    return json({ tag: result });
  } catch (error) {
    // 4.6 Error handling with proper status codes
    if (error.message.includes('not found')) {
      return json({ error: error.message }, { status: 404 });
    }
    return json({ error: error.message }, { status: 400 });
  }
}

export async function DELETE({ params }) {
  try {
    const { category, id } = params;
    await yamlService.deleteTag(category, id);
    return json({ success: true });
  } catch (error) {
    if (error.message.includes('not found')) {
      return json({ error: error.message }, { status: 404 });
    }
    return json({ error: error.message }, { status: 500 });
  }
}
