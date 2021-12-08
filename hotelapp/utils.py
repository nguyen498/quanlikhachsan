from hotelapp import app, db
from hotelapp.models import KindOfRoom, Room, User
import hashlib


def load_kindofroom():
    return KindOfRoom.query.all()


def load_room():
    return Room.query.all()


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name, username=username, password=password,
                email=kwargs.get('email'))

    db.session.add(user)
    db.session.commit()
