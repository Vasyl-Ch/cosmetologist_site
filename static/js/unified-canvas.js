// static/js/unified-canvas.js
// Фіксована швидкість + виправлення Back button

(function() {
    'use strict';

    class UnifiedParticleCanvas {
        constructor(canvasId) {
            this.canvas = document.getElementById(canvasId);
            if (!this.canvas) return;

            this.ctx = this.canvas.getContext('2d');
            this.particles = [];
            this.animationId = null;
            this.mouse = { x: -9999, y: -9999, radius: 120 };
            this.time = 0;
            this.lastTime = 0;
            this.fixedSpeed = 0.15; // ФІКСОВАНА ШВИДКІСТЬ (пікселів за кадр)

            this.init();
            this.setupMouseTracking();
            this.setupPageVisibility(); // Додано: для Back button
        }

        resizeCanvas() {
            this.canvas.width = this.canvas.offsetWidth;
            this.canvas.height = this.canvas.offsetHeight;
        }

        createParticle() {
            const baseOpacity = Math.random() * 0.4 + 0.6;
            return {
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                baseSize: Math.random() * 3 + 2,
                size: 0,
                // ФІКСОВАНА швидкість (напрямок випадковий, але швидкість — константа)
                dirX: (Math.random() - 0.5) * 2,
                dirY: (Math.random() - 0.5) * 2,
                opacity: baseOpacity,
                baseOpacity: baseOpacity,
                pulsePhase: Math.random() * Math.PI * 2,
                pulseSpeed: Math.random() * 0.03 + 0.02
            };
        }

        updateParticle(particle, deltaTime) {
            // Пульсація
            const pulse = Math.sin(this.time * particle.pulseSpeed + particle.pulsePhase);
            particle.size = particle.baseSize + pulse * 1.5;
            particle.opacity = particle.baseOpacity + pulse * 0.2;
            particle.opacity = Math.max(0.4, Math.min(1, particle.opacity));

            // ФІКСОВАНА швидкість: this.fixedSpeed пікселів/кадр
            const speed = this.fixedSpeed;
            const vx = particle.dirX * speed;
            const vy = particle.dirY * speed;

            particle.x += vx;
            particle.y += vy;

            // Обмеження по краях
            if (particle.x > this.canvas.width) particle.x = 0;
            if (particle.x < 0) particle.x = this.canvas.width;
            if (particle.y > this.canvas.height) particle.y = 0;
            if (particle.y < 0) particle.y = this.canvas.height;

            // Реакція на мишку
            const dx = this.mouse.x - particle.x;
            const dy = this.mouse.y - particle.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < this.mouse.radius && distance > 0) {
                const force = (this.mouse.radius - distance) / this.mouse.radius;
                const angle = Math.atan2(dy, dx);
                const pushX = Math.cos(angle) * force * 1.8;
                const pushY = Math.sin(angle) * force * 1.8;

                particle.x -= pushX;
                particle.y -= pushY;
                particle.opacity = Math.min(1, particle.opacity + force * 0.4);
            }
        }

        drawParticle(particle) {
            this.ctx.save();

            const glow = particle.opacity > 0.8 ? 25 : 15;
            this.ctx.shadowBlur = glow;
            this.ctx.shadowColor = `rgba(255, 100, 180, ${particle.opacity})`;
            this.ctx.fillStyle = `rgba(255, 130, 190, ${particle.opacity})`;
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, Math.max(particle.size, 1), 0, Math.PI * 2);
            this.ctx.fill();

            this.ctx.restore();
        }

        connectParticles() {
            const maxDistance = 140;
            for (let i = 0; i < this.particles.length; i++) {
                for (let j = i + 1; j < this.particles.length; j++) {
                    const dx = this.particles[i].x - this.particles[j].x;
                    const dy = this.particles[i].y - this.particles[j].y;
                    const distance = Math.sqrt(dx * dx + dy * dy);

                    if (distance < maxDistance) {
                        const opacity = (1 - distance / maxDistance) * 0.6;
                        this.ctx.strokeStyle = `rgba(255, 140, 200, ${opacity})`;
                        this.ctx.lineWidth = 1.3;
                        this.ctx.beginPath();
                        this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
                        this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
                        this.ctx.stroke();
                    }
                }
            }
        }

        setupMouseTracking() {
            const updateMouse = (e, isTouch = false) => {
                const rect = this.canvas.getBoundingClientRect();
                const clientX = isTouch ? e.touches[0].clientX : e.clientX;
                const clientY = isTouch ? e.touches[0].clientY : e.clientY;
                this.mouse.x = clientX - rect.left;
                this.mouse.y = clientY - rect.top;
            };

            this.canvas.addEventListener('mousemove', (e) => updateMouse(e));
            this.canvas.addEventListener('mouseleave', () => {
                this.mouse.x = -9999;
                this.mouse.y = -9999;
            });

            this.canvas.addEventListener('touchmove', (e) => {
                e.preventDefault();
                updateMouse(e, true);
            }, { passive: false });

            this.canvas.addEventListener('touchend', () => {
                this.mouse.x = -9999;
                this.mouse.y = -9999;
            });
        }

        // НОВЕ: Відновлення анімації при поверненні на сторінку
        setupPageVisibility() {
            document.addEventListener('visibilitychange', () => {
                if (!document.hidden) {
                    // Сторінка знову видима — перезапускаємо
                    this.restartAnimation();
                } else {
                    // Прихована — зупиняємо
                    this.destroy();
                }
            });

            window.addEventListener('pageshow', (e) => {
                if (e.persisted || window.performance?.navigation?.type === 2) {
                    this.restartAnimation();
                }
            });
        }

        restartAnimation() {
            this.destroy();
            this.init();
        }

        init() {
            this.resizeCanvas();
            this.particles = [];
            this.time = 0;
            this.lastTime = performance.now();

            const particleCount = Math.min(Math.floor(this.canvas.width / 5), 180);
            for (let i = 0; i < particleCount; i++) {
                this.particles.push(this.createParticle());
            }

            this.animate();
            this.setupResizeHandler();
        }

        setupResizeHandler() {
            let resizeTimeout;
            const handler = () => {
                clearTimeout(resizeTimeout);
                resizeTimeout = setTimeout(() => {
                    this.resizeCanvas();
                    this.init(); // Перезавантажуємо частинки
                }, 100);
            };
            window.addEventListener('resize', handler);

            // Очищення
            window.addEventListener('beforeunload', () => {
                window.removeEventListener('resize', handler);
            });
        }

        animate(currentTime = performance.now()) {
            const deltaTime = currentTime - this.lastTime;
            this.lastTime = currentTime;

            // Оновлюємо час для пульсації (незалежно від FPS)
            this.time += 0.016; // ~60 FPS

            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

            this.particles.forEach(particle => {
                this.updateParticle(particle, deltaTime);
                this.drawParticle(particle);
            });

            this.connectParticles();

            this.animationId = requestAnimationFrame((t) => this.animate(t));
        }

        destroy() {
            if (this.animationId) {
                cancelAnimationFrame(this.animationId);
                this.animationId = null;
            }
        }
    }

    // === АВТОІНІЦІАЛІЗАЦІЯ З ПІДТРИМКОЮ BACK BUTTON ===
    let canvasInstances = new Map();

    function initCanvas(id) {
        if (document.getElementById(id)) {
            const instance = new UnifiedParticleCanvas(id);
            canvasInstances.set(id, instance);
        }
    }

    function destroyAll() {
        canvasInstances.forEach(inst => inst.destroy());
        canvasInstances.clear();
    }

    document.addEventListener('DOMContentLoaded', () => {
        destroyAll(); // На випадок, якщо скрипт завантажився повторно
        const canvasIds = [
            'heroCanvas', 'articlesCanvas', 'articleCanvas',
            'brandsCanvas', 'productsCanvas', 'proceduresCanvas',
            'proceduresDetailCanvas', 'contactsCanvas'
        ];
        canvasIds.forEach(initCanvas);
    });

    // Підтримка SPA та Back button
    window.addEventListener('pagehide', destroyAll);
    window.addEventListener('pageshow', () => {
        setTimeout(() => {
            const canvasIds = [
                'heroCanvas', 'articlesCanvas', 'articleCanvas',
                'brandsCanvas', 'productsCanvas', 'proceduresCanvas',
                'proceduresDetailCanvas', 'contactsCanvas'
            ];
            canvasIds.forEach(initCanvas);
        }, 50);
    });

    window.UnifiedParticleCanvas = UnifiedParticleCanvas;
})();
