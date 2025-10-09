document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch("/api/v1/auth/login", {
      method: "POST",
      headers: {
          "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
          username: email,  // FastAPI Users использует "username" вместо "email"
          password: password,
      }),
  });

  if (res.ok) {
      const data = await res.json();
      localStorage.setItem("access_token", data.access_token);
      window.location.href = "/profile";
  } else {
      const error = await res.json();
      document.getElementById("message").textContent = error.detail || "Ошибка входа";
  }
});