from django.urls import path
from .views import delete_user, show_users

urlpatterns = [
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('users/', show_users, name='show_users')
]