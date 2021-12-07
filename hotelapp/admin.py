from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from hotelapp import app, db
from hotelapp.models import KindOfRoom, Room

admin = Admin(app=app, name="Hotel website administrator", template_mode="bootstrap4")


class RoomView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_exclude_list = ['image', 'active', 'created_date']
    column_labels = {
        'name': 'Ten SP',
        'description': 'Mo ta',
        'price': 'Gia',
        'image': 'Anh dai dien',
        'kind_id': 'Loai phong'
    }
    column_sortable_list = ['id', 'name', 'price']


admin.add_view(ModelView(KindOfRoom, db.session))
admin.add_view(RoomView(Room, db.session))
