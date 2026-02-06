import yaml from 'js-yaml';
import fs from 'fs/promises';
import path from 'path';

const TAGS_DIR = path.resolve('../taxonomy/tags');

export class YamlService {

  // 2.2 Read all YAML files
  async getAllTags() {
    const files = await fs.readdir(TAGS_DIR);
    const yamlFiles = files.filter(f => f.endsWith('.yaml'));

    const allTags = [];
    for (const file of yamlFiles) {
      const category = path.basename(file, '.yaml');
      const tags = await this.readCategory(category);
      allTags.push(...tags);
    }

    return allTags;
  }

  // 2.3 Read single category file
  async readCategory(category) {
    const filePath = path.join(TAGS_DIR, `${category}.yaml`);

    try {
      const content = await fs.readFile(filePath, 'utf8');
      const tags = yaml.load(content) || [];

      // Add category field if not present
      return tags.map(tag => ({
        ...tag,
        category: tag.category || this.categoryNameFromFile(category)
      }));
    } catch (error) {
      // 2.8 Error handling
      if (error.code === 'ENOENT') {
        return [];
      }
      throw error;
    }
  }

  // 2.4 Write category with proper formatting
  async writeCategory(category, tags) {
    const filePath = path.join(TAGS_DIR, `${category}.yaml`);

    // Format YAML with consistent options
    const content = yaml.dump(tags, {
      indent: 2,
      lineWidth: -1,  // No line wrapping
      noRefs: true,   // No anchors/aliases
      sortKeys: false // Preserve order
    });

    await fs.writeFile(filePath, content, 'utf8');
  }

  // 2.5 Create tag with ID sorting
  async createTag(category, tagData) {
    const tags = await this.readCategory(category);

    // Check for duplicate ID
    if (tags.find(t => t.id === tagData.id)) {
      throw new Error(`Tag with ID ${tagData.id} already exists in ${category}`);
    }

    // Add new tag
    tags.push(tagData);

    // Sort by ID
    tags.sort((a, b) => a.id.localeCompare(b.id));

    await this.writeCategory(category, tags);

    return tagData;
  }

  // 2.6 Update tag with merge logic
  async updateTag(category, id, updates) {
    const tags = await this.readCategory(category);

    const index = tags.findIndex(t => t.id === id);
    if (index === -1) {
      throw new Error(`Tag ${id} not found in ${category}`);
    }

    // Merge updates
    const updatedTag = { ...tags[index], ...updates };
    tags[index] = updatedTag;

    await this.writeCategory(category, tags);

    return updatedTag;
  }

  // 2.7 Delete tag with filtering
  async deleteTag(category, id) {
    const tags = await this.readCategory(category);
    const filtered = tags.filter(t => t.id !== id);

    if (filtered.length === tags.length) {
      throw new Error(`Tag ${id} not found in ${category}`);
    }

    await this.writeCategory(category, filtered);

    return { success: true };
  }

  // 2.9 Helper for filename to category mapping
  categoryNameFromFile(filename) {
    const map = {
      'concept': 'Concept',
      'library': 'Library',
      'language': 'Language',
      'domain': 'Domain',
      'constraint': 'Constraint',
      'task': 'Task',
      'agentic': 'Agentic',
      'context': 'Context'
    };
    return map[filename] || filename;
  }
}

export const yamlService = new YamlService();
