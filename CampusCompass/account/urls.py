from django.urls import path
from . import views
from .views import ActivateAccount
from django.contrib.auth import views as auth_views



urlpatterns= [
    # authentication
    path('register',views.register,name="register"),
    path('register_submit',views.register_submit,name="register_submit"),
    path('login',views.login,name="login"),
    path('login_submit',views.login_submit,name="login_submit"),
    path('logout',views.logout,name="logout"),

    # email confirmation and auth
    path('confirm_email',views.confirm_email,name="email_confirm"),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

]