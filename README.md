# 🥗 Recipe & Grocery Planner - Планировщик рецептов и покупок

REST API для управления рецептами, ингредиентами и списками покупок. Пользователь может сохранять рецепты, создавать из них списки покупок.


## ⚙️ Функциональность:

- 📐 Аннотации типов и валидация данных

- 🗃️ Асинхронные запросы к БД с SQLAlchemy 2.0  

- 🗝️ Аутентификация через `fastapi-users`

- 📦 API для работы с ингредиентами

- 📄 Alembic миграции

- 📝 Автоматическая OpenAPI-документация (`/docs`, `/redoc`)

- 🐳 Docker/Docker Compose

- 🧪 Юнит и интеграционные тесты


## 🚧 В разработке:

📦 API для рецептов и списков покупок

🧑 Работа с профилем пользователя

🔁 Связи:
  - `User ↔ Profile` (один к одному)  
  - `User ↔ Recipes`, `User ↔ ShoppingLists` (один ко многим)  
  - `Recipes ↔ Products`, `ShoppingLists ↔ Products` (многие ко многим)  

🖥️ Веб-интерфейс (UI)

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

3.3. Сгенерируйте командой ниже и добавьте секретные ключи в APP_CONFIG__ACCESS_TOKEN__RESET_PASSWORD_TOKEN_SECRET и APP_CONFIG__ACCESS_TOKEN__VERIFICATION_TOKEN_SECRET:

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
📄 Дополнительные команды смотрите в `Makefile`.

### 🔹 6. Откройте в браузере:

🏠 Приложение: http://127.0.0.1:8000/

📚 Swagger UI: http://127.0.0.1:8000/docs

📘 Redoc: http://127.0.0.1:8000/redoc

### 🔹 7. 🧪 Запуск тестов:
```
make test
```

## ⚙️ Установка и запуск без Docker:

### 🔹 1. Клонируйте репозиторий и перейдите в директорию проекта:
```
git clone https://github.com/MaxBakshaev/FastAPI-Recipe-And-Grocery-Planner.git
```
```
cd FastAPI-Recipe-And-Grocery-Planner
```

### 🔹 2. Создайте и активируйте виртуальное окружение:
```
python -m venv venv
```

Для Linux или macOS:
```
source venv/bin/activate
```
Для Windows:
```
venv\Scripts\activate
```

### 🔹 3. Установите зависимости:
```
pip install -r requirements.txt
```

### 🔹 4. Настройка окружения:

4.1. Создайте БД вручную в PostgreSQL.

4.2. Укажите свои данные в `app/.env.template`:

✏️ Замените в APP_CONFIG__DB__URL:

- `user` — имя пользователя БД
- `pwd` — пароль
- `DBname` — название БД

4.3. Сгенерируйте командой ниже и добавьте секретные ключи в APP_CONFIG__ACCESS_TOKEN__RESET_PASSWORD_TOKEN_SECRET и APP_CONFIG__ACCESS_TOKEN__VERIFICATION_TOKEN_SECRET:

```
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 🔹 5. Перейдите в каталог app и примените миграции:
```
cd app
```
```
alembic upgrade head
```
Вернитесь в корневую директорию:
```
cd ..
```

### 🔹 6. Запустите сервер:
```
python app/main.py
```

Для отключения сервера используйте команду:
```
Ctrl + C
```

### 🔹 7. Откройте в браузере:

- 🏠 Приложение: http://127.0.0.1:8000/

- 📚 Swagger UI: http://127.0.0.1:8000/docs

- 📘 Redoc: http://127.0.0.1:8000/redoc

### 🔹 8. 🧪 Запуск тестов:
```
pytest app/tests
```