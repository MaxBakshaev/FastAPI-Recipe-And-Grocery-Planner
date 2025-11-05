document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Planner loaded');
    loadSavedRecipes();
});

let selectedRecipes = new Set();
let productsCache = {};

async function loadSavedRecipes() {
    const gallery = document.getElementById('saved-recipes-gallery');
    
    if (!gallery) {
        console.error('❌ Gallery element not found');
        return;
    }

    const token = localStorage.getItem('access_token');
    if (!token) {
        gallery.innerHTML = '<p class="text-center">Пожалуйста, войдите в систему</p>';
        return;
    }

    try {
        gallery.innerHTML = '<p class="text-center">🔄 Загрузка рецептов...</p>';
        
        await loadProducts();
        
        const response = await fetch('/api/v1/saved-recipes/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error(`Ошибка загрузки: ${response.status}`);
        }

        const recipes = await response.json();
        renderRecipes(recipes);
        
    } catch (error) {
        console.error('❌ Error:', error);
        gallery.innerHTML = `
            <div class="text-center" style="padding: 50px;">
                <h4>Ошибка загрузки</h4>
                <p style="color: red;">${error.message}</p>
            </div>
        `;
    }
}

async function loadProducts() {
    try {
        const response = await fetch('/api/v1/products/');
        if (response.ok) {
            const products = await response.json();
            productsCache = {};
            products.forEach(product => {
                productsCache[product.id] = product.name;
            });
        }
    } catch (error) {
        console.error('❌ Error loading products:', error);
    }
}

function getProductName(productId) {
    return productsCache[productId] || `Продукт #${productId}`;
}

function renderRecipes(recipes) {
    const gallery = document.getElementById('saved-recipes-gallery');
    
    if (!Array.isArray(recipes) || recipes.length === 0) {
        gallery.innerHTML = `
            <div class="text-center" style="padding: 50px;">
                <h4>У вас пока нет сохраненных рецептов</h4>
                <p>Перейдите на <a href="/">главную страницу</a> и сохраните несколько рецептов</p>
            </div>
        `;
        return;
    }

    gallery.innerHTML = '';

    recipes.forEach(recipe => {
        const article = document.createElement('article');
        article.className = 'recipe-article';
        
        const imageUrl = recipe.image_url || '/static/img/products.jpg';

        article.innerHTML = `
            <div class="recipe-container">
                <div class="recipe-image-wrapper">
                    <img src="${imageUrl}" alt="${recipe.title}" class="recipe-img" 
                         onerror="this.src='/static/img/products.jpg'" />
                    <p class="recipe-meta">${recipe.total_calories} ккал / ${recipe.total_quantity} г.</p>
                    <div class="recipe-actions">
                        <button class="action-btn add-to-grocery-btn" onclick="addToGroceryList(${recipe.id})">
                            📝 В список покупок
                        </button>
                        <button class="action-btn unsave-recipe-btn" onclick="unsaveRecipe(${recipe.id})">
                            ❌ Удалить
                        </button>
                    </div>
                </div>
                <div class="recipe-info">
                    <h4 class="recipe-title">${recipe.title}</h4>
                    <p class="recipe-description">${recipe.body}</p>
                    <div class="recipe-products">
                        <strong>Ингредиенты:</strong>
                        <ul>
                            ${(recipe.products || []).map(product => 
                                `<li>${product.quantity}г - ${getProductName(product.product_id)}</li>`
                            ).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `;

        gallery.appendChild(article);
    });
}

window.addToGroceryList = function(recipeId) {
    alert(`Рецепт #${recipeId} добавлен в список покупок\n(функциональность будет реализована позже)`);
};

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
            loadSavedRecipes();
        } else {
            alert('Ошибка при удалении рецепта');
        }
    } catch (error) {
        console.error('Ошибка удаления рецепта:', error);
        alert('Ошибка при удалении рецепта');
    }
}