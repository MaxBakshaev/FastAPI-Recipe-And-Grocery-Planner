document.addEventListener('DOMContentLoaded', () => {
  const gallery = document.getElementById('recipe-gallery');
  const token = localStorage.getItem('access_token');
  const isAuthenticated = !!token;

  fetch('/api/v1/recipes/')
      .then(response => {
          if (!response.ok) throw new Error("Ошибка загрузки данных");
          return response.json();
      })
      .then(data => {
          if (!Array.isArray(data) || data.length === 0) {
              gallery.innerHTML = '<p class="text-center">Рецепты не найдены</p>';
              return;
          }

          data.forEach(recipe => {
              const article = document.createElement('article');
              article.className = 'recipe-article';
              article.dataset.recipeId = recipe.id;

              const imageUrl = recipe.image_url || '/static/img/products.jpg';

              // Показываем кнопку сохранения только для авторизованных пользователей
              const saveButton = isAuthenticated ? `
                  <div class="recipe-actions">
                      <button class="save-recipe-btn ${recipe.is_saved ? 'saved' : ''}" 
                              onclick="toggleSaveRecipe(${recipe.id}, this)">
                          ${recipe.is_saved ? '✓ Сохранено' : 'Сохранить'}
                      </button>
                  </div>
              ` : '';

              // Определяем имя автора
              const authorName = recipe.username || `пользователь #${recipe.user_id}`;

              article.innerHTML = `
                  <div class="recipe-container">
                      <div class="recipe-image-wrapper">
                          <img src="${imageUrl}" alt="${recipe.title}" class="recipe-img" 
                              onerror="this.src='/static/img/products.jpg'" />
                          <p class="recipe-meta">${recipe.total_calories} ккал / ${recipe.total_quantity} г.</p>
                          ${saveButton}
                      </div>
                      <div class="recipe-info">
                          <h4 class="recipe-title">${recipe.title}</h4>
                          <p class="recipe-description">${recipe.body}</p>
                          <div class="recipe-author">
                              <small>Автор: ${authorName}</small>
                          </div>
                      </div>
                  </div>
              `;

              gallery.appendChild(article);
          });
      })
      .catch(err => {
          console.error('Ошибка загрузки рецептов:', err);
          gallery.innerHTML = '<p class="text-center">Не удалось загрузить рецепты</p>';
      });
});

// Функция сохранения/удаления рецепта
window.toggleSaveRecipe = async function(recipeId, button) {
  const token = localStorage.getItem('access_token');
  if (!token) {
      alert('Пожалуйста, войдите в систему чтобы сохранять рецепты');
      return;
  }

  const isCurrentlySaved = button.classList.contains('saved');
  
  try {
      let response;
      if (isCurrentlySaved) {
          // Удаляем из сохраненных
          response = await fetch(`/api/v1/saved-recipes/${recipeId}/`, {
              method: 'DELETE',
              headers: {
                  'Authorization': `Bearer ${token}`
              }
          });
      } else {
          // Сохраняем рецепт
          response = await fetch('/api/v1/saved-recipes/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
              },
              body: JSON.stringify({ recipe_id: recipeId })
          });
      }

      if (response.ok) {
          // Обновляем состояние кнопки
          button.classList.toggle('saved');
          button.textContent = isCurrentlySaved ? 'Сохранить' : '✓ Сохранено';
          
          // Показываем уведомление
          showNotification(isCurrentlySaved ? 'Рецепт удален из сохраненных' : 'Рецепт сохранен!');
      } else {
          const error = await response.json();
          alert(error.detail || 'Произошла ошибка');
      }
  } catch (error) {
      console.error('Ошибка:', error);
      alert('Произошла ошибка при сохранении рецепта');
  }
}

// Функция показа уведомления
function showNotification(message) {
  const notification = document.createElement('div');
  notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: #28a745;
      color: white;
      padding: 15px 20px;
      border-radius: 5px;
      z-index: 1000;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      animation: slideIn 0.3s ease;
  `;
  notification.textContent = message;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
      notification.style.animation = 'slideOut 0.3s ease';
      setTimeout(() => {
          if (notification.parentNode) {
              document.body.removeChild(notification);
          }
      }, 300);
  }, 3000);
}

// Добавляем CSS анимации
if (!document.querySelector('style[data-recipes-gallery]')) {
  const style = document.createElement('style');
  style.setAttribute('data-recipes-gallery', 'true');
  style.textContent = `
      @keyframes slideIn {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
      }
      @keyframes slideOut {
          from { transform: translateX(0); opacity: 1; }
          to { transform: translateX(100%); opacity: 0; }
      }
      
      .save-recipe-btn {
          background: #6c757d;
          color: white;
          border: none;
          padding: 8px 15px;
          border-radius: 5px;
          cursor: pointer;
          font-size: 0.9rem;
          transition: all 0.3s ease;
          width: 100%;
          margin-top: 10px;
      }
      
      .save-recipe-btn.saved {
          background: #28a745;
      }
      
      .save-recipe-btn:hover {
          opacity: 0.9;
          transform: translateY(-1px);
      }
      
      .recipe-actions {
          margin-top: 10px;
      }
  `;
  document.head.appendChild(style);
}