from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import os.path


Base = declarative_base()  # используем декларативный подход


# создадим классы наследуемые от класса base
# создадим таблицу user
# связь 1 ко многим  user.id к Order.user_id
class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    last_name = Column(String(250))
    first_name = Column(String(250))
    email = Column(String(250))
    order = relationship("Order")  # связь 1 ко многим


# создадим таблицу Order
# связь 1 ко многим  Order.id к Orderitem.order_id
class Order(Base):
    __tablename__ = 'Order'

    id = Column(Integer, primary_key=True)
    reg_date = Column(String(250))
    user_id = Column(Integer, ForeignKey("User.id"))
    user = relationship("User")  # связь 1 ко многим
    orderitem = relationship("Orderitem")


# создадим таблицу Orderitem
# многие к 1 Orderitem.book_id к Book.id и Orderitem.shop_id к Shop.id
class Orderitem(Base):
    __tablename__ = 'Orderitem'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("Order.id"))
    book_id = Column(Integer, ForeignKey("Book.id"))
    shop_id = Column(Integer, ForeignKey("Shop.id"))
    book_quantity = Column(Integer)
    order = relationship("Order")
    shop = relationship("Order")
    book = relationship("Order")
    overlaps = "order,orderitem,shop"


# создадим таблицу Shop
class Shop(Base):
    __tablename__ = 'Shop'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    address = Column(String(250))
    orderitem = relationship("Orderitem")


# создадим таблицу Book
class Book(Base):
    __tablename__ = 'Book'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    author = Column(String(250))
    release_date = Column(String(250))
    orderitem = relationship("Orderitem")


def init_db(path_db, engine, log):
    """Функция для создание и загрузки данных в бд"
    :param log: класс логирования: class Logging
    :param engine: соединение с БД
    :param path_db: путь до базы данных str
    :return результат выполнения
    """
    try:
        # проверим что бд по пути нет
        if not os.path.exists(f'./{path_db}', ):
            log.error("базы данных по пути нет, создадим")
            # создадим БД
            Base.metadata.create_all(engine)
            session = sessionmaker(bind=engine)
            # откроем транзакцию и выполним запрос
            with session() as s:
                users_all = ([User(last_name="Smirnov", first_name="Alex", email="Alex@mail.ru"),
                              User(last_name="Ivanov", first_name="Ivan", email="ivanov@mail.ru"),
                              User(last_name="Petrova", first_name="Anna", email="Anna@gmail.com")])
                shops_all = (
                    [Shop(name="""Москва книжный магазин""", address="""Тверская ул., 8, стр. 1, Москва, 125009"""),
                     Shop(name="""Книжная лавка""", address="""ул. Арбат, 20, Москва, 119002""")])
                books_all = ([Book(name="Изучаем Python", author="Марк Лутц", release_date="2009"),
                              Book(name="Менялы", author="Артур Хейли", release_date="1975"),
                              Book(name="Война и Мир", author="Лев Толстой", release_date="1867"),
                              Book(name="Детство", author="Лев Толстой", release_date="1852")])
                orders_all = ([Order(reg_date="2022-07-02 19:39", user_id="1"),
                               Order(reg_date="2022-02-02 09:00", user_id="2"),
                               Order(reg_date="2022-01-03 18:40", user_id="3"),
                               Order(reg_date="2020-05-03 10:00", user_id="2")
                               ])
                orderitems_all = ([Orderitem(order_id="1", book_id="1", shop_id="1", book_quantity="3"),
                                   Orderitem(order_id="2", book_id="2", shop_id="2", book_quantity="1"),
                                   Orderitem(order_id="3", book_id="4", shop_id="1", book_quantity="1"),
                                   Orderitem(order_id="4", book_id="1", shop_id="1", book_quantity="1")
                                   ])
                s.add_all(users_all)
                s.add_all(shops_all)
                s.add_all(books_all)
                s.add_all(orders_all)
                s.add_all(orderitems_all)
                # применим транзакцию
                s.commit()
            log.info(f"база данных создана")
            return 'database created'
        return "database exists"
    except Exception as ex:
        os.remove(f'./{path_db}')
        log.error(f"произошла ошибка при создании базы данных {ex}")
