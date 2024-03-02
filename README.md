# rlt_telegram_aggregator

Автор проекта - Константин Мельник.

## Tecnhologies

- Python 3.11
- aiogram
- MongoDB
- asyncio

Проект является telegram ботом, который по запросу в формате JSON обращается к MongoDB и изымает определённый датасет из коллекции, агрегирует его и возвращает обратно в том же формате. Объём данных определяется параметрами `dt_from` и `dt_upto` - временной интервал от и до соответственно в ISO формате. `group_type` отвечает за тип агрегации данных, например: month, day, hour. Пример JSON запроса:
```json
{
"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"
}
```

Что вам ответит бот:
```json
{"dataset": [5906586.0, 5515874.0, 5889803.0, 6092634.0], "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00", "2022-11-01T00:00:00", "2022-12-01T00:00:00"]}
```
[Бот](https://t.me/buterb_bot)

### Локальный запуск проекта:

```text
git clone git@github.com:abyxez/rlt_case.git
```

```text
cd rlt_case/
```

Создать и активировать виртуальное окружение:

```text
python3 -m venv venv
```
Linux/macOS: 
```text
source venv/bin/activate
```
Windows: 
```text
source venv/Scripts/activate
```

```text
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements:

```text
pip install -r requirements.txt
```

Запустить проект:

```text
python3 manage.py runserver
```


