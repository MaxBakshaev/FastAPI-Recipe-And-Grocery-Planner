// Функция для обновления видимости меню
function updateMenuVisibility() {
    const token = localStorage.getItem('access_token');
    const isAuthenticated = !!token;

    // Показываем/скрываем пункты меню в зависимости от аутентификации
    document.querySelectorAll('.menu-home').forEach(el => el.classList.toggle('hidden', false)); // Главная всегда видна
    
    // Для авторизованных пользователей
    document.querySelectorAll('.menu-planner, .menu-recipes, .menu-profile, .menu-logout').forEach(el => {
        el.classList.toggle('hidden', !isAuthenticated);
    });
    
    // Для гостей
    document.querySelectorAll('.menu-login, .menu-register').forEach(el => {
        el.classList.toggle('hidden', isAuthenticated);
    });
}

// Обновляем меню при загрузке страницы
document.addEventListener('DOMContentLoaded', updateMenuVisibility);

// Также обновляем при изменении localStorage (если вход/выход на других вкладках)
window.addEventListener('storage', updateMenuVisibility);