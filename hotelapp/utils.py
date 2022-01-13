from hotelapp import app, db
from hotelapp.models import Customer, CustomerRegistration, CustomerReservation, CustomerType, Receipt, ReceiptSurcharge, Registration, Reservation, RoomType, Room, Surcharge, User, UserRole
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

def get_rooms():
    return Room.query.all()



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



def get_receipts():
    return Receipt.query.all()

def get_receipt_by_id(id):
    return db.session.query(Receipt, Registration, Customer, Surcharge)\
                    .filter(Receipt.id.__eq__(id))\
                    .join(Customer, Receipt.customer_id.__eq__(Customer.id))\
                    .join(Registration, Receipt.registration_id.__eq__(Registration.id))\
                    .join(Surcharge, Receipt.registration_id.__eq__(Registration.id))\
                    .first()\

def get_receipt_surcharges(receipt_id):
    return db.session.query(ReceiptSurcharge, Surcharge)\
                    .filter(ReceiptSurcharge.receipt_id.__eq__(receipt_id))\
                    .join(Surcharge, ReceiptSurcharge.surcharge_id.__eq__(Surcharge.id))\
                    .all()\

def set_room_status_by_id(room_id, room_status):
    room = Room.query.get(room_id)
    room.active = room_status
    db.session.commit()

def get_customer_type_by_name(name):
    return CustomerType.query.filter(CustomerType.name.__eq__(name)).first()

def get_surcharge_by_id(id):
    return Surcharge.query.filter(Surcharge.id.__eq__(id)).first()

def create_customer(name, idCard=None, customerType=None, address=None, phone=None):
    new_customer = Customer(
        name=name,
        idCard=idCard,
        address=address,
        type_id=customerType,
        phone=phone
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
    
    return new_reservation



def create_customer_registration(registration_id, customer_id):
    new_customer_registration = CustomerRegistration(
        registration_id=registration_id,
        customer_id=customer_id
    )
    db.session.add(new_customer_registration)
    db.session.commit()


def create_registration(room_id, checkInTime, checkOutTime):
    new_registration = Registration(
        room_id=room_id
        , checkInTime=checkInTime
        , checkOutTime=checkOutTime
    )
    db.session.add(new_registration)
    db.session.commit()
    return new_registration


def registerRoom(customerNames, customerTypes, idCards, addresses,
                room_id, checkInTime, checkoutTime):
    # Create registration
    new_registration = create_registration(room_id, checkInTime, checkoutTime)
    
    for i in range(0, len(customerNames)):
        # Create Each Customer
        new_customer = create_customer(customerNames[i], idCards[i], customerTypes[i], addresses[i])
        # Add Each Family Customer to Customerregistration
        create_customer_registration(new_registration.id, new_customer.id)
        # Gán khách hàng đầu tiên vào biến first_customer
        if i == 0:
            first_customer = new_customer
    
    return new_registration, first_customer


def create_receipt(checkInTime, checkOutTime, unitPrice, customer_id, reservation_id=None, registration_id=None):
    new_receipt = Receipt(
        checkInTime=checkInTime
        , checkOutTime=checkOutTime
        , unitPrice=unitPrice
        , customer_id=customer_id
        , reservation_id=reservation_id
        , registration_id=registration_id
    )
    db.session.add(new_receipt)
    db.session.commit()

    return new_receipt


def create_receipt_surcharge(receipt_id, surcharge_id):
    new_receipt_surcharge = ReceiptSurcharge(
        receipt_id=receipt_id
        , surcharge_id=surcharge_id
    )
    db.session.add(new_receipt_surcharge)
    db.session.commit()

    return new_receipt_surcharge
    


def validate_reservation(reserveInfos, familyInfos, family_members, room_capacity, idCards):
    first_check_is_done = False
    # First Check if customer has members
    if family_members > 0:
        # Check if customer enter more than room capacity
        if family_members <= room_capacity:
            pass
        else:
            err_msg = "Exceed person limit in a room"
            return False, err_msg
            
        # Check if customer enter family infos (any: True if any info True)
        if any(familyInfos) or idCards:
            # Check if familyInfos contain empty value (all: True if all info True)
            if all(familyInfos):
                first_check_is_done = True
            else:
                err_msg = "Please enter full Family info in the form"
                return False, err_msg
    else:
        first_check_is_done = True

    # Second Check if ReserveInfo contain empty value
    if all(reserveInfos) and first_check_is_done:
        success_msg = "Reserve Room Successfully"
    else:
        err_msg = "Please enter full reservation info in the form"
        return False, err_msg

    return True, success_msg
   
   
    