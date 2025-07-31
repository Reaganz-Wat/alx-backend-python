from django.urls import path
from .views import delete_user, show_users, conversation_view, unread_messages_view

urlpatterns = [
    path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
    path('users/', show_users, name='show_users'),
    path('conversations/', conversation_view, name='all_users_conversation'),
    path('unread/', unread_messages_view, name='unread_messages'),
]