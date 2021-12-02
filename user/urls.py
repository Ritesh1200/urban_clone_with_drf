from django.urls import path , include
from user import views
from user.view.login import Login
from user.view.registration import Register
from user.view.logout import Logout
from user.view.forget_password import Verify
from user.view.forget_password import Forget_password
from user.view.forget_password import Reset_password
from user.view.service import Category
from user.view.service import Service
from user.view.cart import Addcart
from user.view.cart import Cart
from user.view.order import Order
from user.view.order import Add_order
from user.view.cart import Remove
from user.view.employee import Add_emp
from user.view.profile import Userprofile
from user.view.update import Update

urlpatterns = [
    path('' , views.Home.as_view() , name = 'user'),
    path('login' , Login.as_view() , name = 'login'),
    path('register' , Register.as_view() , name = 'register'),
    path('logout' , Logout.as_view() , name = 'logout'),
    path('verify/<auth_token>' , Verify.as_view() , name = 'verify'),
    path('forget_password' , Forget_password.as_view() , name = 'forget_password'),
    path('reset_password/<auth_token>' , Reset_password.as_view() , name = 'reset_password'),
    path('category/<int:pk>' , Category.as_view() , name = 'category'),
    path('service/<int:servicepk>/<int:categorypk>' , Service.as_view() , name = 'service'),
    path('service/<int:servicepk>' , Service.as_view() , name = 'service'),
    path('addcart/<int:emp_pk>' , Addcart.as_view() , name = 'addcart'),
    path('cart' , Cart.as_view() , name = 'cart'),
    path('order' , Order.as_view() , name = 'order'),
    path('Add_order/<int:cart_pk>' , Add_order.as_view() , name = 'add_order'),
    path('remove/<int:order_pk>' , Remove.as_view() , name = 'remove'),
    path('add_emp/<int:servicepk>/<int:categorypk>' , Add_emp.as_view() , name = 'add_emp'),
    path('add_emp/<int:servicepk>' , Add_emp.as_view() , name = 'add_emp'),
    path('profile' , Userprofile.as_view() , name = 'profile'),
    path('update' , Update.as_view() , name = 'update'),
    
]