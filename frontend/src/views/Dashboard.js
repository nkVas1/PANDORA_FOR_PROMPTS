// Полная реализация Dashboard view
export default function createDashboard() {
  const container = document.createElement('div');
  container.className = 'dashboard-view';
  container.innerHTML = `
    <div class="dashboard-container">
      <div class="dashboard-header">
        <div>
          <h1>Добро пожаловать в PANDORA</h1>
          <p>Ваш профессиональный менеджер промптов</p>
        </div>
        <button class="btn btn--primary btn--lg" data-action="new-prompt">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          Новый промпт
        </button>
      </div>

      <div class="dashboard-stats">
        <div class="stat-card">
          <div class="stat-card__icon">📝</div>
          <div class="stat-card__content">
            <p class="stat-card__title">Всего промптов</p>
            <p class="stat-card__value" data-stat="prompts">0</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-card__icon">📁</div>
          <div class="stat-card__content">
            <p class="stat-card__title">Проектов</p>
            <p class="stat-card__value" data-stat="projects">0</p>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-card__icon">🏷️</div>
          <div class="stat-card__content">
            <p class="stat-card__title">Тегов</p>
            <p class="stat-card__value" data-stat="tags">0</p>
          </div>
        </div>
      </div>

      <div class="dashboard-content">
        <div class="dashboard-left">
          <div class="dashboard-section">
            <div class="section-header">
              <h2>📝 Недавние промпты</h2>
              <a href="#/prompts" class="link">Показать всё →</a>
            </div>
            <div class="prompts-list"></div>
          </div>
        </div>

        <div class="dashboard-right">
          <div class="dashboard-section">
            <h2>⚡ Быстрые действия</h2>
            <div class="quick-actions">
              <button class="quick-action" data-action="new-prompt">
                <span class="icon">✨</span>
                <span>Новый промпт</span>
              </button>
              <button class="quick-action" data-action="new-project">
                <span class="icon">📁</span>
                <span>Новый проект</span>
              </button>
            </div>
          </div>

          <div class="dashboard-section">
            <h2>📈 Рост (7 дней)</h2>
            <div class="growth-stats"></div>
          </div>
        </div>
      </div>
    </div>
  `;

  // Load data
  if (window.http) {
    window.http.get('/analytics/dashboard').then(resp => {
      const data = resp.data || resp;
      
      // Update stats
      if (data.totals) {
        container.querySelector('[data-stat="prompts"]').textContent = data.totals.prompts || 0;
        container.querySelector('[data-stat="projects"]').textContent = data.totals.projects || 0;
        container.querySelector('[data-stat="tags"]').textContent = data.totals.tags || 0;
      }

      // Update recent prompts
      if (data.popular_prompts && data.popular_prompts.length > 0) {
        const promptsList = container.querySelector('.prompts-list');
        promptsList.innerHTML = data.popular_prompts.slice(0, 5).map(p => `
          <div class="prompt-item" data-id="${p.id}">
            <div class="prompt-item__header">
              <h3 class="prompt-item__title">${p.title}</h3>
              <span class="badge">${p.category}</span>
            </div>
            <p class="prompt-item__usage">Использовано: ${p.usage_count} раз</p>
          </div>
        `).join('');

        promptsList.querySelectorAll('.prompt-item').forEach(item => {
          item.addEventListener('click', () => {
            if (window.router) window.router.navigate(`/editor/${item.dataset.id}`);
          });
        });
      }

      // Update growth stats
      if (data.growth) {
        const growthDiv = container.querySelector('.growth-stats');
        growthDiv.innerHTML = `
          <div class="growth-item">
            <span class="label">За 7 дней:</span>
            <span class="value">+${data.growth.prompts_7d || 0}</span>
            <span class="rate" style="color: ${data.growth.growth_rate_7d > 0 ? '#10b981' : '#ef4444'}">
              ${data.growth.growth_rate_7d > 0 ? '↑' : '↓'} ${Math.abs(data.growth.growth_rate_7d || 0).toFixed(1)}%
            </span>
          </div>
        `;
      }
    }).catch(err => {
      console.warn('Failed to load dashboard data:', err);
    });
  }

  // Setup event listeners
  container.querySelectorAll('[data-action]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const action = e.target.closest('[data-action]').dataset.action;
      
      if (action === 'new-prompt' && window.router) {
        window.router.navigate('/editor');
      } else if (action === 'new-project') {
        window.dispatchEvent(new CustomEvent('project:create'));
      }
    });
  });

  return container;
}
