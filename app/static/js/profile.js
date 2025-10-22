async function loadProfile() {
    const token = localStorage.getItem("access_token");
    if (!token) {
        window.location.href = "/login";
        return;
    }

    const res = await fetch("/profile_info", {
        headers: {
            "Authorization": "Bearer " + token
        }
    });

    if (!res.ok) {
        localStorage.removeItem("access_token");
        window.location.href = "/login";
        return;
    }

    const user = await res.json();

    // Отобразить информацию о пользователе
    document.getElementById("profile-info").innerHTML = `
        <p><strong>Почта:</strong> ${user.email}</p>
        <p><strong>Никнейм:</strong> ${user.username}</p>
        <p><strong>ID:</strong> ${user.id}</p>
    `;

    // Отобразить рецепты с картинками
    const listDiv = document.getElementById("recipes-list");
    if (user.recipes.length === 0) {
        listDiv.innerHTML = "<p>У вас пока нет рецептов.</p>";
    } else {
        let html = '<div class="profile-recipes-grid">';
        user.recipes.forEach(recipe => {
            const imageUrl = recipe.image_url || '/static/img/products.jpg';
            
            html += `
                <div class="profile-recipe-card">
                    <div class="profile-recipe-image">
                        <img src="${imageUrl}" alt="${recipe.title}" 
                             onerror="this.src='/static/img/products.jpg'" />
                    </div>
                    <div class="profile-recipe-info">
                        <h5><strong>${recipe.title}</strong></h5>
                        <p class="recipe-body">${recipe.body}</p>
                        <p class="recipe-meta">${recipe.total_calories} ккал / ${recipe.total_quantity} г.</p>
                    </div>
                </div>
            `;
        });
        html += "</div>";
        listDiv.innerHTML = html;
    }
}

loadProfile();