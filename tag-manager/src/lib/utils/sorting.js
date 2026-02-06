// 6.6-6.7 Sorting utilities
export function sortTags(tags, sortBy) {
  const sorted = [...tags];

  switch (sortBy) {
    case 'name':
      sorted.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
      break;

    case 'id':
      sorted.sort((a, b) => (a.id || '').localeCompare(b.id || ''));
      break;

    case 'difficulty':
      const diffOrder = { basic: 1, intermediate: 2, advanced: 3 };
      sorted.sort((a, b) => {
        const aOrder = diffOrder[a.difficulty] || 0;
        const bOrder = diffOrder[b.difficulty] || 0;
        return aOrder - bOrder;
      });
      break;

    default:
      // Default to name sorting
      sorted.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
  }

  return sorted;
}
