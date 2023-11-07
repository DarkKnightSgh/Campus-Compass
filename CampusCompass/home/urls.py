from django.urls import path
from . import views

urlpatterns= [
    path('', views.home,name= 'home'),
    path('privacy-policy',views.privacypolicy,name="privacypolicy"),
    path('contact-us',views.contact_us,name="contactus"),
    path('about-us',views.about_us,name="aboutus"),
    path('contact-success',views.contact_success,name="contactsuccess"),
    path('copyright',views.copyright,name="copyright"),
    path('error404',views.error_404,name="error404"),

]