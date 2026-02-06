import { json } from '@sveltejs/kit';
import { gitService } from '$lib/server/git-service.js';

export async function GET() {
  const status = await gitService.getStatus();
  return json(status);
}
