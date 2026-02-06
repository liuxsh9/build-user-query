// 4.2 GET by category
import { json } from '@sveltejs/kit';
import { yamlService } from '$lib/server/yaml-service.js';

export async function GET({ params }) {
  try {
    const { category } = params;
    const tags = await yamlService.readCategory(category);
    return json({ tags });
  } catch (error) {
    return json({ error: error.message }, { status: 500 });
  }
}
