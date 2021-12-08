from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from hotelapp import db
from enum import Enum as UserEnum


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class User(BaseModel):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


class KindOfRoom(BaseModel):
    __tablename__ = 'kindofroom'

    name = Column(String(50), nullable=False)
    room = relationship('Room', backref='KindOfRoom', lazy=True)

    def __str__(self):
        return self.name


class Room(BaseModel):
    __tablename__ = 'room'

    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Float, default=0)
    image = Column(String(255))
    active = Column(Boolean, default=True)
    quantity = Column(Integer, default=1)
    kind_id = Column(Integer, ForeignKey(KindOfRoom.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
   db.create_all()

    # k1 = KindOfRoom(name='Phòng đơn')
    # k2 = KindOfRoom(name='Phòng đôi')
    # k3 = KindOfRoom(name='Phòng ba')
    # k4 = KindOfRoom(name='Phòng gia đình')
    # k5 = KindOfRoom(name='Homestay')
    #
    # db.session.add(k1)
    # db.session.add(k2)
    # db.session.add(k3)
    # db.session.add(k4)
    # db.session.add(k5)
    #
    # db.session.commit()

    # room = [{
    #     "id": 1,
    #     "name": "Deluxe giường đơn",
    #     "description": "Wifi miễn phí\n1 giường nhỏ\nDiện tích phòng: 32 m²\nHướng phòng: Thành phố\nPhòng tắm vòi sen & bồn tắm",
    #     "price": 400000,
    #     "image": "images/p1.png",
    #     "quantity": 2,
    #     "kind_id": 1
    # }, {
    #     "id": 2,
    #     "name": "Phòng hai giường thường",
    #     "description": "Wifi miễn phí\n1 giường lớn,1 giường nhỏ\nDiện tích phòng: 32 m²\nHướng phòng: Thành phố\nPhòng tắm vòi sen & bồn tắm",
    #     "price": 700000,
    #     "image": "images/p2.png",
    #     "quantity": 4,
    #     "kind_id": 2
    # }, {
    #     "id": 3,
    #     "name": "Phòng ba giường thường",
    #     "description": "Wifi miễn phí\n1 giường lớn, 2 giường nhỏ\nDiện tích phòng: 50 m²\nHướng phòng: Thành phố\nPhòng tắm vòi sen & bồn tắm",
    #     "price": 1000000,
    #     "image": "images/p3.png",
    #     "quantity": 6,
    #     "kind_id": 3
    # }, {
    #     "id": 4,
    #     "name": "Phòng gia đình thường",
    #     "description": "Wifi miễn phí\n2 giường lớn, 1 giường nhỏ\nDiện tích phòng: 60 m²\nHướng phòng: Thành phố\nPhòng tắm vòi sen & bồn tắm",
    #     "price": 1200000,
    #     "image": "images/p4.png",
    #     "quantity": 6,
    #     "kind_id": 4
    # }, {
    #     "id": 5,
    #     "name": "Homestay",
    #     "description": "Wifi miễn phí\n2 phòng lớn, 2 phòng nhỏ\nDiện tích nhà: 100 m²\nHướng phòng: Thành phố\nPhòng tắm vòi sen & bồn tắm",
    #     "price": 3000000,
    #     "image": "images/p5.png",
    #     "quantity": 8,
    #     "kind_id": 5
    # }]
    #
    # for r in room:
    #     ro = Room(name=r['name'], price=r['price'], image=r['image'], quantity=r['quantity'],
    #               description=r['description'], kind_id=r['kind_id'])
    #     db.session.add(ro)
    #
    # db.session.commit()

    # r = Room(name='phong mot giuong vip',
    #          description='Wifi miễn phí1 giường nhỏDiện tích phòng: 32 m²Hướng phòng: Thành phốPhòng tắm vòi sen & bồn tắm',
    #          price='1000000', image="images/p1.png", kind_id='1')
    # db.session.add(r)
    # db.session.commit()
