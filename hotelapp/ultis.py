from hotelapp import app, db
from hotelapp.models import KindOfRoom, Room


def load_kindofroom():
    return KindOfRoom.query.all()


def load_room():
    return Room.query.all()
