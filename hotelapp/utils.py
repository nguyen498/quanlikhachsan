from hotelapp import app, db
from hotelapp.models import Customer, CustomerReservation, CustomerType, Reservation, RoomType, Room, User, UserRole
from sqlalchemy import  func
import hashlib


def load_kindofroom():
    return RoomType.query.all()


def get_room(kw=None, category_id=None, from_price=None, to_price=None, page=1):
    rooms = Room.query.filter(Room.active.__eq__(True))

    if category_id:
        rooms = rooms.filter(Room.category_id.__eq__(category_id))

    if kw:
        rooms = rooms.filter(Room.name.contains(kw))

    if from_price:
        rooms = rooms.filter(Room.price.__ge__(from_price))

    if to_price:
        rooms = rooms.filter(Room.price.__le__(to_price))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return rooms.slice(start, end).all()



def count_products():
    return Room.query.filter(Room.active.__eq__(True)).count()


def count_room_in_category(category_id):
    return Room.query.filter(Room.category_id.__eq__(category_id)).count()


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name, username=username,
                password=password,
                email=kwargs.get('email'))

    db.session.add(user)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_category_by_id(category_id):
    return RoomType.query.get(category_id)





def check_login(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(
            User.username.__eq__(username.strip()),
            User.password.__eq__(password)
        ).first()


#Lay du lieu thong ke
def kind_stats():
    return db.session.query(RoomType.id, RoomType.name, func.count(Room.id))\
                     .join(Room, RoomType.id.__eq__(Room.category_id))\
                     .group_by(RoomType.id, RoomType.name).all()

def get_room_by_id(id):
    return Room.query.get(id)

def get_customer_type():
    return CustomerType.query.all()


def create_customer(name, idCard, customerType, address):
    new_customer = Customer(
        name=name,
        idCard=idCard,
        address=address,
        type_id=customerType
    )
    db.session.add(new_customer)
    db.session.commit()
    return new_customer
    

def create_reservation(room_id, reserveBy, checkInTime, checkOutTime, phone):
    new_reservation = Reservation(
        room_id=room_id,
        reserveBy=reserveBy,
        phone=phone,
        checkInTime=checkInTime,
        checkOutTime=checkOutTime
    )
    db.session.add(new_reservation)
    db.session.commit()
    return new_reservation


def create_customer_reservation(reservation_id, customer_id):
    new_customer_reservation = CustomerReservation(
        reservation_id=reservation_id,
        customer_id=customer_id
    )
    db.session.add(new_customer_reservation)
    db.session.commit()


def reserveRoom(customerNames, customerTypes, idCards, addresses,
                room_id, reserveBy, checkInTime, checkoutTime, phone):
    # Create reservation
    new_reservation = create_reservation(room_id, reserveBy, checkInTime, checkoutTime, phone)
    
    for i in range(0, len(customerNames)):
        # Create Each Customer
        new_customer = create_customer(customerNames[i], idCards[i], customerTypes[i], addresses[i])
        # Add Each Family Customer to CustomerReservation
        create_customer_reservation(new_reservation.id, new_customer.id)
    
    
   
   
    