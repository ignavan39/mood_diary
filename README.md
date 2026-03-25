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

**Mood Diary** — мультиплатформенный бот (Telegram + VK), который помогает пользователю раз в день оценивать своё настроение по шкале от **0 до 10**. Все данные сохраняются в базе, что позволяет отслеживать динамику эмоционального состояния, строить графики и анализировать паттерны.

### ✨ Возможности
- 🎯 Оценка настроения одним нажатием (шкала 0–10)
- 📊 Просмотр статистики за неделю / месяц / год
- 📈 Генерация инфографики с графиком настроения (`/export`)
- 💬 Поддержка Telegram и VK — одна база, разные платформы
- 🧱 Clean Architecture: Domain → Application → Infrastructure → Presentation

---

## 🔍 Поиск по проекту

Этот репозиторий может быть полезен если ты ищешь:

- пример бота на aiogram 3.x
- VK бот без сторонних фреймворков — чистый long polling через `vk_api`
- шаблон Clean Architecture на Python
- мультиплатформенный бот с общей бизнес-логикой
- интеграция Prometheus + Grafana для мониторинга
- асинхронный PostgreSQL с SQLAlchemy 2.0

---

## 🚀 Быстрый старт

### Требования
- Python 3.12+
- PostgreSQL 14+
- Docker и Docker Compose *(рекомендуется)*
- Токен бота от [@BotFather](https://t.me/BotFather)
- Токен сообщества VK *(опционально)*

### 🐳 Запуск через Docker Compose

```bash
git clone https://github.com/ignavan39/mood_diary.git
cd mood_diary
cp .env.example .env  # заполни переменные
docker compose up -d
```

Миграции применятся автоматически при первом запуске.

### 💻 Локальный запуск

```bash
uv sync
alembic upgrade head
python -m src.main
```

---

## ⚙️ Конфигурация

| Переменная | Описание | Обязательно |
|---|---|---|
| `TG_BOT_TOKEN` | Токен Telegram бота | ✅ |
| `TG_BOT_ENABLED` | Включить Telegram бота | ✅ |
| `VK_BOT_TOKEN` | Токен сообщества VK | ❌ |
| `VK_BOT_GROUP_ID` | ID группы VK | ❌ |
| `VK_BOT_ENABLED` | Включить VK бота | ❌ |
| `PG__USER` | Пользователь PostgreSQL | ✅ |
| `PG__PASSWORD` | Пароль PostgreSQL | ✅ |
| `PG__HOST` | Хост PostgreSQL | ✅ |
| `PG__NAME` | Имя базы данных | ✅ |
| `PG__PORT` | Порт PostgreSQL | ✅ |
| `REDIS__HOST` | Хост Redis | ✅ |
| `REDIS__PASSWORD` | Пароль Redis | ✅ |

---

## 🗂️ Структура проекта

```
src/
├── main.py
├── domain/                          # Бизнес-сущности, интерфейсы
│   ├── entities/                    # User, Diary, StatsPeriod
│   ├── repositories/                # Интерфейсы репозиториев
│   ├── dtos/                        # SaveDiaryDTO, UpdateDiaryDTO
│   └── exceptions/
├── application/                     # Бизнес-логика
│   ├── use_cases/                   # RegisterUser, RecordMood, GetUserStats,
│   │                                # UpdateMood, GenerateMoodInfographic
│   ├── services/                    # ChartGeneratorInterface
│   └── dtos/
├── infrastructure/                  # Реализации
│   ├── database/                    # SQLAlchemy модели и репозитории
│   ├── charts/                      # MoodChartGenerator (matplotlib)
│   ├── cache/redis/                 # RedisManager
│   ├── concurrency/                 # ExecutorPool
│   ├── configs/                     # Settings (pydantic-settings)
│   ├── ioc/container/               # DI контейнеры
│   ├── lifecycle/                   # SignalHandler
│   └── metrics/                     # Prometheus, Health check
└── presentation/
    ├── common/                      # BaseBot, BotRunner, Messages
    ├── telegram/                    # Telegram бот (aiogram 3.x)
    │   ├── bot.py
    │   ├── middlewares/             # MetricsMiddleware, ErrorHandlerMiddleware
    │   └── endpoints/
    │       ├── mood/                # /mood, /export
    │       ├── user/                # /start, /profile
    │       └── help/                # /help
    └── vk/                          # VK бот (vk_api, чистый long polling)
        ├── bot.py
        ├── polling.py               # VkLongPolling — поток + адаптер событий
        ├── sdk/
        │   ├── types.py             # VkMessage, VkUser, VkEvent (frozen dataclasses)
        │   └── keyboards.py        # VkKeyboard builder
        ├── keyboards/               # Готовые клавиатуры проекта
        │   ├── main.py
        │   └── mood_select.py
        └── handlers/                # Хендлеры — аналог Telegram controllers
            ├── base.py              # VkHandler (ABC)
            ├── router.py            # VkRouter — цепочка хендлеров
            ├── user/
            │   ├── register.py
            │   └── fallback.py
            ├── mood/
            │   ├── mood.py          # MoodMenuHandler, RecordMoodHandler, UpdateMoodHandler
            │   ├── stats.py         # StatsMenuHandler, StatsHandler
            │   └── export.py        # ExportHandler
            └── help/
                └── help.py
```

---

## 🔁 Поток данных

```
┌─────────────────────────────────────────────────┐
│ Presentation (Telegram handlers / VK handlers)  │
│ → зависит от Application                        │
└────────────────────┬────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Application (Use Cases, DTOs)                   │
│ → зависит от Domain                             │
└────────────────────┬────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│ Domain (Entities, Repository Interfaces)        │
│ → НЕ зависит ни от чего                         │
└─────────────────────────────────────────────────┘
                     ↑
┌─────────────────────────────────────────────────┐
│ Infrastructure (SQLAlchemy, matplotlib, Redis)  │
│ → реализует Domain интерфейсы                   │
└─────────────────────────────────────────────────┘
```

Telegram и VK используют **одни и те же use cases** и **одну БД**. Пользователи разделяются по полю `platform`.

### VK архитектура (без сторонних фреймворков)

```
VkLongPolling (поток)
    ↓ адаптирует vk_api события в VkMessage
VkRouter
    ↓ перебирает цепочку VkHandler
VkHandler (ABC)
    ↓ вызывает use case → отправляет ответ через vk_api
```

---

## 📊 Мониторинг

| Сервис | URL | Доступ |
|--------|-----|--------|
| **Grafana** | http://localhost:3000 | admin / admin123 |
| **Prometheus** | http://localhost:9090 | — |
| **Bot Metrics** | http://localhost:8000/metrics | — |
| **Health** | http://localhost:8080/health | — |

---

## 📦 Технологии

| Компонент | Технология |
|-----------|-----------|
| **Backend** | Python 3.12+, asyncio |
| **Telegram** | aiogram 3.x |
| **VK** | vk_api (чистый long polling, без фреймворков) |
| **Charts** | matplotlib (Agg, потокобезопасный) |
| **ORM** | SQLAlchemy 2.0 + asyncpg |
| **Config** | Pydantic Settings |
| **Migrations** | Alembic |
| **DI** | dependency-injector |
| **Cache** | Redis |
| **Monitoring** | Prometheus + Grafana |
| **Packaging** | Docker, Compose, uv |

---

## Код стайл

```bash
mypy src/
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

MIT — подробности в файле [LICENSE](LICENSE).

---

> ⚠️ **Важно**: Этот бот не является медицинским инструментом. Если вы испытываете стойкое ухудшение настроения, тревогу или депрессивные состояния — обратитесь к квалифицированному специалисту.

---
*Сделано с заботой о ментальном здоровье 🌱*