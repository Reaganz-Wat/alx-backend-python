from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status, filters as drf_filters
from django_filters import rest_framework as filters

from .filters import MessageFilter
from .models import User, Conversation, Message
from .permissions import IsConversationParticipant, IsParticipantOfConversation, IsSenderOrReadOnly
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    permission_classes = [IsAuthenticated, IsConversationParticipant]

    def create(self, request, *args, **kwargs):
        # Expect a list of participant IDs in the request
        participant_ids = request.data.get('participant_ids')

        if not participant_ids or not isinstance(participant_ids, list):
            return Response({'error': 'participant_ids must be a list of user UUIDs'},
                            status=status.HTTP_400_BAD_REQUEST)

        print(participant_ids)

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

# class MessageViewSet(viewsets.ModelViewSet):
#     serializer_class = MessageSerializer
#     permission_classes = [
#         IsAuthenticated,
#         IsParticipantOfConversation,
#         IsSenderOrReadOnly,
#     ]
#
#     filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter]
#     filterset_class = MessageFilter
#     ordering_fields = ['sent_at']
#     ordering = ['-sent_at']  # latest first
#
#     def get_queryset(self):
#         return Message.objects.filter(
#             conversation__participants_id=self.request.user.user_id
#         )
#
#     def perform_create(self, serializer):
#         # Automatically assign the sender as the logged-in user
#         serializer.save(sender_id=self.request.user)



class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [
        IsAuthenticated,
        IsParticipantOfConversation,
        IsSenderOrReadOnly,
    ]

    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        if not conversation_id:
            return Message.objects.none()

        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__participants_id=self.request.user.user_id
        )

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation_id')
        if not conversation_id:
            return Response({'error': 'conversation_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if user is a participant
        if not conversation.participants_id.filter(user_id=request.user.user_id).exists():
            return Response({'error': 'You are not a participant in this conversation'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender_id=request.user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer