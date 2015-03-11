# coding: utf-8

from __future__ import absolute_import, print_function

from datetime import datetime
from decimal import Decimal
from pony.orm import *

from decimal import Decimal
from datetime import date



db = Database("sqlite", "database.sqlite", create_db=True)

class Client(db.Entity):
    email = Required(unicode, unique=True)
    password = Required(unicode)
    name = Required(unicode)
    country = Required(unicode)
    address = Required(unicode)
    orders = Set("Order")


class Order(db.Entity):
    id = PrimaryKey(int, auto=True)
    state = Required(unicode)
    date_created = Required(datetime)
    date_delivered = Optional(datetime)
    total_price = Required(Decimal)
    client = Required(Client)
    items = Set("Order_Item")


class Discount(db.Entity):
    amount = Required(int)
    date_start = Required(datetime)
    date_expired = Required(datetime)
    brand = Required(unicode)
    clothing = Set("Clothing")


class Brand(db.Entity):
    name = Required(unicode)
    country = Required(unicode)
    description = Optional(unicode)
    clothing = Set("Clothing")


class Category(db.Entity):
    name = Required(unicode)
    clothing = Set("Clothing")


class Clothing(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(unicode)
    description = Optional(unicode)
    picture = Optional(buffer)
    price = Required(Decimal)
    category = Required(Category)
    brand = Required(Brand)
    store = Optional("Store")
    order__items = Set("Order_Item")
    discount = Optional(Discount)


class Store(db.Entity):
    country = Required(unicode)
    adress = Required(unicode)
    clothing = Set(Clothing)


class Order_Item(db.Entity):
    quantity = Required(int)
    price = Required(Decimal)
    order = Required(Order)
    clothing = Required(Clothing)
    PrimaryKey(order, clothing)


sql_debug(True)
db.generate_mapping(create_tables=True)

@db_session
def populate_database():
    if select(s for s in Client).count() > 0:
        return

    s1 = Client(email='js@gmail.com', password='1245', name='John', country='russia', address='192111 Moscow')

    c1 = Category(name=u'Брюки')
    c2 = Category(name=u'Обувь')

    b1 = Brand (name = 'Nike', country = 'usa')

    cl1 = Clothing(name=u'Штаны обыкновенные',price = 500, category = c1, brand = b1)



populate_database()
