from datetime import datetime
from re import T
from flask import request
from flask_admin import AdminIndexView
from flask_admin.base import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_login.utils import logout_user
from werkzeug.utils import redirect
from wtforms.fields import TextAreaField

from hotelapp import app, db, utils
from hotelapp.models import (Customer, CustomerType, Receipt, Registration, Reservation,
                             Room, RoomType, User, UserRole)


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
    column_exclude_list = ['image', 'created_date']
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
        'kind_id': 'Loai phong',
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


class ReservationView(ModelView):
    column_display_pk = True
    column_filters = ['room_id', 'checkInTime', 'checkOutTime']
    column_list = ('id', 'room_id', 'reserveBy', 'phone', 'checkInTime',
                   'checkOutTime', 'customers')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class RegistrationView(ModelView):
    column_display_pk = True
    column_filters = ['room_id', 'checkInTime', 'checkOutTime']
    column_list = ('id', 'checkInTime', 'checkOutTime', 'room_id', 'customers')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class CustomerView(ModelView):
    column_display_pk = True
    can_view_details = True
    edit_model = True
    details_modal = True
    column_filters = ['name']
    column_searchable_list = ['name']
    column_list = ('id', 'name', 'idCard', 'address', 'reservations')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class ReceiptView(ModelView):
    column_list = ('checkInTime', 'checkOutTime', 'unitPrice',
                   'customer_id', 'reservation_id', 'registration_id', 'surcharges')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class MakeRegistrationView(BaseView):
    @expose('/', methods=['get', 'post'])
    def registration(self):
        rooms = utils.get_rooms()
        customer_types_db = utils.get_customer_type()
        selected_room = ""
        success_msg = ""
        second_post = request.form.get('second_post')
        # Select Room Variables
        selected_room_id = request.form.get('selected_room_id')
        selected_room = utils.get_room_by_id(selected_room_id)


        if request.method == 'POST' and second_post:
            # Surcharge Variables
            customer_foreign_type_db = utils.get_customer_type_by_name("Quốc tế")
            
            # reservation info
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

            # Lập phiếu thuê phòng
            # thuê phòng
            registration_result = utils.registerRoom(customerNames, customerTypes, idCards, addresses, selected_room_id, checkInTime, checkOutTime)
            registration = registration_result[0]
            first_customer = registration_result[1]
            # Tính tiền phòng theo số ngày
            total_amount = selected_room.price * days_diff
            # Tạo hóa đơn
            receipt = utils.create_receipt(checkInTime=checkInTime, checkOutTime=checkOutTime, unitPrice=total_amount,
                                           customer_id=first_customer.id, registration_id=registration.id, room_id=selected_room_id)
            # Chuyển trạng thái phòng sang đã đặt
            utils.set_room_status_by_id(selected_room_id, False)
            # Thêm phụ thu id vào ReceiptSurcharge của hó đơn vừa tạo
            if family_members >= 3:
                utils.create_receipt_surcharge(receipt.id, utils.get_surcharge_by_id(1).id)
            if [customer_type_id for customer_type_id in customerTypes if str(customer_type_id).__eq__(str(customer_foreign_type_db.id))]:
                utils.create_receipt_surcharge(receipt.id, utils.get_surcharge_by_id(2).id)

            success_msg = "Register succesfully"
           


        return self.render(
            'admin/pages/registration.html'
            , rooms=rooms
            , selected_room=selected_room
            , customer_types_db=customer_types_db
            , success_msg=success_msg
        )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


# receipt payment
class ReceiptPaymentView(BaseView):
    @expose('/', methods=['get', 'post'])
    def ReceiptPayment(self):
        receipts = utils.get_receipts()
        selected_receipt = ""
        customer_name = ""
        room_id = 0
        total_amount = 0
        second_post = request.form.get('second_post')
        # Select receipt Variables
        selected_receipt_id = request.form.get('selected_receipt_id')
        

        if request.method == 'POST':
            print("selected_receipt_id")
            print(selected_receipt_id)
            filter_result = utils.get_receipt_by_id(selected_receipt_id)
            print(filter_result)
            selected_receipt = filter_result[0]
            registration = filter_result[1]
            customer = filter_result[2]
            customer_name = customer.name
            room_id = registration.room_id
            total_amount = selected_receipt.unitPrice

            # results = utils.get_receipt_surcharges(selected_receipt.id)
       
            # if results:
            #     for result in results:
            #         total_amount = total_amount * result.Surcharge.ratio
            

        return self.render(
            'admin/pages/receipt_payment.html'
            , receipts=receipts
            , selected_receipt=selected_receipt
            , customer_name=customer_name
            , room_id=room_id
            , total_amount=total_amount
        )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN



class RevenueStatsView(BaseView):
    @expose('/')
    def ProductsStats(self):
        month           = request.args.get('month')
        # tất cả receipt cả phụ thu (lọc theo tháng)
        receipts = utils.get_receipts_by_month(month)
                
        return self.render(
            'admin/pages/revenueStats.html',
            month=month,
            receipts=receipts
        )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

admin = Admin(app, name='Admin', template_mode='bootstrap4', index_view=AdminHomeView())

# Stats View
admin.add_view(RevenueStatsView(name='Revenue Stats'))
# Custom View
admin.add_view(MakeRegistrationView(name='Make Registration'))
# Default View
admin.add_view(RegistrationView(Registration, db.session))
admin.add_view(RoomView(Room, db.session))
admin.add_view(ReservationView(Reservation, db.session))
admin.add_view(CustomerView(Customer, db.session))
admin.add_view(ReceiptPaymentView(name='Receipt Payment'))
admin.add_view(ReceiptView(Receipt, db.session))
admin.add_view(AdminAutheticatedView(User, db.session))
admin.add_view(AdminAutheticatedView(RoomType, db.session))
admin.add_view(AdminAutheticatedView(CustomerType, db.session))
admin.add_view(LogoutView(name="Log out"))
