import { json } from '@sveltejs/kit';
import { gitService } from '$lib/server/git-service.js';

export async function POST({ request }) {
  const { message } = await request.json();

  if (!message || message.trim().length === 0) {
    return json({ error: 'Commit message is required' }, { status: 400 });
  }

  const result = await gitService.commit(message);

  if (result.success) {
    return json(result);
  } else {
    return json(result, { status: 500 });
  }
}
