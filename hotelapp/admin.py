from flask_admin import AdminIndexView
from flask_admin.base import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView, view
from flask_login import current_user
from flask_login.utils import logout_user
from werkzeug.utils import redirect
from wtforms.fields import TextAreaField

from hotelapp import app, db, utils
from hotelapp.models import RoomType, Room, User, UserRole


# Admin View
class AdminHomeView(AdminIndexView):
    @expose('/')
    def home(self):
        kind_stats = utils.kind_stats()
        return self.render(
            'admin/pages/index.html', 
            kind_stats=kind_stats, msg="Hello"
        )


class RoomView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_exclude_list = ['image', 'active', 'created_date']
    form_overrides = dict(description=TextAreaField)
    form_widget_args = {
        'description': {
            'rows': 5
        }
    }
    column_labels = {
        'name': 'Ten SP',
        'description': 'Mo ta',
        'price': 'Gia',
        'image': 'Anh dai dien',
        'kind_id': 'Loai phong'
    }
    column_sortable_list = ['id', 'name', 'price']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


# kiểm tra admin
class AdminAutheticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


admin = Admin(app, name='Hotel website administrator', template_mode='bootstrap4', index_view=AdminHomeView())

admin.add_view(AdminAutheticatedView(RoomType, db.session))
admin.add_view(RoomView(Room, db.session))
admin.add_view(AdminAutheticatedView(User, db.session))
admin.add_view(LogoutView(name="Log out"))
