# Science Fiction Movies API

## Структура проекта

```text
homework/
├── main.py
├── requirements.txt
├── README.md
├── run.bat
└── .gitignore
```

## Установка и запуск

### Windows

```powershell
cd homework
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### macOS / Linux

```bash
cd homework
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

После запуска сервер доступен по адресу <http://127.0.0.1:8000>.

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## Статус-коды и ошибки

| Ситуация                                  | Статус | Ответ                                              |
|-------------------------------------------|--------|----------------------------------------------------|
| Фильм найден                              | 200    | Объект фильма                                      |
| Новый фильм создан                        | 201    | Созданный фильм с `id`                             |
| Фильм с таким названием уже существует    | 400    | `{"detail": "Фильм с названием «...» уже существует"}` |
| Фильм с указанным `id` не найден          | 404    | `{"detail": "Фильм с id=... не найден"}`           |
| Данные не прошли проверку модели          | 422    | Стандартная ошибка валидации FastAPI               |

### Получить список фильмов

```http
GET /movies
```

Ответ `200`:

```json
[
  {
    "title": "Интерстеллар",
    "director": "Кристофер Нолан",
    "year": 2014,
    "id": 1
  },
  {
    "title": "Матрица",
    "director": "Лана и Лилли Вачовски",
    "year": 1999,
    "id": 2
  }
]
```

### Получить фильм по id

```http
GET /movies/1
```

Ответ `200` — объект фильма. Если фильма нет:

```http
GET /movies/100
```

Ответ `404`:

```json
{
  "detail": "Фильм с id=100 не найден"
}
```

### Добавить фильм

```http
POST /movies
Content-Type: application/json

{
  "title": "Чужой",
  "director": "Ридли Скотт",
  "year": 1979
}
```

Ответ `201`:

```json
{
  "title": "Чужой",
  "director": "Ридли Скотт",
  "year": 1979,
  "id": 4
}
```

Повторное добавление с тем же названием вернёт `400`:

```json
{
  "detail": "Фильм с названием «Чужой» уже существует"
}
```

Если отправить `year: 1899` или `year: 2031`, FastAPI вернёт `422` с описанием
ошибки валидации. Например, для слишком короткого названия:

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "title"],
      "msg": "String should have at least 2 characters",
      "input": "Я",
      "ctx": {"min_length": 2}
    }
  ]
}
```

## Проверка через Swagger

1. Запустите сервер и откройте <http://127.0.0.1:8000/docs>.
2. `GET /movies` → **Try it out** → **Execute**: должен вернуться список из трёх фильмов.
3. `GET /movies/1` → **Execute**: должен вернуться один фильм.
4. `GET /movies/100` → **Execute**: должен вернуться статус `404`.
5. `POST /movies` с новым названием → **Execute**: должен вернуться статус `201`.
6. Повторите тот же запрос → должен вернуться статус `400`.
7. Отправьте `year` меньше 1900 или больше 2030 → должен вернуться статус `422`.
