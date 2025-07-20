# from django.urls import path, include
# from rest_framework import routers
#
# from .views import UserViewSet, ConversationViewSet, MessageViewSet
#
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')
# router.register(r'conversations', ConversationViewSet, basename='conversation')
# router.register(r'message', MessageViewSet, basename='message')
#
# urlpatterns = [
#     path('', include(router.urls))
# ]



from django.urls import path, include
from rest_framework_nested import routers

from .views import UserViewSet, ConversationViewSet, MessageViewSet

# 1️⃣ Top-level router
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')

# 2️⃣ Nested router: conversations under users
user_conversations_router = routers.NestedDefaultRouter(router, r'users', lookup='user')
user_conversations_router.register(r'conversations', ConversationViewSet, basename='user-conversations')

# 3️⃣ Nested router: messages under conversations
conversation_messages_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_messages_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# 4️⃣ Combine all routes
urlpatterns = [
    path('', include(router.urls)),
    path('', include(user_conversations_router.urls)),
    path('', include(conversation_messages_router.urls)),
]
