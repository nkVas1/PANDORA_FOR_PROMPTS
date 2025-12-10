/**
 * PromptEditor - Advanced prompt editor with markdown, variables, AI suggestions
 * 
 * Features:
 * - Markdown support
 * - Template variables
 * - AI optimization suggestions
 * - Live preview
 * - Auto-save
 */

export class PromptEditor {
  constructor(container, options = {}) {
    this.container = typeof container === 'string' 
      ? document.querySelector(container) 
      : container;
    this.options = options;
    this.content = options.content || '';
    this.variables = new Set(options.variables || []);
    this.isDirty = false;
    this.lastSaved = null;

    this.setup();
  }

  /**
   * Setup editor
   */
  setup() {
    this.container.innerHTML = `
      <div class="prompt-editor">
        <div class="editor-toolbar">
          <button class="editor-btn" data-action="bold" title="Bold (Ctrl+B)"><strong>B</strong></button>
          <button class="editor-btn" data-action="italic" title="Italic (Ctrl+I)"><em>I</em></button>
          <button class="editor-btn" data-action="code" title="Code"><code>&lt;&gt;</code></button>
          <div class="editor-toolbar__sep"></div>
          <button class="editor-btn" data-action="variables" title="Insert Variable">$</button>
          <button class="editor-btn" data-action="ai-optimize" title="AI Optimize">✨</button>
          <div class="editor-toolbar__sep"></div>
          <button class="editor-btn" data-action="preview" title="Preview">👁️</button>
        </div>
        <div class="editor-main">
          <textarea class="editor-input" placeholder="Write your prompt here..."></textarea>
          <div class="editor-preview" style="display: none;"></div>
        </div>
        <div class="editor-footer">
          <div class="editor-stats">
            <span class="stat">Words: <strong data-stat="words">0</strong></span>
            <span class="stat">Characters: <strong data-stat="chars">0</strong></span>
          </div>
          <div class="editor-actions">
            <button class="btn btn--secondary" data-action="cancel">Cancel</button>
            <button class="btn btn--primary" data-action="save">Save</button>
          </div>
        </div>
      </div>
    `;

    this.textarea = this.container.querySelector('.editor-input');
    this.preview = this.container.querySelector('.editor-preview');
    this.statsWords = this.container.querySelector('[data-stat="words"]');
    this.statsChars = this.container.querySelector('[data-stat="chars"]');

    this.textarea.value = this.content;
    this.setupEventListeners();
    this.updateStats();
  }

  /**
   * Setup event listeners
   */
  setupEventListeners() {
    // Content changes
    this.textarea.addEventListener('input', () => {
      this.content = this.textarea.value;
      this.isDirty = true;
      this.updateStats();
    });

    // Keyboard shortcuts
    this.textarea.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
        e.preventDefault();
        this.insertMarkdown('**', '**');
      } else if ((e.ctrlKey || e.metaKey) && e.key === 'i') {
        e.preventDefault();
        this.insertMarkdown('_', '_');
      } else if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        this.save();
      }
    });

    // Toolbar buttons
    this.container.querySelectorAll('.editor-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const action = btn.dataset.action;
        switch (action) {
          case 'bold':
            this.insertMarkdown('**', '**');
            break;
          case 'italic':
            this.insertMarkdown('_', '_');
            break;
          case 'code':
            this.insertMarkdown('`', '`');
            break;
          case 'variables':
            this.showVariablesPicker();
            break;
          case 'ai-optimize':
            this.aiOptimize();
            break;
          case 'preview':
            this.togglePreview();
            break;
        }
      });
    });

    // Action buttons
    this.container.querySelector('[data-action="save"]')?.addEventListener('click', () => {
      this.save();
    });

    this.container.querySelector('[data-action="cancel"]')?.addEventListener('click', () => {
      if (this.options.onCancel) {
        this.options.onCancel();
      }
    });
  }

  /**
   * Insert markdown formatting
   */
  insertMarkdown(before, after) {
    const start = this.textarea.selectionStart;
    const end = this.textarea.selectionEnd;
    const selected = this.content.substring(start, end);
    const text = this.content.substring(0, start) + before + selected + after + this.content.substring(end);

    this.textarea.value = text;
    this.content = text;
    this.textarea.selectionStart = start + before.length;
    this.textarea.selectionEnd = start + before.length + selected.length;
    this.textarea.focus();
    this.isDirty = true;
    this.updateStats();
  }

  /**
   * Show variables picker
   */
  showVariablesPicker() {
    const defaultVars = ['user_name', 'date', 'topic', 'tone', 'language'];
    const menu = document.createElement('div');
    menu.className = 'variables-menu';
    menu.innerHTML = defaultVars.map(v => `
      <div class="variable-item" data-var="${v}">${v}</div>
    `).join('');

    menu.addEventListener('click', (e) => {
      const item = e.target.closest('.variable-item');
      if (item) {
        const varName = item.dataset.var;
        this.insertMarkdown('{', `_${varName}}`);
      }
      menu.remove();
    });

    this.container.appendChild(menu);
  }

  /**
   * AI optimize prompt
   */
  async aiOptimize() {
    if (!window.http) return;

    try {
      const response = await window.http.post('/prompts/optimize', {
        content: this.content
      });

      if (response.data.optimized) {
        this.textarea.value = response.data.optimized;
        this.content = response.data.optimized;
        this.isDirty = true;
        this.updateStats();
      }
    } catch (err) {
      console.error('AI optimize failed:', err);
    }
  }

  /**
   * Toggle preview
   */
  togglePreview() {
    const showPreview = this.preview.style.display === 'none';
    this.textarea.style.display = showPreview ? 'none' : 'block';
    this.preview.style.display = showPreview ? 'block' : 'none';

    if (showPreview) {
      // Simple markdown rendering
      let html = this.content
        .replace(/^### (.*?)$/gm, '<h3>$1</h3>')
        .replace(/^## (.*?)$/gm, '<h2>$1</h2>')
        .replace(/^# (.*?)$/gm, '<h1>$1</h1>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/_(.*?)_/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>');

      this.preview.innerHTML = html;
    }
  }

  /**
   * Update stats
   */
  updateStats() {
    const words = this.content.trim().split(/\s+/).filter(w => w.length > 0).length;
    const chars = this.content.length;

    this.statsWords.textContent = words;
    this.statsChars.textContent = chars;
  }

  /**
   * Save
   */
  save() {
    if (this.options.onSave) {
      this.options.onSave({
        content: this.content,
        variables: Array.from(this.variables)
      });
    }
    this.isDirty = false;
    this.lastSaved = new Date();
  }

  /**
   * Get content
   */
  getContent() {
    return this.content;
  }

  /**
   * Set content
   */
  setContent(content) {
    this.content = content;
    this.textarea.value = content;
    this.updateStats();
  }
}
