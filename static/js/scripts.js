// static/js/main.js

document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // ========================================
    // 1. БУРГЕР-МЕНЮ
    // ========================================
    const burger = document.getElementById('burger');
    const nav = document.getElementById('nav');

    if (burger && nav) {
        const toggleMenu = () => {
            burger.classList.toggle('active');
            nav.classList.toggle('active');
            document.body.style.overflow = nav.classList.contains('active') ? 'hidden' : '';
        };

        burger.addEventListener('click', toggleMenu);

        // Закрытие при клике на ссылку
        nav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                burger.classList.remove('active');
                nav.classList.remove('active');
                document.body.style.overflow = '';
            });
        });

        // Закрытие при клике вне меню
        document.addEventListener('click', (e) => {
            if (!burger.contains(e.target) && !nav.contains(e.target)) {
                burger.classList.remove('active');
                nav.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    // ========================================
    // 2. КНОПКА "НАВЕРХ"
    // ========================================
    const scrollTop = document.getElementById('scrollTop');

    if (scrollTop) {
        const toggleScrollTop = () => {
            if (window.pageYOffset > 400) {
                scrollTop.classList.add('visible');
            } else {
                scrollTop.classList.remove('visible');
            }
        };

        window.addEventListener('scroll', throttle(toggleScrollTop, 100));
        scrollTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        // Инициализация при загрузке
        toggleScrollTop();
    }

    // ========================================
    // 3. ПЛАВНАЯ ПРОКРУТКА К ЯКОРЯМ
    // ========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#' || href === '#!') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const offsetTop = target.getBoundingClientRect().top + window.pageYOffset - 80;

                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });

                // Закрываем мобильное меню, если открыто
                if (nav && nav.classList.contains('active')) {
                    burger.classList.remove('active');
                    nav.classList.remove('active');
                    document.body.style.overflow = '';
                }
            }
        });
    });

    // ========================================
    // 4. ЛЕНИВАЯ ЗАГРУЗКА ИЗОБРАЖЕНИЙ
    // ========================================
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        img.classList.add('loaded');
                    }
                    observer.unobserve(img);
                }
            });
        }, { rootMargin: '50px' });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // ========================================
    // 5. АНИМАЦИЯ ПОЯВЛЕНИЯ ПРИ СКРОЛЛЕ
    // ========================================
    const animateElements = document.querySelectorAll('.animate-on-scroll');

    const checkAnimation = () => {
        const triggerBottom = window.innerHeight * 0.85;

        animateElements.forEach(el => {
            const elTop = el.getBoundingClientRect().top;
            if (elTop < triggerBottom) {
                el.classList.add('animated');
            }
        });
    };

    if (animateElements.length > 0) {
        window.addEventListener('scroll', throttle(checkAnimation, 50));
        checkAnimation();
    }

    // ========================================
    // 6. АВТОЗАКРЫТИЕ АЛЕРТОВ
    // ========================================
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.4s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 400);
        }, 5000);
    });

    // ========================================
    // 7. ПОДТВЕРЖДЕНИЕ УДАЛЕНИЯ
    // ========================================
    document.querySelectorAll('[data-confirm]').forEach(el => {
        el.addEventListener('click', function (e) {
            const message = this.getAttribute('data-confirm') || 'Вы уверены, что хотите удалить?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // ========================================
    // 8. ПЛАВНОЕ ПОЯВЛЕНИЕ СТРАНИЦЫ
    // ========================================
    document.body.style.opacity = '0';
    window.addEventListener('load', () => {
        setTimeout(() => {
            document.body.style.transition = 'opacity 0.7s ease';
            document.body.style.opacity = '1';
        }, 50);
    });
});

// ========================================
// УТИЛИТЫ
// ========================================

// Debounce — задержка выполнения
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle — ограничение частоты
function throttle(func, limit) {
    let inThrottle;
    return function (...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Форматирование цены
window.formatPrice = function (price) {
    return new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
};

// Показ/скрытие элемента с анимацией
window.toggleElement = function (element, show) {
    if (!element) return;
    element.style.transition = 'opacity 0.3s ease';
    if (show) {
        element.style.display = 'block';
        setTimeout(() => element.style.opacity = '1', 10);
    } else {
        element.style.opacity = '0';
        setTimeout(() => element.style.display = 'none', 300);
    }
};
