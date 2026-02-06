import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export class GitService {

  async getStatus() {
    try {
      const { stdout } = await execAsync('git status --porcelain ../taxonomy/tags/');

      const changes = stdout
        .split('\n')
        .filter(line => line.trim())
        .map(line => {
          const status = line.substring(0, 2);
          const file = line.substring(3);
          return {
            status: this.parseStatus(status),
            file: file.replace('../taxonomy/tags/', '')
          };
        });

      return {
        hasChanges: changes.length > 0,
        changes
      };
    } catch (error) {
      return {
        hasChanges: false,
        changes: [],
        error: error.message
      };
    }
  }

  async commit(message) {
    try {
      await execAsync('git add ../taxonomy/tags/');
      await execAsync(`git commit -m "${this.escapeMessage(message)}"`);

      const status = await this.getStatus();

      return {
        success: true,
        status
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async getRecentCommits(limit = 10) {
    try {
      const { stdout } = await execAsync(
        `git log --oneline -n ${limit} -- ../taxonomy/tags/`
      );

      return stdout.split('\n').filter(line => line.trim());
    } catch (error) {
      return [];
    }
  }

  parseStatus(code) {
    const map = {
      'M ': 'modified',
      ' M': 'modified',
      'A ': 'added',
      'D ': 'deleted',
      '??': 'untracked'
    };
    return map[code] || 'unknown';
  }

  escapeMessage(message) {
    return message.replace(/"/g, '\\"');
  }
}

export const gitService = new GitService();
