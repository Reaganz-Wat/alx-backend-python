# chats/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSenderOrReadOnly(BasePermission):
    """
    Only allow the sender of a message to view/edit/delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender_id == request.user


class IsConversationParticipant(BasePermission):
    """
    Only allow participants of a conversation to view or interact with it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants_id.all()
