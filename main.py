from datetime import datetime
from sqlalchemy.orm import sessionmaker
from alchemy import User, Order, Orderitem, Shop, Book, init_db
from sqlalchemy import create_engine, select, insert, delete, update, func
from flask import Flask, jsonify, make_response, request, abort
from config import db_name, path_db, log_level
import logging

# запустим логирование уровень логирования импортируем из конфига
logging.basicConfig(filename='test_task.log',
                    format='%(asctime)s - %(message)s',
                    level=log_level)

path_db = f'{path_db}/{db_name}'
logging.debug(f"Путь до базы данных {path_db}")
# если включена отладка, то включем вывод запросов
if log_level == 10:
    engine = create_engine(f'sqlite://{path_db}', echo=True)
else:
    engine = create_engine(f'sqlite://{path_db}')
session = sessionmaker(bind=engine)

app = Flask(__name__)


def main():
    # перед запуском API проверим, что существует БД, если ее нет, то создадим.
    init = init_db(path_db=path_db, engine=engine, log=logging)
    logging.debug(f"инициализация базы данных: {init}")


# Блок кода работы с таблицей USER
# реализуем метод получения списка всех пользователей
@app.route('/test_task/api/user_data', methods=['GET'])
def get_user_data():
    """Функция для получения списка пользователей
    :return список всех пользователей в формате JSON"""
    json_data = []
    # запишем информаци от кого пришел запрос
    logging.info(f"поступил запрос на получении информации о всех пользователях с IP:{request.remote_addr}")
    # вынесем запрос в переменную для записи отладочной информации
    m_query = select(User)
    logging.debug(f"запрос на получения списка пользователей \n{m_query}")
    # создадим сессию и сформируем запрос
    try:
        with session() as s:
            # в цикле заполняем наш json_data результатом запроса
            for row in s.execute(select(User)):
                json_data.append({'id': row[0].id, 'last_name': row[0].last_name, 'first_name': row[0].first_name,
                                  'email': row[0].email})
            logging.debug(f"результат запроса \n {json_data}")
    except Exception as ex:
        logging.error(f"в фукнции get_user_data произошло исключение \n {ex}")
        return jsonify({'error': ex})
    logging.info(f"result : ok")
    return jsonify({'users': json_data})


# реализуем метод получения пользователя по id
@app.route('/test_task/api/user_data/<int:user_id>', methods=['GET'])
def get_user_data_id(user_id):
    """Функция для получения пользователя по ID
    :param user_id: ID пользователя : int
    :return информация о пользователе в формате JSON"""
    json_data = []
    logging.info(f"поступил запрос на получении информации о пользователе с ID={user_id} с IP:{request.remote_addr}")
    # создадим сессию и сформируем запрос
    # вынесем запрос в переменную для записи отладочной информации
    m_query = select(User).where(User.id == user_id)
    logging.debug(f"запрос на получения списка пользователя по=ID {user_id} \n{m_query}")
    try:
        with session() as s:
            for row in s.execute(m_query):
                # в цикле заполняем наш json_data результатом  запроса
                json_data.append({'id': row[0].email, 'last_name': row[0].last_name, 'first_name': row[0].first_name,
                                  'email': row[0].email})
    except Exception as ex:
        logging.error(f"в фукнции get_user_data произошло исключение \n {ex}")
        return jsonify({'error': ex})
    logging.debug(f"результат запроса \n {json_data}")
    # проверяем что список пуст, если пуст значит пользователя нет и вернем 404
    if len(json_data) == 0:
        logging.info(f"пользователя с id {user_id} нет в таблице user")
        return abort(404)
    logging.info(f"result : ok")
    return jsonify({'users': json_data})


# реализуем фунцию добавления пользователя в БД
@app.route('/test_task/api/user_data', methods=['POST'])
def create_user():
    """Функция создания пользователя
    :return ответ в формате JSON"""
    # получим входящие данные в формате json
    request_data = request.json
    logging.info(f"поступил запрос на создание  пользователя с IP:{request.remote_addr}")
    logging.debug(f"JSON данные которые пришли {request_data}")
    # вынесем запрос в переменную для записи отладочной информации
    m_query = insert(User).values(last_name=request_data['last_name'], first_name=request_data['first_name'],
                                  email=request_data["email"])
    logging.debug(f"запрос на создание пользователя \n{m_query}")
    # установим сессию и добавим пользователя в бд
    try:
        with session() as s:
            s.execute(m_query)
            s.commit()

    except Exception as ex:
        logging.error(f"в фукнции get_user_data произошло исключение \n {ex}")
        return jsonify({'error': ex})
    logging.info(f"result : ok")
    return jsonify({'result': 'ok'})


