from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ConversationSerializer(serializers.ModelSerializer):

    participants_id = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants_id',
            'created_at',
            'messages',
        ]

class MessageSerializer(serializers.ModelSerializer):

    sender_id = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender_id',
            'conversation',
            'message_body',
            'sent_at'
        ]