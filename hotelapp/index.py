from flask import render_template, request, redirect, url_for
from hotelapp import app, utils



@app.route("/")
def home():
    s = "Wellcome to my website"
    room = utils.load_room()
    return render_template('index.html', s=s, room=room)


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

    return render_template('register.html',
                           error_msg=error_msg)


@app.context_processor
def common_response():
    return {
        'kindofroom': utils.load_kindofroom()
    }


if __name__ == "__main__":
    from hotelapp.admin import *

    app.run(debug=True)
