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

// Отобразить рецепты
const listDiv = document.getElementById("recipes-list");
if (user.recipes.length === 0) {
    listDiv.innerHTML = "<p>У вас пока нет рецептов.</p>";
} else {
    let html = "<ul>";
    user.recipes.forEach(recipe => {
    html += `<li>
        <strong>${recipe.title}</strong><br/>
        ${recipe.body}<br/>
        Калории: ${recipe.total_calories}, Граммы: ${recipe.total_quantity}
    </li>`;
    });
    html += "</ul>";
    listDiv.innerHTML = html;
}
}

loadProfile();