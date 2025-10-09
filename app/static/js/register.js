document.getElementById("register-form").addEventListener("submit", async function (e) {
e.preventDefault();

const username = document.getElementById("username").value;
const email = document.getElementById("email").value;
const password = document.getElementById("password").value;

const messageEl = document.getElementById("register-message");
messageEl.style.color = "red";
messageEl.textContent = "";

try {
    const res = await fetch("/api/v1/auth/register", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, password, username })
    });

    const data = await res.json();

    if (res.ok) {
    messageEl.style.color = "green";
    messageEl.textContent = "Регистрация успешна! Перенаправление...";
    setTimeout(() => {
        window.location.href = "/login";
    }, 2000);
    } else {
    messageEl.textContent = data.detail || "Ошибка регистрации";
    }
} catch (err) {
    console.error("Ошибка запроса:", err);
    messageEl.textContent = "Ошибка сети. Попробуйте позже.";
}
});