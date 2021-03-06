from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.sqltypes import Numeric, Text
from hotelapp import db
from enum import Enum as UserEnum
from flask_login import UserMixin

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


class RoomType(BaseModel):
    __tablename__ = 'room_type'

    name = Column(String(50), nullable=False)
    room = relationship('Room', backref='RoomType', lazy=True)

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
    category_id = Column(Integer, ForeignKey(RoomType.id), nullable=False)

    def __str__(self):
        return self.name


class CustomerType(BaseModel):
    __tablename__ = 'customer_type'

    name = Column(String(50), nullable=False)
    customer = relationship('Customer', backref='CustomerType', lazy=True)

    def __str__(self):
        return self.name


class Customer(BaseModel):
    __tablename__ = 'customer'

    name = Column(String(50), nullable=False)
    phone = Column(Numeric(50), nullable=True)
    idCard = Column(String(50), nullable=True)
    address = Column(String(255), nullable=True)
    type_id = Column(Integer, ForeignKey(CustomerType.id), nullable=True)

    def __str__(self):
        return self.name


class Reservation(BaseModel):
    __tablename__ = 'reservation'

    reserveBy = Column(String(50), nullable=False)
    phone = Column(String(50))
    checkInTime = Column(DateTime, default=datetime.now())
    checkOutTime = Column(DateTime, default=datetime.now())
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    customers = relationship('Customer', secondary='customer_reservation', lazy='subquery',
                        backref=backref('reservations', lazy=True))


class CustomerReservation(db.Model):
    __tablename__ = 'customer_reservation'

    reservation_id = Column(Integer, ForeignKey(Reservation.id), nullable=False, primary_key=True)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False, primary_key=True)



class Registration(BaseModel):
    __tablename__ = 'registration'

    checkInTime = Column(DateTime, default=datetime.now())
    checkOutTime = Column(DateTime, default=datetime.now())
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    customers = relationship('Customer', secondary='customer_registration', lazy='subquery',
                        backref=backref('registrations', lazy=True))

class CustomerRegistration(db.Model):
    __tablename__ = 'customer_registration'

    registration_id = Column(Integer, ForeignKey(Registration.id), nullable=False, primary_key=True)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False, primary_key=True)



class Receipt(BaseModel):
    __tablename__ = 'receipt'

    checkInTime = Column(DateTime, default=datetime.now())
    checkOutTime = Column(DateTime, default=datetime.now())
    unitPrice = Column(Float, default=0)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    reservation_id = Column(Integer, ForeignKey(Reservation.id), nullable=True)
    registration_id = Column(Integer, ForeignKey(Registration.id), nullable=True)
    surcharges = relationship('Surcharge', secondary='receipt_surcharge', lazy='subquery',
                        backref=backref('receipts', lazy=True))

class Surcharge(BaseModel):
    __tablename__ = 'surcharge'

    description = Column(Text(255), nullable=False)
    ratio = Column(Float, default=1)

    def __str__(self):
        return '* ' + str(self.ratio)


class ReceiptSurcharge(BaseModel):
    __tablename__ = 'receipt_surcharge'

    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    surcharge_id = Column(Integer, ForeignKey(Surcharge.id), nullable=False, primary_key=True)




if __name__ == '__main__':
    db.create_all()

    admin2 = User(name="admin2", username="admin2",
                  password="202cb962ac59075b964b07152d234b70", email="123", active=True, user_role="ADMIN")

    db.session.add(admin2)

    s1 = Surcharge(description="Kha??ch ha??ng >= 3", ratio=1.25)
    s2 = Surcharge(description="Co?? kha??ch qu????c t????", ratio=1.5)

    db.session.add(s1)
    db.session.add(s2)

    ct1 = CustomerType(name='Qu????c T????')
    ct2 = CustomerType(name='Trong N??????c')

    db.session.add(ct1)
    db.session.add(ct2)

    k1 = RoomType(name='Ph??ng ????n')
    k2 = RoomType(name='Ph??ng ????i')
    k3 = RoomType(name='Ph??ng ba')
    k4 = RoomType(name='Ph??ng gia ????nh')
    k5 = RoomType(name='Homestay')
    
    db.session.add(k1)
    db.session.add(k2)
    db.session.add(k3)
    db.session.add(k4)
    db.session.add(k5)
    
    rooms = [{
        "id": 1,
        "name": "Deluxe gi?????ng ????n",
        "description": "Wifi mi???n ph??\n1 gi?????ng nh???\nDi???n t??ch ph??ng: 32 m??\nH?????ng ph??ng: Th??nh ph???\nPh??ng t???m v??i sen & b???n t???m",
        "price": 400000,
        "image": "images/p1.png",
        "quantity": 2,
        "category_id": 1
    }, {
        "id": 2,
        "name": "Ph??ng hai gi?????ng th?????ng",
        "description": "Wifi mi???n ph??\n1 gi?????ng l???n,1 gi?????ng nh???\nDi???n t??ch ph??ng: 32 m??\nH?????ng ph??ng: Th??nh ph???\nPh??ng t???m v??i sen & b???n t???m",
        "price": 700000,
        "image": "images/p2.png",
        "quantity": 4,
        "category_id": 2
    }, {
        "id": 3,
        "name": "Ph??ng ba gi?????ng th?????ng",
        "description": "Wifi mi???n ph??\n1 gi?????ng l???n, 2 gi?????ng nh???\nDi???n t??ch ph??ng: 50 m??\nH?????ng ph??ng: Th??nh ph???\nPh??ng t???m v??i sen & b???n t???m",
        "price": 1000000,
        "image": "images/p3.png",
        "quantity": 6,
        "category_id": 3
    }, {
        "id": 4,
        "name": "Ph??ng gia ????nh th?????ng",
        "description": "Wifi mi???n ph??\n2 gi?????ng l???n, 1 gi?????ng nh???\nDi???n t??ch ph??ng: 60 m??\nH?????ng ph??ng: Th??nh ph???\nPh??ng t???m v??i sen & b???n t???m",
        "price": 1200000,
        "image": "images/p4.png",
        "quantity": 6,
        "category_id": 4
    }, {
        "id": 5,
        "name": "Homestay",
        "description": "Wifi mi???n ph??\n2 ph??ng l???n, 2 ph??ng nh???\nDi???n t??ch nh??: 100 m??\nH?????ng ph??ng: Th??nh ph???\nPh??ng t???m v??i sen & b???n t???m",
        "price": 3000000,
        "image": "images/p5.png",
        "quantity": 8,
        "category_id": 5
    }]
    
    for r in rooms:
        ro = Room(name=r['name'], price=r['price'], image=r['image'], quantity=r['quantity'],
                  description=r['description'], category_id=r['category_id'])
        db.session.add(ro)
    
    db.session.commit()
    
    r = Room(name='phong mot giuong vip',
             description='Wifi mi???n ph??\n1 gi?????ng nh???\nDi???n t??ch ph??ng: 32 m??\nH?????ng ph??ng: Th??nh ph???\nPh??ng t???m v??i sen & b???n t???m',
             price='1000000', image="images/p1.png", category_id='1')
    db.session.add(r)
    db.session.commit()
