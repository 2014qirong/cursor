/**
 * main.js - 全局脚本文件
 * 包含网站通用功能和导航栏逻辑
 */

// 导航栏处理
function initNavigation() {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li');
    const body = document.body;

    // 汉堡按钮点击事件
    if (burger) {
        burger.addEventListener('click', () => {
            // 切换导航栏显示
            nav.classList.toggle('nav-active');
            // 防止滚动
            body.classList.toggle('no-scroll');

            // 导航链接动画
            navLinks.forEach((link, index) => {
                if (link.style.animation) {
                    link.style.animation = '';
                } else {
                    link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
                }
            });

            // 汉堡按钮动画
            burger.classList.toggle('toggle');
        });
    }

    // 点击导航链接关闭菜单
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (nav.classList.contains('nav-active')) {
                nav.classList.remove('nav-active');
                burger.classList.remove('toggle');
                body.classList.remove('no-scroll');
                navLinks.forEach(link => {
                    link.style.animation = '';
                });
            }
        });
    });

    // 点击外部关闭菜单
    document.addEventListener('click', (e) => {
        if (nav.classList.contains('nav-active') && 
            !nav.contains(e.target) && 
            !burger.contains(e.target)) {
            nav.classList.remove('nav-active');
            burger.classList.remove('toggle');
            body.classList.remove('no-scroll');
            navLinks.forEach(link => {
                link.style.animation = '';
            });
        }
    });

    // 添加平滑滚动效果
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

// 工具卡片高亮效果
function initToolCards() {
    const toolCards = document.querySelectorAll('.tool-card');
    
    toolCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px)';
            card.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.1)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
            card.style.boxShadow = '';
        });
    });
}

// 添加CSS动画
function addAnimationStyles() {
    if (!document.getElementById('dynamic-styles')) {
        const style = document.createElement('style');
        style.id = 'dynamic-styles';
        style.textContent = `
            @keyframes navLinkFade {
                from {
                    opacity: 0;
                    transform: translateX(50px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            .toggle .line1 {
                transform: rotate(-45deg) translate(-5px, 6px);
            }
            
            .toggle .line2 {
                opacity: 0;
            }
            
            .toggle .line3 {
                transform: rotate(45deg) translate(-5px, -6px);
            }
            
            .no-scroll {
                overflow: hidden;
            }
        `;
        document.head.appendChild(style);
    }
}

// 实用函数：显示通知消息
function showNotification(message, type = 'info', duration = 3000) {
    // 移除现有通知
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => {
        notification.remove();
    });

    // 创建新通知
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // 添加到页面
    document.body.appendChild(notification);

    // 显示动画
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    // 自动隐藏
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, duration);
}

// 在页面加载完成后执行初始化
document.addEventListener('DOMContentLoaded', () => {
    addAnimationStyles();
    initNavigation();
    initToolCards();

    // 检查URL参数，如果有消息参数则显示通知
    const urlParams = new URLSearchParams(window.location.search);
    const message = urlParams.get('message');
    const type = urlParams.get('type') || 'info';
    
    if (message) {
        showNotification(decodeURIComponent(message), type);
        // 清除URL参数
        window.history.replaceState({}, document.title, window.location.pathname);
    }
}); 