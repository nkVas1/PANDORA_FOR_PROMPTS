/**
 * Loading Screen Manager
 * Управляет HTML загрузочным экраном во время инициализации приложения
 */

class LoadingScreenManager {
  constructor() {
    this.element = document.getElementById('loading-screen');
    this.progressFill = document.getElementById('loading-progress-fill');
    this.progressText = document.getElementById('loading-progress-text');
    this.statusElements = {
      initialized: document.getElementById('status-initialized'),
      api: document.getElementById('status-api'),
      data: document.getElementById('status-data'),
      ready: document.getElementById('status-ready'),
    };
  }

  /**
   * Обновить прогресс загрузки
   */
  setProgress(percent) {
    if (this.progressFill) {
      this.progressFill.style.width = `${Math.min(percent, 100)}%`;
    }
    if (this.progressText) {
      this.progressText.textContent = `${Math.round(percent)}%`;
    }
  }

  /**
   * Обновить текст прогресса
   */
  setMessage(message) {
    if (this.progressText) {
      this.progressText.textContent = message;
    }
  }

  /**
   * Обновить статус элемента
   * status: 0 = ожидание, 1 = готово, 2 = загружается
   */
  setStatus(key, status) {
    const element = this.statusElements[key];
    if (element) {
      element.setAttribute('data-status', status);
    }
  }

  /**
   * Скрыть loading screen с анимацией
   */
  hide() {
    if (this.element) {
      this.element.classList.remove('loading-screen--visible');
      // Удалить через 600ms после начала анимации выхода
      setTimeout(() => {
        if (this.element && this.element.parentNode) {
          this.element.parentNode.removeChild(this.element);
        }
      }, 600);
    }
  }

  /**
   * Показать loading screen
   */
  show() {
    if (this.element) {
      this.element.classList.add('loading-screen--visible');
    }
  }

  /**
   * Полный цикл загрузки с примерным прогрессом
   */
  async simulateLoad(duration = 3000) {
    const steps = 20;
    const stepDuration = duration / steps;
    let currentStep = 0;

    const progressSequence = [
      { percent: 5, key: 'initialized', status: 1, message: 'Инициализация ядра...' },
      { percent: 15, key: 'initialized', status: 2, message: 'Загрузка конфигурации...' },
      { percent: 30, key: 'api', status: 1, message: 'Проверка API...' },
      { percent: 45, key: 'api', status: 2, message: 'Подключение к серверу...' },
      { percent: 60, key: 'data', status: 1, message: 'Загрузка данных...' },
      { percent: 75, key: 'data', status: 2, message: 'Обработка информации...' },
      { percent: 90, key: 'ready', status: 1, message: 'Завершение инициализации...' },
      { percent: 100, key: 'ready', status: 2, message: 'Готово!', hideDelay: 500 },
    ];

    for (const step of progressSequence) {
      this.setProgress(step.percent);
      if (step.message) {
        this.setMessage(step.message);
      }
      if (step.key) {
        this.setStatus(step.key, step.status);
      }

      await new Promise(resolve => setTimeout(resolve, stepDuration * (step.percent / 100)));
    }

    // Дождаться завершения перед скрытием
    await new Promise(resolve => setTimeout(resolve, 300));
    this.hide();
  }
}

// Экспортировать для использования в app.js
window.LoadingScreenManager = LoadingScreenManager;

// Инициализировать при загрузке документа
let loadingScreen = null;
document.addEventListener('DOMContentLoaded', () => {
  loadingScreen = new LoadingScreenManager();
  console.log('[LoadingScreen] Initialized');
});
