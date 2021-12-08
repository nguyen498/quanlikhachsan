from flask_admin import Admin, AdminIndexView
from flask_admin.base import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_login.utils import logout_user
from werkzeug.utils import redirect

from hotelapp import app, db, utils
from hotelapp.models import KindOfRoom, Room, User, UserRole


class AdminHomeView(AdminIndexView):
    @expose('/')
    def home(self):
        # cate_stats = utils.cate_stats2()
        return self.render(
            'admin/pages/index.html', 
            # cate_stats=cate_stats
        )


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

admin.add_view(AdminAutheticatedView(KindOfRoom, db.session))
admin.add_view(RoomView(Room, db.session))
admin.add_view(AdminAutheticatedView(User, db.session))
admin.add_view(LogoutView(name="Log out"))
