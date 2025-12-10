// Very small hash-based router
export default class Router {
  constructor() {
    this.routes = new Map();
    window.addEventListener('hashchange', () => this._onHashChange());
  }

  addRoute(path, loader) {
    this.routes.set(path, loader);
  }

  async _onHashChange() {
    const path = location.hash.replace('#', '') || '/';
    await this.navigate(path);
  }

  async navigate(path) {
    const loader = this.routes.get(path) || this.routes.get('/dashboard');
    if (loader) {
      try {
        const viewFactory = await loader();
        const el = document.getElementById('app');
        if (el && viewFactory) {
          el.innerHTML = '';
          el.appendChild(viewFactory);
        }
      } catch (e) {
        console.error('Router navigate error', e);
      }
    }
  }
}
