# 🥗 Recipe & Grocery Planner - Планировщик рецептов и покупок

REST API для управления рецептами, ингредиентами и списками покупок. Пользователь может сохранять рецепты, создавать из них списки покупок.

## 🛠️ Используемые технологии

- **Бэкенд**: FastAPI
- **ORM**: SQLAlchemy 2.0 + Alembic
- **Валидация**: Pydantic
- **СУБД**: PostgreSQL
- **Контейнеризация**: Docker + Docker Compose + Poetry
- **Тестирование**: Pytest
- **Фронтенд**: Jinja + HTML/CSS/JS (Free Template Simple House)

## 🚧 В разработке:

- 📦 API для работы со списками покупок

- 🧑 Работа с профилем пользователя

- 🔁 Связи:
    
  `User ↔ ShoppingLists` (один ко многим)  
  `ShoppingLists ↔ Products` (многие ко многим)  

## 📡 Эндпоинты

### 🔸 Auth
- `POST /api/v1/auth/login` — Аутентификация пользователя.
- `POST /api/v1/auth/logout` — Выход из системы.
- `POST /api/v1/auth/register` — Регистрация нового пользователя.
- `POST /api/v1/auth/request-verify-token` — Запрос токена верификации.
- `POST /api/v1/auth/verify` — Подтверждение email.
- `POST /api/v1/auth/forgot-password` — Запрос сброса пароля.
- `POST /api/v1/auth/reset-password` — Сброс пароля.

### 🔸 Users
- `GET /api/v1/users/me` — Получение текущего пользователя.
- `PATCH /api/v1/users/me` — Обновление профиля.
- `GET /api/v1/users/{id}` — Получение пользователя по ID.
- `PATCH /api/v1/users/{id}` — Обновление пользователя.
- `DELETE /api/v1/users/{id}` — Удаление пользователя.

### 🔸 Messages
- `GET /api/v1/messages` — Получение публичных сообщений.
- `GET /api/v1/messages/secrets` — Получение приватных сообщений.

### 🔸 Products
- `GET /api/v1/products/` — Получение списка продуктов.
- `POST /api/v1/products/` — Создание продукта.
- `GET /api/v1/products/{product_id}/` — Получение продукта по ID.
- `PUT /api/v1/products/{product_id}/` — Полное обновление продукта.
- `DELETE /api/v1/products/{product_id}/` — Удаление продукта.

### 🔸 Recipes
- `GET /api/v1/recipes/` — Получение списка рецептов.
- `POST /api/v1/recipes/` — Создание рецепта.
- `GET /api/v1/recipes/{recipe_id}/` — Получение рецепта по ID.
- `PUT /api/v1/recipes/{recipe_id}/` — Полное обновление рецепта.
- `PATCH /api/v1/recipes/{recipe_id}/` — Частичное обновление рецепта
- `DELETE /api/v1/recipes/{recipe_id}/` — Удаление рецепта.
- `POST /api/v1/recipes/upload/recipe-image` — Загрузка изображения рецепта.

### 🔸 Views
- `GET /Home` — Главная страница.
- `GET /login` — Страница входа.
- `GET /register` — Страница регистрации.
- `GET /profile` — Страница профиля.
- `GET /profile_info` — Информация о пользователе и его рецептах.
- `GET /recipes` — Страница создания рецепта.

## 🐳 Установка и запуск с Docker:

### 🔹 1. Клонируйте репозиторий и перейдите в директорию проекта:
```
git clone https://github.com/MaxBakshaev/FastAPI-Recipe-And-Grocery-Planner.git
```
```
cd FastAPI-Recipe-And-Grocery-Planner
```

### 🔹 2. Создайте файлы окружения:

Для Linux или macOS:
```
mkdir -p app && touch app/.env app/.env.postgres
```
Для Windows:
```
type nul > app\.env
type nul > app\.env.postgres
```

### 🔹 3. Настройте файл `app/.env`:

3.1. Добавьте переменные окружения:
```
APP_CONFIG__DB__URL=postgresql+asyncpg://user:pwd@localhost:5432/DBname
APP_CONFIG__DB__ECHO=1
APP_CONFIG__ACCESS_TOKEN__RESET_PASSWORD_TOKEN_SECRET=
APP_CONFIG__ACCESS_TOKEN__VERIFICATION_TOKEN_SECRET=
```
3.2. ✏️ Замените в APP_CONFIG__DB__URL:

- `user` — имя пользователя БД
- `pwd` — пароль
- `DBname` — название БД

🔑 Сгенерируйте секретные ключи и добавьте в APP_CONFIG__ACCESS_TOKEN__RESET_PASSWORD_TOKEN_SECRET и APP_CONFIG__ACCESS_TOKEN__VERIFICATION_TOKEN_SECRET:

```
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 🔹 4. Настройте файл `app/.env.postgres`:

4.1. Добавьте переменные окружения с вашими данными:
```
POSTGRES_USER=ваше_имя_пользователя
POSTGRES_PASSWORD=ваш_пароль
POSTGRES_DB=ваше_название_БД
```

### 🔹 5. Запуск контейнеров:

Убедитесь, что Docker Desktop запущен. Затем создайте и запустите докер контейнер:
```
make bup
```
Остановка контейнера:
```
make stop
```
- 📄 Дополнительные команды смотрите в `Makefile`.

### 🔹 6. Откройте в браузере:

- 🏠 Приложение: http://127.0.0.1:8000/

- 📚 Swagger UI: http://127.0.0.1:8000/docs

- 📘 Redoc: http://127.0.0.1:8000/redoc

### 🔹 7. 🧪 Запуск тестов:
```
make test
```