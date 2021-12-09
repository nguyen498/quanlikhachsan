from hotelapp import app, db
from hotelapp.models import KindOfRoom, Room, User, UserRole
import hashlib


def load_kindofroom():
    return KindOfRoom.query.all()


def load_room(kind_id=None, kw=None, from_price=None, to_price=None, page=1):
    rooms = Room.query.filter(Room.active.__eq__(True))

    if kind_id:
        rooms = rooms.filter(Room.category_id.__eq__(kind_id))

    if kw:
        rooms = rooms.filter(Room.name.contains(kw))

    if from_price:
        rooms = rooms.filter(Room.price.__ge__(from_price))

    if to_price:
        rooms = rooms.filter(Room.price.__le__(to_price))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size

    return rooms.slice(start, start + page_size).all()


def count_products():
    return Room.query.filter(Room.active.__eq__(True)).count()


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name, username=username,
                password=password,
                email=kwargs.get('email'))

    db.session.add(user)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def check_login(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(
            User.username.__eq__(username.strip()),
            User.password.__eq__(password)
        ).first()
