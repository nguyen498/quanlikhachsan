from datetime import datetime
import math
from flask import render_template, request, redirect, url_for
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from hotelapp import app, utils
from hotelapp import login_manager
from flask_login import current_user, login_user, logout_user
from hotelapp.models import Surcharge, UserRole
from hotelapp.admin import *

# You will need to provide a user_loader callback.
# This callback is used to reload the user object from the user ID stored in the session


# Admin
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    error_msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = utils.check_login(username=username, password=password, role=UserRole.ADMIN)
        if user:
            login_user(user)

        return redirect('admin')


# Client
@app.route("/")
def home():
    category_id = request.args.get("category_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    s = "Wellcome to my website"
    room = utils.get_room(category_id=category_id, kw=kw, from_price=from_price,
                           to_price=to_price)
    return render_template('/client/pages/index.html', s=s, room=room)


@app.route("/checkout/<int:room_id>", methods=['GET', 'POST'])
def checkout(room_id):
    validation_message = ""
    validation_is_valid = False
    room = utils.get_room_by_id(id=room_id)
    customer_types_db = utils.get_customer_type()
    

    if request.method == 'POST':
        # Surcharge Variables
        customer_foreign_type_db = utils.get_customer_type_by_name("Quốc tế")

        # reservation info
        reserveBy = request.form.get('reserveBy')
        phone = request.form.get('phone')
        checkInTime = request.form.get('checkInTime')
        checkOutTime = request.form.get('checkOutTime')

        # date format
        date_format = "%Y-%m-%d"
        d1 = datetime.strptime(checkInTime, date_format)
        d2 = datetime.strptime(checkOutTime, date_format)
        delta = d2 - d1
        days_diff = delta.days

        # Families info
        customerNames = request.form.getlist('customerName[]')
        customerTypes = request.form.getlist('customerType[]')
        idCards = request.form.getlist('idCard[]')
        addresses = request.form.getlist('address[]')
        family_members = len(customerNames)
        room_capacity = room.quantity

        # Array of infos
        reserveInfos = [reserveBy, phone, checkInTime, checkOutTime]
        familyInfos = [customerNames, customerTypes, addresses]

        # Validation steps
        validation_result = utils.validate_reservation(reserveInfos, familyInfos, family_members, room_capacity, idCards)
        validation_is_valid = validation_result[0]
        validation_message = validation_result[1]
        
       
        # reserve Room steps after validation
        try:

            if validation_is_valid:
                # Lưu người đặt phòng
                reservePerson = utils.create_customer(name=reserveBy, phone=phone)
                # Đặt phòng
                reservation = utils.reserveRoom(customerNames, customerTypes, idCards, addresses, room_id, reserveBy, checkInTime, checkOutTime, phone)
                # Tính tiền phòng theo số ngày
                total_amount = room.price * days_diff
                # Tạo hóa đơn
                receipt = utils.create_receipt(checkInTime=checkInTime, checkOutTime=checkOutTime, unitPrice=total_amount,
                                     customer_id=reservePerson.id, reservation_id=reservation.id)
                # Thêm phụ thu id vào ReceiptSurcharge của hó đơn vừa tạo
                if family_members >= 3:
                    utils.create_receipt_surcharge(receipt.id, utils.get_surcharge_by_id(1).id)
                if [customer_type_id for customer_type_id in customerTypes if str(customer_type_id).__eq__(str(customer_foreign_type_db.id))]:
                    utils.create_receipt_surcharge(receipt.id, utils.get_surcharge_by_id(2).id)

        except Exception as exception:
            validation_is_valid = False
            validation_message = 'Error from server: ' + str(exception)

    
    return render_template('/client/pages/checkout.html'
        , room=room
        , customer_types_db=customer_types_db
        , success_msg=validation_message if validation_is_valid else ""
        , err_msg=validation_message if not validation_is_valid else ""
    )


@app.route("/category/<int:category_id>")
def category_detail(category_id):
    # get parameters
    keyword = request.args.get('keyword', "")
    category = utils.get_category_by_id(category_id)
    page = request.args.get('page', 1)
    room = utils.get_room(kw=keyword, category_id=category_id, page=int(page))
    
    return render_template(
        '/client/pages/category.html',
        title=category.name,
        category=category, 
        room=room,
        pages=math.ceil(utils.count_room_in_category(category_id)/app.config['PAGE_SIZE'])
    )



@app.route("/room/<int:room_id>")
def room_detail(room_id):
    room = utils.get_room_by_id(id=room_id)
    return render_template(
        "./client/pages/room_details.html"
        , title=room.name
        , room=room
    )
    
# Client
@app.route("/login", methods=['get', 'post'])
def user_login():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = utils.check_login(username=username, password=password, role=UserRole.USER)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg = "Username hoặc password không chính xác"

    return render_template("client/pages/login.html", err_msg=err_msg)


@app.route("/user-logout")
def logout():
    logout_user()
    return redirect(url_for('user_login'))


@app.route('/register', methods=['get', 'post'])
def user_register():
    error_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        try:
            if password.strip().__eq__(confirm.strip()):
                utils.add_user(name=name, username=username,
                               password=password, email=email)
                return redirect(url_for('user_login'))
            else:
                error_msg = 'Password not confirm!!'
        except Exception as ex:
            error_msg = "He thong bi loi: " + str(ex)

    return render_template('/client/pages/register.html', error_msg=error_msg)


@app.context_processor
def common_response():
    return {
        'kindofroom': utils.load_kindofroom()
    }


@login_manager.user_loader
def inject_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


if __name__ == "__main__":
    from hotelapp.admin import *

    app.run(debug=True)
