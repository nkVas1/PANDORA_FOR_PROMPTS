/**
 * AnimatedGradientMesh - Canvas-based animated background with gradient orbs
 * 
 * Features:
 * - 5-color particle system
 * - Organic motion simulation
 * - Smooth gradient blending
 * - Responsive to viewport
 * - Configurable animation speed
 */

export class AnimatedGradientMesh {
  constructor(canvas, options = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.width = canvas.width;
    this.height = canvas.height;
    this.particles = [];
    this.animationId = null;
    this.isRunning = false;

    // Options
    this.particleCount = options.particleCount || 5;
    this.speed = options.speed || 0.5;
    this.colors = options.colors || [
      '#6366f1', // indigo
      '#ec4899', // pink
      '#10b981', // emerald
      '#f59e0b', // amber
      '#3b82f6'  // blue
    ];

    this.init();
  }

  /**
   * Initialize particles
   */
  init() {
    this.particles = [];
    for (let i = 0; i < this.particleCount; i++) {
      this.particles.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        vx: (Math.random() - 0.5) * this.speed,
        vy: (Math.random() - 0.5) * this.speed,
        radius: (50 + Math.random() * 100),
        color: this.colors[i % this.colors.length],
        angle: Math.random() * Math.PI * 2
      });
    }
  }

  /**
   * Start animation
   */
  start() {
    if (this.isRunning) return;
    this.isRunning = true;
    this.animate();
  }

  /**
   * Stop animation
   */
  stop() {
    this.isRunning = false;
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
    }
  }

  /**
   * Animation loop
   */
  animate = () => {
    if (!this.isRunning) return;

    // Clear canvas
    this.ctx.clearRect(0, 0, this.width, this.height);

    // Update and draw particles
    this.particles.forEach((p, i) => {
      // Update position with sine/cosine motion
      p.angle += 0.002;
      p.x += Math.cos(p.angle) * p.vx;
      p.y += Math.sin(p.angle) * p.vy;

      // Bounce off edges
      if (p.x - p.radius < 0 || p.x + p.radius > this.width) {
        p.vx *= -1;
      }
      if (p.y - p.radius < 0 || p.y + p.radius > this.height) {
        p.vy *= -1;
      }

      // Draw circle with gradient
      const gradient = this.ctx.createRadialGradient(
        p.x, p.y, 0,
        p.x, p.y, p.radius
      );
      gradient.addColorStop(0, p.color + '80'); // Semi-transparent
      gradient.addColorStop(1, p.color + '00'); // Fully transparent

      this.ctx.fillStyle = gradient;
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      this.ctx.fill();
    });

    this.animationId = requestAnimationFrame(this.animate);
  };

  /**
   * Handle window resize
   */
  handleResize() {
    this.width = this.canvas.width;
    this.height = this.canvas.height;
  }
}
