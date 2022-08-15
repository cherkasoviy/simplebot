## Запуск локально

В терминале в каталоге с проектом выполнить

`pip install --no-cache-dir --upgrade -r /requirements.tx`

после этого можно запускаться командой

`uvicorn app.main:app --reload`

Открыв в браузере  http://127.0.0.1:8000 видим ответ от бота и это значит что все получилось


## API Endpoints and documentation
Пока `uvicorn` запущен:

http://127.0.0.1:8000/docs - Swagger UI (OpenAPI) интерактивная документация по эндпоинтам и методам

http://127.0.0.1:8000/redoc - альтернатива на основе ReDoc с возможностью скачивания


## База Данных

В качестве БД используется SQLite, исключительно для тестового задания, в реальной жизни файловую базу данных коненчо же использовать не стоит

База представляет из себя одну таблицу, со следующими полями:



    request_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    timestamp TEXT,
    user_id TEXT,
    direction TEXT, 
    text TEXT,
    data TEXT

`direction` - может принимтаь 2 значения REQUEST или ANSWER для запросов пользователя и ответов бота соответственно 

`text` - содержит текст пользователя\бота

`data` - содержит в сыром виде JSON со всеми полями

## Запуск в проде

В терминале в каталоге с проектом выполнить

`docker build -t botimage .`

и затем

`docker run -d --name botcontainer -p 80:80 botimage`

При необходимости смапить бота на другой порт поменять номер порта не только в команде выше но и в последней строке Dockerfile 