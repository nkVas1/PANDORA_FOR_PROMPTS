/**
 * Card Component - Glass morphism card with ripple effect
 * 
 * Features:
 * - Glass morphism design
 * - Ripple effect on hover
 * - Customizable styling
 * - Responsive
 */

export function createGlassCard(options = {}) {
  const card = document.createElement('div');
  card.className = `glass-card ${options.className || ''}`;
  
  if (options.title) {
    const title = document.createElement('h3');
    title.className = 'glass-card__title';
    title.textContent = options.title;
    card.appendChild(title);
  }
  
  if (options.content) {
    const content = document.createElement('div');
    content.className = 'glass-card__content';
    if (typeof options.content === 'string') {
      content.innerHTML = options.content;
    } else {
      content.appendChild(options.content);
    }
    card.appendChild(content);
  }
  
  if (options.footer) {
    const footer = document.createElement('div');
    footer.className = 'glass-card__footer';
    footer.appendChild(options.footer);
    card.appendChild(footer);
  }
  
  // Add ripple effect
  card.addEventListener('click', (e) => {
    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    
    card.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });
  
  return card;
}

/**
 * StatCard - Card with stat display
 */
export function createStatCard(icon, label, value, trend = null) {
  const card = document.createElement('div');
  card.className = 'stat-card';
  
  let trendHTML = '';
  if (trend) {
    const trendColor = trend.value > 0 ? '#10b981' : '#ef4444';
    const trendArrow = trend.value > 0 ? '↑' : '↓';
    trendHTML = `<span class="stat-card__trend" style="color: ${trendColor}">${trendArrow} ${Math.abs(trend.value)}%</span>`;
  }
  
  card.innerHTML = `
    <div class="stat-card__icon">${icon}</div>
    <div class="stat-card__content">
      <div class="stat-card__label">${label}</div>
      <div class="stat-card__value">${value}</div>
      ${trendHTML}
    </div>
  `;
  
  return card;
}
