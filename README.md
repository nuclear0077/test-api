# test-api
Для запуска данного API необходимо:

1  - git clone https://github.com/nuclear0077/test-api

2 - установить зависимости pip install -r requirements.txt 

3 - создать папку DB в каталоге и при первом запуске база данных будет создана

4 - Заполнить файл config.py указать путь до БД и указать уровень логирования.


Методы REST API - это набор обработчиков, с которыми можно взаимодействовать через сеть Интернет по протоколу HTTP.

Передача параметров при отправке HTTP-запросов производится в составе URL.

Результат выполнения запроса возвращается обработчиком в формате JSON.

## Получение информации о текущих пользователях в базе данных.


Метод	путь

GET	http://127.0.0.1:5000/test_task/api/user_data

Успешный ответ:

Список пользователей в формате jSON.

Пример ответа:

{
    "users": [
        {
            "email": "Alex@mail.ru",
            "first_name": "Alex",
            "id": 1,
            "last_name": "Smirnov"
        },
        {
            "email": "ivanov@mail.ru",
            "first_name": "Ivan",
            "id": 2,
            "last_name": "Ivanov"
        },
        {
            "email": "Anna@gmail.com",
            "first_name": "Anna",
            "id": 3,
            "last_name": "Petrova"
        }
    ]
}

## Получение информации пользователе в базе данных.

Метод путь

Получим информацию о пользователе с ID 2

GET	http://127.0.0.1:5000/test_task/api/user_data/2

Успешный ответ:

Информация о пользователе в формате jSON.

Пример ответа:

{
    "users": [
        {
            "email": "ivanov@mail.ru",
            "first_name": "Ivan",
            "id": "ivanov@mail.ru",
            "last_name": "Ivanov"
        }
    ]
}

если пользователя нет в бд получим следующий ответ

{
    "error": "Not found"
}

## Создание пользователя в базе данных.

Метод	путь

POST	http://127.0.0.1:5000/test_task/api/user_data

Пример запроса:

JSON в формате

{ 
   "last_name": "Smirnov",
   "first_name": "Victor",
   "email": "victor@gmail.com"
}

Успешный ответ:

{
    "result": "ok"
}

## Удаление пользователя из базы данных.

Метод	путь

Удалим пользователя с ID 2

DELETE	http://127.0.0.1:5000/test_task/api/user_data/2

Успешный ответ:

{'result': 'ok'}

если пользователя нет в бд получим следующий ответ

{
    "error": "Not found"
}

## Обновление информации о пользователе в базе данных.

Данный метод используется для обновления информации о  пользователе в базе данных.

Метод	путь

PUT	http://127.0.0.1:5000/test_task/api/user_data

Пример запроса:

JSON в формате

{  "id":1,
   "last_name": "Smirnov",
   "first_name": "Victor",
   "email": "victor@gmail.com"
}

Успешный ответ:

{
    "result": "ok"
}

если пользователя нет в бд получим следующий ответ

{
    "error": "Not found"
}

## Получение информации о истории заказов пользовтаеля.

Метод	путь

Получим информацию о пользователе с ID 1

GET	http://127.0.0.1:5000/test_task/api/order_data_user/1

Успешный ответ:

Информация о пользователе в формате jSON.

Пример ответа:

{
    "user_order_history": [
        {
            "book_name": "Изучаем Python",
            "book_quantity": 3,
            "email": "victor@gmail.com",
            "first_name": "Victor",
            "id_user": 1,
            "last_name": "Smirnov",
            "order_id": 1,
            "reg_date": "2022-07-02 19:39",
            "shop_address": "Тверская ул., 8, стр. 1, Москва, 125009",
            "shop_name": "Москва книжный магазин"
        }
    ]
}
если пользователя нет в бд получим следующий ответ

{
    "error": "Not found"
}

## Получение информации о заказе.

Метод	путь

Получим информацию о заказе с ID 3

GET	http://127.0.0.1:5000/test_task/api/order_data/3

Успешный ответ:

Информация о пользователе в формате jSON.

Пример ответа:

{
    "order_data": [
        {
            "book_name": "Детство",
            "book_quantity": 1,
            "email": "Anna@gmail.com",
            "first_name": "Anna",
            "id_user": 3,
            "last_name": "Petrova",
            "order_id": 3,
            "reg_date": "2022-01-03 18:40",
            "shop_address": "Тверская ул., 8, стр. 1, Москва, 125009",
            "shop_name": "Москва книжный магазин"
        }
    ]
}

если заказа в бд нет получим следующий ответ

{
    "error": "Not found"
}


## Создание нового заказа.

Метод	путь

POST	http://127.0.0.1:5000/test_task/api/order_data

Пример запроса:

JSON в формате

{   "user_id" : 2,
    "book_id":2,
    "shop_id":2,
    "book_quantity":4
}

Успешный ответ:

{
    "order_id": 5,
    "result": "ok"
}
