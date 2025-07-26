# chats/permissions.py

from rest_framework import permissions

from chats.models import Conversation


class IsSenderOrReadOnly(permissions.BasePermission):
    """
    Only allow the sender of a message to view/edit/delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender_id == request.user


class IsConversationParticipant(permissions.BasePermission):
    """
    Only allow participants of a conversation to view or interact with it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants_id.all()


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows only authenticated users who are participants of a conversation.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if view.basename == "message" and request.method in ['GET', 'POST']:
            conversation_id = (
                request.data.get("conversation_id") or
                request.query_params.get("conversation_id")
            )
            if not conversation_id:
                return False

            try:
                conversation = Conversation.objects.get(conversation_id=conversation_id)
                return request.user in conversation.participants_id.all()
            except Conversation.DoesNotExist:
                return False

        return True

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user not in obj.conversation.participants_id.all():
            return False

        # Restrict certain methods to only sender
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.sender_id == request.user

        return True