# реализуем функцию удаления пользователя
# можно доработать и всю удалить информацию о заказ
@app.route('/test_task/api/user_data/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Функция для удаления пользователя из БД
    :param user_id: ID пользователя : int
    :return результат в формате JSON"""
    logging.info(f"поступил запрос на удаление пользователя с IP:{request.remote_addr}")
    # вынесем запрос в переменную для записи отладочной информации
    select_query = select(User).where(User.id == user_id)
    logging.debug(f"запрос на получения пользователя по id={user_id} в функции delete_user \n{select_query}")
    # откроем сессию, сформируем запрос на получении данных из таблицы user
    try:
        with session() as s:
            answer = s.execute(select_query).first()
            # проверим, что информация о пользователе была получена из бд
            if answer is None:
                logging.info(f"пользователя с id={user_id} нет в таблице user")
                return jsonify({'error': 'user not found'})
    except Exception as ex:
        logging.error(f"в фукнции delete_user при получении информации о пользователе произошло исключение \n {ex}")
        return jsonify({'error': ex})
    # вынесем запрос в переменную для записи отладочной информации
    m_query = delete(User).where(User.id == user_id)
    logging.debug(f"запрос на удаление пользователя id {user_id}\n{m_query}")
    # установим сессию и сформируем запрос на удаление пользователя из бд
    try:
        with session() as s:
            s.execute(m_query)
            s.commit()

    except Exception as ex:
        logging.error(f"в фукнции delete_user произошло исключение \n {ex}")
        return jsonify({'error': ex})
    logging.info(f"result : ok")
    return jsonify({'result': 'ok'})


# реализуем функцию обновления информации в БД в таблице user
@app.route('/test_task/api/user_data', methods=['PUT'])
def update_user():
    """Функция для обновления информации в БД user
    :return результат в формате JSON"""
    logging.info(f"поступил запрос на обновлении информации о пользователе с IP:{request.remote_addr}")
    # получим ответ
    request_data = request.json
    # создадим пустой список для записи результата проверки пользователя в БД
    json_data = []
    # проверим что передан id не None
    if request_data['id'] is None:
        return jsonify({'error': 'no is id'})
    # вынесем запрос в переменную для записи отладочной информации
    select_query = select(User).where(User.id == int(request_data['id']))
    logging.debug(f"запрос на получения пользователя по id={request_data['id']} в функции update_user \n{select_query}")
    # откроем сессию сформируем запрос на получение данных из таблицы user
    try:
        with session() as s:
            answer = s.execute(select_query).first()
            # проверим, что информация о пользователе была получена из бд
            if answer is None:
                logging.info(f"пользователя с id={request_data['id']} нет в таблице user")
                return jsonify({'error': 'user not found'})
            json_data.append(
                {'id': answer[0].email, 'last_name': answer[0].last_name, 'first_name': answer[0].first_name,
                 'email': answer[0].email})
    except Exception as ex:
        logging.error(f"в фукнции update_user при получении информации о пользователе произошло исключение \n {ex}")
        return jsonify({'error': ex})

    # вынесем запрос в переменную для записи отладочной информации
    upd_query = update(User).where(User.id == int(request_data['id'])).values(email=request_data['email'],
                                                                              first_name=request_data['first_name'],
                                                                              last_name=request_data['last_name']
                                                                              )
    logging.debug(f"запрос на обновление данных о пользователе id {request_data['id']}\n{upd_query}")
    # откроем сессию и сформируем запрос на обновление информации о пользователе в таблице user
    try:
        with session() as s:
            s.execute(upd_query)
            s.commit()

    except Exception as ex:
        logging.error(f"в фукнции update_user при обновлении данных произошло исключение \n {ex}")
        return jsonify({'error': ex})
    logging.info(f"result : ok")
    return jsonify({'result': 'ok'})


# Конец блока работы с таблицей USER

# Блок кода реализации получения истории заказа пользователя
@app.route('/test_task/api/order_data_user/<int:user_id>', methods=['GET'])
def user_order_history(user_id):
    """Функция для получения истории заказа пользователя по ID
    :param user_id: id пользователя : int
    :return история заказа пользователя в формате JSON"""
    json_data = []
    logging.info(
        f"поступил запрос на получении информации о истории заказа пользователя с ID={user_id} с IP:{request.remote_addr}")
    # создадим сессию и сформируем запрос
    # вынесем запрос в переменную для записи отладочной информации
    m_query = select(User, Order, Orderitem, Shop, Book).select_from(Order).join(User).join(Orderitem).join(Shop).join(
        Book).where(User.id == user_id)
    logging.debug(f"запрос на получение списка пользователя по=ID {user_id} \n{m_query}")
    try:
        with session() as s:
            for row in s.execute(m_query):
                # в цикле заполняем наш json_data результатом  запроса
                json_data.append({'id_user': row[0].id, 'last_name': row[0].last_name, 'first_name': row[0].first_name,
                                  'email': row[0].email, 'order_id': row[1].id, 'reg_date': row[1].reg_date, 'book_name': row[4].name,
                                  'book_quantity': row[2].book_quantity, 'shop_name': row[3].name,
                                  'shop_address': row[3].address})
    except Exception as ex:
        logging.error(f"в фукнции user_order_history произошло исключение \n {ex}")
        return jsonify({'error': ex})
    logging.debug(f"результат запроса \n {json_data}")
    # проверяем что список пуст, если пуст значит пользователя нет и вернем 404
    if len(json_data) == 0:
        logging.info(f"пользователя с id {user_id} нет в таблице user")
        return abort(404)
    logging.info(f"result : ok")
    return jsonify({'user_order_history': json_data})


# Конец блока кода реализации получения истории заказа пользователя

# Блок кода реализации получения данных определенного заказа
@app.route('/test_task/api/order_data/<int:order_id>', methods=['GET'])
def order_data(order_id):
    """Функция для получения истории заказа  по ID
    :param order_id: номер заказа : int
    :return история заказа по номеру в формате JSON"""
    json_data = []
    logging.info(
        f"поступил запрос на получение информации о истории заказа  с ID={order_id} с IP:{request.remote_addr}")
    # создадим сессию и сформируем запрос
    # вынесем запрос в переменную для записи отладочной информации
    m_query = select(User, Order, Orderitem, Shop, Book).select_from(Order).join(User).join(Orderitem).join(Shop).join(
        Book).where(Order.id == order_id)
    logging.debug(f"запрос на получение списка пользователя по=ID {order_id} \n{m_query}")
    try:
        with session() as s:
            for row in s.execute(m_query):
                # в цикле заполняем наш json_data результатом  запроса
                json_data.append({'id_user': row[0].id, 'last_name': row[0].last_name, 'first_name': row[0].first_name,
                                  'email': row[0].email, 'order_id':row[1].id,'reg_date': row[1].reg_date, 'book_name': row[4].name,
                                  'book_quantity': row[2].book_quantity, 'shop_name': row[3].name,
                                  'shop_address': row[3].address})
    except Exception as ex:
        logging.error(f"в фукнции order_data произошло исключение \n {ex}")
        return jsonify({'error': ex})
    logging.debug(f"результат запроса \n {json_data}")
    # проверяем что список пуст, если пуст значит пользователя нет и вернем 404
    if len(json_data) == 0:
        logging.info(f"заказа с id {order_id} нет в таблице order")
        return abort(404)
    logging.info(f"result : ok")
    return jsonify({'order_data': json_data})


# Конец блока кода реализации получения данных определенного заказа

# Блок кода создание нового заказа
# Будем считать что данные для создания заказа всегда приходят кореектные ( shop_id,
# book_id,user_id и тд ) а так можно реализовать задачу используя подзапросы и проверять что есть магазин,
# книга и пользователь,  если хоть чего то нет вызывать исключение и откатывать транзакцию
@app.route('/test_task/api/order_data', methods=['POST'])
def create_order():
    """Функция для создания заказа"""
    request_data = request.json
    logging.info(f"поступил запрос на создание  пользователя с IP:{request.remote_addr}")
    logging.debug(f"JSON данные которые пришли {request_data}")
    # установим сессию и добавить пользователя в бд
    try:
        with session() as s:
            # при открытии сессии у нас открывается транзакция и пока транзакция открыта, изменения другие транзакции
            # внести не могут.
            # получим максимальный order.id и присвоим новый id заказа
            max_order_id = [row[0] for row in s.execute(select(func.max(Order.id)))][0]
            logging.debug(f"получено максимальное текущее order.id={max_order_id}")
            max_order_id += 1
            query_order = insert(Order).values(id=max_order_id, reg_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
                                               user_id=request_data["user_id"])
            query_orderitem = insert(Orderitem).values(order_id=max_order_id, book_id=request_data['book_id'],
                                                       shop_id=request_data['shop_id'],
                                                       book_quantity=request_data["book_quantity"])
            logging.debug(f"запрос на добавление данных в таблицу order \n{query_order}")
            logging.debug(f"запрос на добавление данных в таблицу orderitem \n{query_orderitem}")
            # выполним запросы
            s.execute(query_order)
            s.execute(query_orderitem)
            # зафиксируем транзакцию
            s.commit()

    except Exception as ex:
        logging.error(f"в фукнции create_order произошло исключение \n {ex}")
        return jsonify({'error': ex})
    logging.info(f"result : ok")
    return jsonify({'order_id': max_order_id, 'result': 'ok'})


# Конец блок кода создания нового заказа

# поменяем формат ответа ошибки 404 на JSON
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    main()
    app.run(debug=True)
