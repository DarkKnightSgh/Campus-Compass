from django.urls import path
from . import views

urlpatterns = [
    path('<department_id>', views.get_branches, name='get_branches'),
]
