document.addEventListener('DOMContentLoaded', () => {
    const gallery = document.getElementById('recipe-gallery');

    fetch('/api/v1/recipes/')
        .then(response => response.json())
        .then(data => {
            if (!data.length) {
                gallery.innerHTML = '<p class="text-center">Рецепты не найдены</p>';
                return;
            }

            data.forEach(recipe => {
                const article = document.createElement('article');
                article.className = 'col-lg-3 col-md-4 col-sm-6 col-12 tm-gallery-item';

                article.innerHTML = `
                    <figure>
                        <img src="${recipe.image_url}" alt="${recipe.title}" class="img-fluid tm-gallery-img" />
                        <figcaption>
                            <h4 class="tm-gallery-title">${recipe.title}</h4>
                            <p class="tm-gallery-description">${recipe.description}</p>
                            <p class="tm-gallery-price">${recipe.calories} ккал / ${recipe.weight} г.</p>
                        </figcaption>
                    </figure>
                `;

                gallery.appendChild(article);
            });
        })
        .catch(err => {
            console.error('Ошибка загрузки рецептов:', err);
            gallery.innerHTML = '<p class="text-center">Не удалось загрузить рецепты</p>';
        });
});