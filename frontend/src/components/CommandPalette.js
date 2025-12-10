/**
 * CommandPalette - Fuzzy search command palette (Cmd+K shortcut)
 * 
 * Features:
 * - Fuzzy search
 * - Command categories
 * - Keyboard navigation
 * - Recent commands
 */

export class CommandPalette {
  constructor(options = {}) {
    this.commands = [];
    this.container = document.createElement('div');
    this.container.className = 'command-palette';
    this.isOpen = false;
    this.selectedIndex = 0;
    this.recentCommands = JSON.parse(localStorage.getItem('recentCommands') || '[]');

    this.setupHTML();
    this.setupKeyBindings();
  }

  /**
   * Setup HTML structure
   */
  setupHTML() {
    this.container.innerHTML = `
      <div class="command-palette__overlay"></div>
      <div class="command-palette__content">
        <div class="command-palette__header">
          <input 
            type="text" 
            class="command-palette__input" 
            placeholder="Search commands (Cmd+K)..."
          />
        </div>
        <div class="command-palette__list"></div>
      </div>
    `;

    this.input = this.container.querySelector('.command-palette__input');
    this.list = this.container.querySelector('.command-palette__list');
    this.overlay = this.container.querySelector('.command-palette__overlay');

    // Event listeners
    this.input.addEventListener('input', () => this.search());
    this.overlay.addEventListener('click', () => this.close());
  }

  /**
   * Register command
   */
  registerCommand(cmd) {
    this.commands.push({
      id: cmd.id,
      label: cmd.label,
      description: cmd.description || '',
      category: cmd.category || 'General',
      action: cmd.action,
      shortcut: cmd.shortcut || null
    });
  }

  /**
   * Search commands
   */
  search() {
    const query = this.input.value.toLowerCase();
    let filtered = this.commands;

    if (query) {
      filtered = this.commands.filter(cmd => {
        const score = this.fuzzyScore(
          query,
          (cmd.label + ' ' + cmd.description).toLowerCase()
        );
        return score > 0;
      });

      filtered.sort((a, b) => {
        const scoreA = this.fuzzyScore(query, a.label.toLowerCase());
        const scoreB = this.fuzzyScore(query, b.label.toLowerCase());
        return scoreB - scoreA;
      });
    } else {
      // Show recent commands when empty
      const recentIds = this.recentCommands;
      filtered = this.commands.filter(cmd => recentIds.includes(cmd.id));
    }

    this.renderResults(filtered);
  }

  /**
   * Fuzzy score matching
   */
  fuzzyScore(query, str) {
    let score = 0;
    let queryIdx = 0;
    let strIdx = 0;

    while (queryIdx < query.length && strIdx < str.length) {
      if (query[queryIdx] === str[strIdx]) {
        score += 1;
        queryIdx++;
      }
      strIdx++;
    }

    return queryIdx === query.length ? score : 0;
  }

  /**
   * Render search results
   */
  renderResults(commands) {
    this.list.innerHTML = '';
    this.selectedIndex = 0;

    commands.forEach((cmd, idx) => {
      const item = document.createElement('div');
      item.className = 'command-palette__item';
      if (idx === this.selectedIndex) {
        item.classList.add('selected');
      }

      item.innerHTML = `
        <div class="command-palette__item-label">${cmd.label}</div>
        ${cmd.description ? `<div class="command-palette__item-desc">${cmd.description}</div>` : ''}
        ${cmd.shortcut ? `<div class="command-palette__item-shortcut">${cmd.shortcut}</div>` : ''}
      `;

      item.addEventListener('click', () => this.executeCommand(cmd));
      this.list.appendChild(item);
    });
  }

  /**
   * Execute command
   */
  executeCommand(cmd) {
    // Add to recent commands
    this.recentCommands = [
      cmd.id,
      ...this.recentCommands.filter(id => id !== cmd.id)
    ].slice(0, 10);
    localStorage.setItem('recentCommands', JSON.stringify(this.recentCommands));

    // Execute action
    if (cmd.action) {
      cmd.action();
    }

    this.close();
  }

  /**
   * Setup keyboard shortcuts
   */
  setupKeyBindings() {
    document.addEventListener('keydown', (e) => {
      // Cmd+K to open palette
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        this.toggle();
      }

      if (!this.isOpen) return;

      // Navigation
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        this.selectedIndex = Math.min(
          this.selectedIndex + 1,
          this.list.children.length - 1
        );
        this.updateSelection();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        this.selectedIndex = Math.max(this.selectedIndex - 1, 0);
        this.updateSelection();
      } else if (e.key === 'Enter') {
        e.preventDefault();
        const selected = this.list.children[this.selectedIndex];
        if (selected) {
          selected.click();
        }
      } else if (e.key === 'Escape') {
        e.preventDefault();
        this.close();
      }
    });
  }

  /**
   * Update selected item visual
   */
  updateSelection() {
    this.list.querySelectorAll('.command-palette__item').forEach((item, idx) => {
      item.classList.toggle('selected', idx === this.selectedIndex);
    });
  }

  /**
   * Open palette
   */
  open() {
    if (this.isOpen) return;
    this.isOpen = true;
    document.body.appendChild(this.container);
    this.container.classList.add('open');
    this.input.focus();
    this.search();
  }

  /**
   * Close palette
   */
  close() {
    this.isOpen = false;
    this.container.classList.remove('open');
    setTimeout(() => this.container.remove(), 200);
  }

  /**
   * Toggle palette
   */
  toggle() {
    if (this.isOpen) {
      this.close();
    } else {
      this.open();
    }
  }
}
