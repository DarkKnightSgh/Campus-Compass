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
    path('profile',views.profile,name="profile"),
    path('edit_profile',views.edit_profile,name="edit_profile"),
    path('edit_profile_submit',views.edit_profile_submit,name="edit_profile_submit"),

    # email confirmation and auth
    path('confirm_email',views.confirm_email,name="email_confirm"),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

    # mentor
    path('mentor_registration',views.mentor_registration,name='mentor_registration'),

    # forgot / change password
    # Change Password
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='account/change-password.html',
            success_url = '/account/login'
            ) ,  name='change_password'),
    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='account/password-reset.html',
             subject_template_name='account/password_reset_subject.txt',
             email_template_name='account/password_reset_email.html',
            #  success_url='login'
         ),
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='account/password-reset-done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password_reset_complete.html'
         ),
         name='password_reset_complete'),



]