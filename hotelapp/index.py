from flask import render_template, request, redirect, url_for
from hotelapp import app, utils
from hotelapp.admin import *
from hotelapp import login_manager
from flask_login import current_user, login_user, logout_user

from hotelapp.models import UserRole

# You will need to provide a user_loader callback. 
# This callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader    
def inject_user(user_id):
    return utils.get_user_by_id(user_id=user_id)


# Admin
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
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
    s = "Wellcome to my website"
    room = utils.load_room()
    return render_template('/client/pages/index.html', s=s, room=room)


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
                return redirect(url_for('home'))
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


