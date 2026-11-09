# ci_cd_practice

Консольное Python-приложение: калькулятор двух чисел. Принимает два числа,
предлагает выбрать математическую операцию и выводит результат в виде строки,
например `2 + 2 = 4`.

## Структура проекта

```
ci_cd_practice/
├── app/
│   ├── __init__.py
│   ├── calculator.py   # операции, вычисление, форматирование результата
│   └── main.py         # консольный интерфейс (точка входа)
├── tests/
│   ├── __init__.py
│   └── test_calculator.py
├── .github/
│   └── workflows/
│       └── python-app.yml  # CI: тесты, деплой, versions.md
├── Procfile
├── requirements.txt
├── pytest.ini
└── README.md
```

## Требования

- Python 3.10+ (проверялось на 3.12)
- pytest (ставится из `requirements.txt`)

## Установка

```bash
cd ci_cd_practice

# создать и активировать виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate

# установить зависимости
pip install -r requirements.txt
```

## Запуск

Из корня проекта (там, где лежит эта папка `ci_cd_practice`):

```bash
python -m app.main
```

### Пример сессии

```
Калькулятор двух чисел
Введите первое число: 2
Введите второе число: 2

Доступные операции:
  + — Сложение
  - — Вычитание
  * — Умножение
  / — Деление
Выберите операцию: +
2 + 2 = 4

Посчитать ещё раз? (y/n): n
До свидания!
```

При делении на ноль приложение попросит ввести другое второе число.
При вводе не-числа запрос повторяется.

## Запуск тестов

Из корня проекта:

```bash
pytest
```

Подробный вывод по всем тестам:

```bash
pytest -v
```

## CI/CD

На каждый коммит в `main` запускается GitHub Actions (файл `.github/workflows/python-app.yml`):

| Джоба | Что делает |
|---|---|
| `test` | Устанавливает Python 3.12, ставит зависимости, запускает `pytest -v` |
| `deploy` | Пушит в Heroku (запускается **только** если `test` прошёл) |
| `update-versions` | Дописывает дату, хеш и сообщение коммита в `versions.md` |

## Деплой на Heroku

### Подготовка

1. Создать приложение на Heroku (один раз):

   ```bash
   heroku create <имя-приложения>
   ```

2. В настройках репозитория GitHub (Settings → Secrets and variables → Actions) добавить:
   | Имя | Значение |
   |---|---|
   | `HEROKU_API_KEY` | Ключ из Heroku → Account Settings → API Key |
   | `HEROKU_APP_NAME` | Имя приложения (например `my-calculator`) |

### Как работает деплой

Джоба `deploy` пушит коммит напрямую в Heroku Git-remote по HTTPS:

```
https://api:<API_KEY>@git.heroku.com/<APP>.git
```

### Важное примечание

Приложение — консольное (`input()`), а Heroku `web`-dyno не имеет stdin.
При запуске `web: python -m app.main` процесс сразу завершается с ошибкой EOF.

Чтобы протестировать приложение на Heroku:

```bash
heroku run python -m app.main
```

Это запустит приложение в отдельном one-off dyno с интерактивной консолью.
