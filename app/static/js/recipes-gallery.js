document.addEventListener('DOMContentLoaded', () => {
  const gallery = document.getElementById('recipe-gallery');

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

        // Используем картинку рецепта или заглушку
        const imageUrl = recipe.image_url || '/static/img/products.jpg';

        article.innerHTML = `
          <div class="recipe-container">
            <div class="recipe-image-wrapper">
              <img src="${imageUrl}" alt="${recipe.title}" class="recipe-img" 
                   onerror="this.src='/static/img/products.jpg'" />
              <p class="recipe-meta">${recipe.total_calories} ккал / ${recipe.total_quantity} г.</p>
            </div>
            <div class="recipe-info">
              <h4 class="recipe-title">${recipe.title}</h4>
              <p class="recipe-description">${recipe.body}</p>
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