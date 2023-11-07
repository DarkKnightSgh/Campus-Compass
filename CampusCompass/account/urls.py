from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns= [
    path('register',views.register,name="register"),
    path('register_submit',views.register_submit,name="register_submit"),
    path('login',views.login,name="login"),
    path('login_submit',views.login_submit,name="login_submit"),
    path('logout',views.logout,name="logout"),

]