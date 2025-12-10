// Minimal Dashboard view factory
export default function createDashboard() {
  const container = document.createElement('div');
  container.className = 'dashboard';

  const header = document.createElement('h1');
  header.textContent = 'PANDORA — Dashboard';
  container.appendChild(header);

  const stats = document.createElement('div');
  stats.className = 'dashboard-stats';
  stats.innerHTML = `\
    <div class="card">\
      <h3>Total Prompts</h3>\
      <div id="total-prompts">0</div>\
    </div>\
    <div class="card">\
      <h3>Total Projects</h3>\
      <div id="total-projects">0</div>\
    </div>`;

  container.appendChild(stats);

  // Fetch simple stats if http available
  if (window.http) {
    window.http.get('/analytics/dashboard').then(resp => {
      try {
        const data = resp.data || resp;
        const tp = data.totals ? data.totals.prompts : 0;
        const tpr = data.totals ? data.totals.projects : 0;
        const elTp = container.querySelector('#total-prompts');
        const elTpr = container.querySelector('#total-projects');
        if (elTp) elTp.textContent = tp;
        if (elTpr) elTpr.textContent = tpr;
      } catch (e) {
        console.warn('Failed to parse dashboard response', e);
      }
    }).catch(() => {});
  }

  return container;
}
