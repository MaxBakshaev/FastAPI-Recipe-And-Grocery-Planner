document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
  
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const messageEl = document.getElementById("message");
  
    // Очищаем предыдущие сообщения
    messageEl.textContent = "";
    messageEl.className = "text-center";
  
    try {
      const res = await fetch("/api/v1/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });
  
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem("access_token", data.access_token);
        
        // Показываем сообщение об успехе
        messageEl.textContent = "Вход выполнен успешно!";
        messageEl.style.color = "green";
        messageEl.style.fontWeight = "500";
        
        // Задержка перед перенаправлением
        setTimeout(() => {
          window.location.href = "/profile";
        }, 1000);
        
      } else {
        const errorData = await res.json();
        
        // Преобразуем код ошибки в понятное сообщение
        let errorMessage = "Ошибка входа";
        
        if (errorData.detail === "LOGIN_BAD_CREDENTIALS") {
          errorMessage = "Неверный email или пароль";
        } else if (errorData.detail === "LOGIN_USER_NOT_VERIFIED") {
          errorMessage = "Аккаунт не подтвержден. Проверьте вашу почту";
        } else if (typeof errorData.detail === "string") {
          // Если detail уже строка, используем ее
          errorMessage = errorData.detail;
        }
        
        // Красиво отображаем ошибку
        messageEl.textContent = errorMessage;
        messageEl.style.color = "#dc3545";
        messageEl.style.fontWeight = "500";
        messageEl.style.padding = "10px 0";
      }
    } catch (error) {
      console.error("Ошибка:", error);
      messageEl.textContent = "Ошибка соединения. Попробуйте еще раз";
      messageEl.style.color = "#dc3545";
      messageEl.style.fontWeight = "500";
      messageEl.style.padding = "10px 0";
    }
  });