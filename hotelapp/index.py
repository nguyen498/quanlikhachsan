from flask import render_template
from hotelapp import app
import ultis


@app.route("/")
def home():
    s = "Wellcome to my website"
    room = ultis.load_room()
    kindofroom = ultis.load_kindofroom()
    return render_template('index.html', s=s, room=room,
                           kindofroom=kindofroom)


if __name__ == "__main__":
    from hotelapp.admin import *

    app.run(debug=True)
