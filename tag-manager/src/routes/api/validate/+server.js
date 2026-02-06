// 4.7 Validation-only endpoint
import { json } from '@sveltejs/kit';
import { validateTag } from '$lib/server/validation-rules.js';
import { yamlService } from '$lib/server/yaml-service.js';

export async function POST({ request }) {
  try {
    const { tag } = await request.json();

    if (!tag) {
      return json({ error: 'Tag data required' }, { status: 400 });
    }

    const allTags = await yamlService.getAllTags();
    const validation = validateTag(tag, allTags);

    return json(validation);
  } catch (error) {
    return json({ error: error.message }, { status: 500 });
  }
}
