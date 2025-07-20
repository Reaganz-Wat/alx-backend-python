from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        # Expect a list of participant IDs in the request
        participant_ids = request.data.get('participant_ids')

        if not participant_ids or not isinstance(participant_ids, list):
            return Response({'error': 'participant_ids must be a list of user UUIDs'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Fetch users
        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response({'error': 'One or more user IDs are invalid'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create conversation
        conversation = Conversation.objects.create()
        conversation.participants_id.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        # Expect: conversation_id, sender_id, message_body
        conversation_id = request.data.get('conversation_id')
        sender_id = request.data.get('sender_id')
        message_body = request.data.get('message_body')

        if not all([conversation_id, sender_id, message_body]):
            return Response({'error': 'conversation_id, sender_id, and message_body are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            sender = User.objects.get(user_id=sender_id)
        except (Conversation.DoesNotExist, User.DoesNotExist):
            return Response({'error': 'Invalid conversation or sender ID'},
                            status=status.HTTP_404_NOT_FOUND)

        # Ensure sender is a participant
        if sender not in conversation.participants_id.all():
            return Response({'error': 'Sender is not a participant in the conversation'},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            conversation=conversation,
            sender_id=sender,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)