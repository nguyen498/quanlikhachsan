import math
from flask import render_template, request, redirect, url_for
from sqlalchemy.sql.elements import Null
from hotelapp import app, utils
from hotelapp import login_manager
from flask_login import current_user, login_user, logout_user
from hotelapp.models import UserRole
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
    first_check_is_done = False
    success_msg = ""
    err_msg = ""
    reserveBy = request.form.get('reserveBy')
    phone = request.form.get('phone')
    checkInTime = request.form.get('checkInTime')
    checkoutTime = request.form.get('checkoutTime')
    
    customerNames = request.form.getlist('customerName[]')
    customerTypes = request.form.getlist('customerType[]')
    idCards = request.form.getlist('idCard[]')
    addresses = request.form.getlist('address[]')
    family_number = len(customerNames)

    if request.method == 'POST':
        reserveInfos = [reserveBy, phone, checkInTime, checkoutTime]
        familyInfos = [customerNames, customerTypes, addresses]


        # Reserve Room
        try:
            # Check if customer has members
            if family_number > 0:
                # Check if customer enter family infos (any: True if any info True)
                if any(familyInfos) or idCards:
                    # Check if familyInfos contain empty value (all: True if all info True)
                    if all(familyInfos):
                        first_check_is_done = True
                    else:
                        err_msg = "Please enter full Family info in the form"
            else:
                first_check_is_done = True

            # Check if ReserveInfo contain empty value 
            if all(reserveInfos) and first_check_is_done:
                utils.reserveRoom(customerNames, customerTypes, idCards, addresses, room_id, reserveBy, checkInTime, checkoutTime, phone)
                success_msg = "Reserve Room Successfully"
            else:
                err_msg = "Please enter full reservation info in the form"
        except Exception as exception:
            err_msg = 'Error from server: ' + str(exception)

    
    # Render Template
    room = utils.get_room_by_id(id=room_id)
    customer_types_db = utils.get_customer_type()
    return render_template('/client/pages/checkout.html'
        , room=room
        , customer_types_db=customer_types_db
        , success_msg=success_msg
        , err_msg=err_msg
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
        "./client/pages/room_details.html",
        title=room.name,
        room=room
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

    return render_template('/client/pages/register.html',
                           error_msg=error_msg)


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
