function logout() {
    localStorage.removeItem("access_token");
    window.location.href = "/";
}

function updateMenu() {
    const isAuth = !!localStorage.getItem("access_token");

    // Показываем общие
    document.querySelector(".menu-home")?.classList.remove("hidden");

    if (isAuth) {
        document.querySelector(".menu-recipes")?.classList.remove("hidden");
        document.querySelector(".menu-profile")?.classList.remove("hidden");
        document.querySelector(".menu-logout")?.classList.remove("hidden");
    } else {
        document.querySelector(".menu-login")?.classList.remove("hidden");
        document.querySelector(".menu-register")?.classList.remove("hidden");
    }
}

document.addEventListener("DOMContentLoaded", updateMenu);

async function apilogout() {
    const token = localStorage.getItem("access_token");

    if (!token) {
    window.location.href = "/";
    return;
    }

    try {
    const res = await fetch("/api/v1/auth/logout", {
        method: "POST",
        headers: {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        },
    });

    if (res.ok) {
        localStorage.removeItem("access_token");
        window.location.href = "/";
    } else {
        console.error("Ошибка при выходе:", await res.text());
        alert("Ошибка при выходе.");
    }
    } catch (error) {
    console.error("Ошибка сети при выходе:", error);
    alert("Ошибка сети. Попробуйте позже.");
    }
}