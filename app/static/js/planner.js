document.addEventListener('DOMContentLoaded', () => {
    const gallery = document.getElementById('saved-recipes-gallery');
    const searchInput = document.getElementById('search-input');
    const sortSelect = document.getElementById('sort-select');
    const clearFilters = document.getElementById('clear-filters');
    const selectedRecipesContainer = document.getElementById('selected-recipes');
    const groceryListContainer = document.getElementById('grocery-list');
    const groceryItems = document.getElementById('grocery-items');
    const clearGroceryList = document.getElementById('clear-grocery-list');

    let savedRecipes = [];
    let selectedRecipes = new Set();

    // Загрузка сохраненных рецептов
    async function loadSavedRecipes() {
        try {
            const token = localStorage.getItem('access_token');
            if (!token) {
                gallery.innerHTML = '<p class="text-center">Пожалуйста, войдите в систему</p>';
                return;
            }

            const response = await fetch('/api/v1/saved-recipes/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Ошибка загрузки сохраненных рецептов');
            }

            savedRecipes = await response.json();
            renderRecipes(savedRecipes);
            updateStatistics(savedRecipes);
        } catch (error) {
            console.error('Ошибка загрузки рецептов:', error);
            gallery.innerHTML = '<p class="text-center">Не удалось загрузить сохраненные рецепты</p>';
        }
    }

    // Рендеринг рецептов
    function renderRecipes(recipes) {
        if (!Array.isArray(recipes) || recipes.length === 0) {
            gallery.innerHTML = '<p class="text-center">У вас пока нет сохраненных рецептов</p>';
            return;
        }

        gallery.innerHTML = '';

        recipes.forEach(recipe => {
            const article = document.createElement('article');
            article.className = 'recipe-article';
            article.dataset.recipeId = recipe.id;

            const imageUrl = recipe.image_url || '/static/img/products.jpg';
            const isSelected = selectedRecipes.has(recipe.id);

            article.innerHTML = `
                <div class="recipe-container ${isSelected ? 'selected' : ''}">
                    <div class="recipe-image-wrapper">
                        <img src="${imageUrl}" alt="${recipe.title}" class="recipe-img" 
                             onerror="this.src='/static/img/products.jpg'" />
                        <p class="recipe-meta">${recipe.total_calories} ккал / ${recipe.total_quantity} г.</p>
                        <div class="recipe-actions">
                            <button class="select-recipe-btn ${isSelected ? 'selected' : ''}" 
                                    onclick="toggleRecipeSelection(${recipe.id})">
                                ${isSelected ? '✓ Выбран' : 'Выбрать'}
                            </button>
                            <button class="unsave-recipe-btn" onclick="unsaveRecipe(${recipe.id})">
                                Удалить
                            </button>
                        </div>
                    </div>
                    <div class="recipe-info">
                        <h4 class="recipe-title">${recipe.title}</h4>
                        <p class="recipe-description">${recipe.body}</p>
                        <div class="recipe-products">
                            <strong>Продукты:</strong>
                            <ul>
                                ${recipe.products.map(product => 
                                    `<li>${product.quantity}g - Product ID: ${product.product_id}</li>`
                                ).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
            `;

            gallery.appendChild(article);
        });
    }

    // Обновление статистики
    function updateStatistics(recipes) {
        const totalRecipes = document.getElementById('total-recipes');
        const totalCalories = document.getElementById('total-calories');
        const totalWeight = document.getElementById('total-weight');

        totalRecipes.textContent = recipes.length;
        
        const totalCal = recipes.reduce((sum, recipe) => sum + recipe.total_calories, 0);
        const totalWgt = recipes.reduce((sum, recipe) => sum + recipe.total_quantity, 0);

        totalCalories.textContent = totalCal.toLocaleString();
        totalWeight.textContent = totalWgt.toLocaleString();
    }

    // Фильтрация и сортировка
    function filterAndSortRecipes() {
        let filtered = [...savedRecipes];

        // Поиск
        const searchTerm = searchInput.value.toLowerCase();
        if (searchTerm) {
            filtered = filtered.filter(recipe => 
                recipe.title.toLowerCase().includes(searchTerm) ||
                recipe.body.toLowerCase().includes(searchTerm)
            );
        }

        // Сортировка
        const sortBy = sortSelect.value;
        switch (sortBy) {
            case 'title':
                filtered.sort((a, b) => a.title.localeCompare(b.title, 'ru'));
                break;
            case 'calories':
                filtered.sort((a, b) => b.total_calories - a.total_calories);
                break;
            case 'weight':
                filtered.sort((a, b) => b.total_quantity - a.total_quantity);
                break;
            case 'newest':
                // По умолчанию уже новые сначала
                break;
        }

        renderRecipes(filtered);
    }

    // Управление выбором рецептов для списка покупок
    window.toggleRecipeSelection = function(recipeId) {
        if (selectedRecipes.has(recipeId)) {
            selectedRecipes.delete(recipeId);
        } else {
            selectedRecipes.add(recipeId);
        }

        updateSelectedRecipesDisplay();
        updateGroceryList();
        loadSavedRecipes(); // Перерисовываем для обновления стилей кнопок
    }

    function updateSelectedRecipesDisplay() {
        if (selectedRecipes.size === 0) {
            selectedRecipesContainer.innerHTML = '<p>Выберите рецепты для формирования списка покупок</p>';
            return;
        }

        const selectedNames = Array.from(selectedRecipes).map(id => {
            const recipe = savedRecipes.find(r => r.id === id);
            return recipe ? recipe.title : 'Неизвестный рецепт';
        });

        selectedRecipesContainer.innerHTML = `
            <h5>Выбранные рецепты (${selectedRecipes.size}):</h5>
            <ul>
                ${selectedNames.map(name => `<li>${name}</li>`).join('')}
            </ul>
        `;
    }

    function updateGroceryList() {
        if (selectedRecipes.size === 0) {
            groceryListContainer.style.display = 'none';
            return;
        }

        // Здесь можно добавить логику для агрегации продуктов из выбранных рецептов
        // Пока просто показываем контейнер
        groceryListContainer.style.display = 'block';
        groceryItems.innerHTML = `
            <li>Функциональность агрегации продуктов будет добавлена позже</li>
            <li>Выбрано рецептов: ${selectedRecipes.size}</li>
        `;
    }

    // Удаление рецепта из сохраненных
    window.unsaveRecipe = async function(recipeId) {
        if (!confirm('Удалить этот рецепт из сохраненных?')) {
            return;
        }

        try {
            const token = localStorage.getItem('access_token');
            const response = await fetch(`/api/v1/saved-recipes/${recipeId}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                // Удаляем из выбранных если был выбран
                selectedRecipes.delete(recipeId);
                // Перезагружаем список
                loadSavedRecipes();
                updateSelectedRecipesDisplay();
                updateGroceryList();
            } else {
                alert('Ошибка при удалении рецепта');
            }
        } catch (error) {
            console.error('Ошибка удаления рецепта:', error);
            alert('Ошибка при удалении рецепта');
        }
    }

    // Обработчики событий
    searchInput.addEventListener('input', filterAndSortRecipes);
    sortSelect.addEventListener('change', filterAndSortRecipes);
    
    clearFilters.addEventListener('click', () => {
        searchInput.value = '';
        sortSelect.value = 'title';
        filterAndSortRecipes();
    });

    clearGroceryList.addEventListener('click', () => {
        selectedRecipes.clear();
        updateSelectedRecipesDisplay();
        updateGroceryList();
        loadSavedRecipes();
    });

    // Загружаем рецепты при загрузке страницы
    loadSavedRecipes();
});