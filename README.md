# 📓 Mood Diary — Телеграм-бот для отслеживания настроения

> Простой и приватный способ фиксировать своё эмоциональное состояние каждый день.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)

---

## 📋 О проекте

**Mood Diary** — это телеграм-бот, который помогает пользователю раз в день оценивать своё настроение по шкале от **0 до 10**. Все данные сохраняются в базе, что позволяет отслеживать динамику эмоционального состояния, строить графики и анализировать паттерны.

### ✨ Возможности
- 🎯 Оценка настроения одним нажатием (шкала 0–10)
- 📅 Напоминание раз в день (настраиваемое время)
- 📊 Просмотр истории и статистики за неделю/месяц

---

## 🚀 Быстрый старт

### Требования
- Python 3.12+
- PostgreSQL 14+
- Docker и Docker Compose *(опционально, но рекомендуется)*
- Токен бота от [@BotFather](https://t.me/BotFather)

### 🐳 Запуск через Docker Compose (рекомендуется)

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ignavan39/mood_diary.git
cd mood_diary
```

2. Создайте файл окружения `.env` в корне проекта:
```env
# Telegram
TG_BOT__TOKEN=your_telegram_bot_token_here

# Database
PG__USER=
PG__PASSWORD=
PG__HOST=
PG__NAME=
PG__PORT=

# App
TIMEZONE=Europe/Moscow
REMINDER_TIME=20:00
```

3. Запустите сервисы:
```bash
docker compose up -d
```

4. Примените миграции:
```bash
docker compose exec app alembic upgrade head
```

5. Запустите бота и напишите ему в Telegram `/start`

### 💻 Локальный запуск (без Docker)

1. Установите зависимости (рекомендуется использовать `uv`):
```bash
# Если установлен uv
uv sync

# Или через pip
pip install -r <(uv export)
```

2. Создайте и настройте `.env` (см. пример выше).

3. Примените миграции:
```bash
alembic upgrade head
```

4. Запустите бота:
```bash
python -m src.main
```

---

## ⚙️ Конфигурация

Все настройки задаются через переменные окружения или файл `.env`.


## 🗂️ Структура проекта

```
mood_diary/
├── migration/               # Alembic-миграции
│   ├── versions/            # Файлы миграций
│   └── env.py               # Конфигурация окружения Alembic
├── alembic.ini              # Настройки Alembic
├── src/
│   ├── __init__.py
│   ├── main.py              # Точка входа, запуск бота
│   ├── database.py          # Настройки SQLAlchemy, сессии
│   ├── configs/             # Конфигурация через Pydantic Settings
│   └── models/              # SQLAlchemy-модели (User, MoodEntry)
├── pyproject.toml           # Зависимости и метаданные проекта
├── uv.lock                  # Lock-файл зависимостей (uv)
├── docker-compose.yml       # Оркестрация сервисов
├── Dockerfile               # Образ приложения
└── .env.example             # Шаблон переменных окружения
```

---

## 🛠️ Разработка

### Миграции базы данных (Alembic)

```bash
# Создать новую миграцию после изменения моделей
alembic revision --autogenerate -m "description"

# Применить миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1

# Просмотреть историю миграций
alembic history
```

## 📦 Технологии

- **Backend**: Python 3.12+, asyncio
- **Telegram Bot API**: pyTelegramBotAPI (`telebot`)
- **ORM**: SQLAlchemy 2.0 (async) + asyncpg
- **Валидация**: Pydantic v2 + pydantic-settings
- **Миграции**: Alembic
- **Контейнеризация**: Docker, Docker Compose
- **Управление зависимостями**: uv *(или pip)*

---


## 📄 Лицензия

Распространяется под лицензией MIT. Подробности — в файле [LICENSE](LICENSE).

---


> ⚠️ **Важно**: Этот бот не является медицинским инструментом. Если вы испытываете стойкое ухудшение настроения, тревогу или депрессивные состояния — обратитесь к квалифицированному специалисту.

---

*Сделано с заботой о ментальном здоровье 🌱*