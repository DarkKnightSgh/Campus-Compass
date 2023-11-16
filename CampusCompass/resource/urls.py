from django.urls import path
from . import views

urlpatterns= [
    path('',views.resource,name="resource"),    
    path('upload', views.upload_resource, name='upload_resource'),
    path('tag/<tag>', views.resource_by_tag, name='search'),

]