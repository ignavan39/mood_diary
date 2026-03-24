# 📓 Mood Diary — Бот для отслеживания настроения

> Простой и приватный способ фиксировать своё эмоциональное состояние каждый день.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20Architecture-orange)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
[![Stars](https://img.shields.io/github/stars/ignavan39/mood_diary?style=flat)](https://github.com/ignavan39/mood_diary/stargazers)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

---

![](./.github/assets/social-preview.png)

## 📋 Оглавление
- [О проекте](#-о-проекте)
- [Поиск по проекту](#-поиск-по-проекту)
- [Быстрый старт](#-быстрый-старт)
- [Конфигурация](#️-конфигурация)
- [Структура проекта](#️-структура-проекта)
- [Поток данных](#-поток-данных)
- [Мониторинг](#-мониторинг)
- [Технологии](#-технологии)

---

## 📋 О проекте

**Mood Diary** — это мультиплатформенный бот (Telegram + VK), который помогает пользователю раз в день оценивать своё настроение по шкале от **0 до 10**. Все данные сохраняются в базе, что позволяет отслеживать динамику эмоционального состояния, строить графики и анализировать паттерны.

### ✨ Возможности
- 🎯 Оценка настроения одним нажатием (шкала 0–10)
- 📊 Просмотр истории и статистики за неделю/месяц/год
- 📈 Генерация инфографики с графиком настроения (`/export`)
- 💬 Поддержка Telegram и VK (одна база, разные платформы)
- 🧱 Чистая архитектура: Domain → Application → Infrastructure → Presentation

---

## 🔍 Поиск по проекту

Этот репозиторий может быть полезен если ты ищешь:

- пример бота на aiogram 3.x и vkbottle 4.x
- шаблон Clean Architecture на Python
- мультиплатформенный бот (Telegram + VK) с общей бизнес-логикой
- интеграция Prometheus + Grafana для мониторинга
- асинхронный PostgreSQL с SQLAlchemy 2.0
- self-hosted решение для ментального здоровья

---

## 🚀 Быстрый старт

### Требования
- Python 3.12+
- PostgreSQL 14+
- Docker и Docker Compose *(опционально, но рекомендуется)*
- Токен бота от [@BotFather](https://t.me/BotFather)
- Токен сообщества VK *(опционально)*

### 🐳 Запуск через Docker Compose (рекомендуется)

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ignavan39/mood_diary.git
cd mood_diary
```

2. Создайте файл окружения `.env` в корне проекта:
```env
# Telegram
TG_BOT_TOKEN=your_telegram_bot_token_here

# VK (опционально — если не нужен, просто не добавляй)
VK_BOT_TOKEN=vk1.a.xxxxxxxxxxxxxxxx
VK_BOT_GROUP_ID=123456789

# Database
PG__USER=
PG__PASSWORD=
PG__HOST=postgres
PG__NAME=mood_diary
PG__PORT=5432

# Redis
REDIS__HOST=redis
REDIS__PORT=6379
REDIS__PASSWORD=password

# Monitoring
GRAFANA_USER=admin
GRAFANA_PASSWORD=admin123
```

3. Запустите сервисы:
```bash
docker compose up -d
```

Миграции применятся автоматически через образ `migrate` при первом запуске.

4. Напишите боту `/start` в Telegram или VK.

### 💻 Локальный запуск (без Docker)

1. Установите зависимости:
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

| Переменная | Описание | Обязательно |
|---|---|---|
| `TG_BOT_TOKEN` | Токен Telegram бота | ❌ |
| `VK_BOT_TOKEN` | Токен сообщества VK | ❌ |
| `VK_BOT_GROUP_ID` | ID группы VK (число) | ❌ |
| `PG__USER` | Пользователь PostgreSQL | ✅ |
| `PG__PASSWORD` | Пароль PostgreSQL | ✅ |
| `PG__HOST` | Хост PostgreSQL | ✅ |
| `PG__NAME` | Имя базы данных | ✅ |
| `PG__PORT` | Порт PostgreSQL | ✅ |
| `REDIS__HOST` | Хост Redis | ✅ |
| `REDIS__PASSWORD` | Пароль Redis | ✅ |
| `GRAFANA_USER` | Пользователь Grafana | ❌ |
| `GRAFANA_PASSWORD` | Пароль Grafana | ❌ |

---

## 🗂️ Структура проекта

```
mood-diary-bot/
├── README.md
├── src/
│   ├── main.py                        # Точка входа, запуск всех ботов
│   ├── domain/                        # Domain слой — бизнес-сущности
│   │   ├── dtos/                      # SaveDiaryDTO, SaveUserDTO, UpdateDiaryDTO
│   │   ├── entities/                  # User, Diary, StatsPeriod
│   │   ├── repositories/              # Интерфейсы DiaryRepository, UserRepository
│   │   └── exceptions/                # Domain исключения
│   ├── application/                   # Application слой — бизнес-логика
│   │   ├── use_cases/                 # RegisterUser, RecordMood, GetUserStats,
│   │   │                              # UpdateMood, GenerateMoodInfographic
│   │   ├── services/                  # ChartGeneratorInterface
│   │   └── dtos/                      # DTO запросов/ответов use cases
│   ├── infrastructure/                # Infrastructure слой
│   │   ├── database/                  # SQLAlchemy модели и репозитории
│   │   │   ├── models/                # UserModel, DiaryModel
│   │   │   └── repositories/          # SQLAlchemy реализации репозиториев
│   │   ├── charts/                    # MoodChartGenerator (matplotlib)
│   │   ├── cache/redis/               # RedisManager
│   │   ├── concurrency/               # ExecutorPool для CPU-задач
│   │   ├── configs/                   # Settings (pydantic-settings)
│   │   ├── ioc/container/             # DI контейнеры (dependency-injector)
│   │   ├── lifecycle/                 # SignalHandler
│   │   └── metrics/                   # Prometheus метрики, Health check
│   └── presentation/                  # Presentation слой
│       ├── common/                    # BaseBot, BotRunner, Messages
│       ├── telegram/                  # Telegram бот (aiogram 3.x)
│       │   ├── bot.py
│       │   ├── commands/
│       │   └── endpoints/
│       │       ├── mood/              # /mood, /export
│       │       ├── user/              # /start, /profile
│       │       └── help/              # /help
│       └── vk/                        # VK бот (vkbottle 4.x)
│           ├── bot.py
│           └── keyboards.py
├── monitoring/
│   └── grafana/
│       ├── prometheus.yml
│       └── provisioning/
│           ├── dashboards/
│           └── datasources/
├── pyproject.toml
├── uv.lock
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

---

## 🔁 Поток данных

```
┌─────────────────────────────────────────────┐
│ Presentation (Telegram / VK handlers)       |
|  (aiogram, vkbottle)                        │
│ → зависит от Application                    │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│ Application (Use Cases, DTOs)               │
│ → зависит от Domain                         │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│ Domain (Entities, Repository Interfaces)    │
│ → НЕ зависит ни от чего                     │
└─────────────────────────────────────────────┘
                  ↑
┌─────────────────────────────────────────────┐
│ Infrastructure (SQLAlchemy, redis,          │
│ matplotlib)                                 │
│ → реализует Domain интерфейсы               │
└─────────────────────────────────────────────┘
```

Оба бота (Telegram и VK) используют **одни и те же use cases** и **одну базу данных**. Пользователи разделяются по полю `platform` (`telegram` / `vk`).

---

## 📊 Мониторинг

Папка `monitoring/` содержит конфигурацию Prometheus + Grafana.

### 🔗 Доступ к интерфейсам

| Сервис | URL | Логин/Пароль |
|--------|-----|--------------|
| **Grafana** | http://localhost:3000 | admin / admin123 |
| **Prometheus** | http://localhost:9090 | — |
| **Bot Metrics** | http://localhost:8000/metrics | — |
| **Health** | http://localhost:8080/health | — |

### 📈 Метрики

| Метрика | Тип | Описание |
|---------|-----|----------|
| `bot_messages_total` | Counter | Всего обработано сообщений |
| `bot_request_duration_seconds` | Histogram | Время обработки запроса |
| `bot_active_users` | Gauge | Активных пользователей за час |
| `bot_users_registered_total` | Counter | Всего зарегистрировано пользователей |

---

## 📦 Технологии

| Компонент | Технология | Зачем |
|-----------|-----------|--------|
| **Backend** | Python 3.12+, asyncio | Асинхронность, высокая производительность |
| **Telegram** | aiogram 3.x | Современный async-фреймворк для Telegram |
| **VK** | vkbottle 4.x | Long polling бот для VK сообществ |
| **Charts** | matplotlib (Agg) | Генерация инфографики настроения |
| **ORM** | SQLAlchemy 2.0 + asyncpg | Типизированные async-запросы к PostgreSQL |
| **Config** | Pydantic Settings | Валидация настроек, типизация, .env-поддержка |
| **Migrations** | Alembic | Управление схемой БД |
| **DI** | dependency-injector | IoC контейнер, разделение слоёв |
| **Cache** | Redis (redis) | Состояния сессий |
| **Monitoring** | Prometheus + Grafana | Метрики и дашборды |
| **Containerization** | Docker, Compose | Воспроизводимая среда, лёгкий деплой |
| **Package Manager** | uv | Быстрая установка зависимостей |

---

## Код стайл

```bash
# Проверка типов
mypy src/

# Линтинг и форматирование
ruff check src/ && ruff format src/
```

---

## ⭐ Понравился проект?

- Поставь звезду ⭐ — это лучшая поддержка!
- Расскажи другу 🗣️ — если считаешь полезным
- Предложи идею 💡 — через Issues или Discussions
- Исправь опечатку ✏️ — любой вклад важен

Спасибо что заглянул! 🙏

---

## 📄 Лицензия

Распространяется под лицензией MIT. Подробности — в файле [LICENSE](LICENSE).

---

> ⚠️ **Важно**: Этот бот не является медицинским инструментом. Если вы испытываете стойкое ухудшение настроения, тревогу или депрессивные состояния — обратитесь к квалифицированному специалисту.

---

*Сделано с заботой о ментальном здоровье 🌱*