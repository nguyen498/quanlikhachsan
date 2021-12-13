import math
from flask import render_template, request, redirect, url_for
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

        return redirect('/admin')


# Client
@app.route("/")
def home():
    kind_id = request.args.get("kind_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    page = request.args.get('page', 1)
    s = "Wellcome to my website"
    room = utils.load_room(kind_id=kind_id, kw=kw, from_price=from_price,
                           to_price=to_price, page=int(page))
    return render_template('/client/pages/index.html', s=s, room=room,
                           pages=math.ceil(utils.count_products()/app.config['PAGE_SIZE']))

@app.route("/category")
def category():
    # get parameters
    _id = int(request.args.get('category_id', 0))

    return render_template('/client/pages/category.html',

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
