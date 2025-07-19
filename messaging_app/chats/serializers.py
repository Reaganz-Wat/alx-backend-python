# serializers.py

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone_number',
            'role',
            'password',
            'created_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'user_id': {'read_only': True},
            'created_at': {'read_only': True}
        }

    def get_full_name(self, obj):
        """Return the user's full name"""
        return f"{obj.first_name} {obj.last_name}".strip()

    def validate_email(self, value):
        """Validate email uniqueness"""
        if User.objects.filter(email=value).exists():
            if not self.instance or self.instance.email != value:
                raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_phone_number(self, value):
        """Validate phone number format"""
        if value and not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only numbers, spaces, hyphens, and plus signs.")
        return value

    def create(self, validated_data):
        """Create user with hashed password"""
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    sender_id = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender_id',
            'sender_name',
            'conversation',
            'message_body',
            'sent_at'
        ]
        extra_kwargs = {
            'message_id': {'read_only': True},
            'sent_at': {'read_only': True}
        }

    def get_sender_name(self, obj):
        """Return sender's full name"""
        return f"{obj.sender_id.first_name} {obj.sender_id.last_name}".strip()

    def validate_message_body(self, value):
        """Validate message body is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value.strip()


class ConversationSerializer(serializers.ModelSerializer):
    participants_id = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participants_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants_id',
            'participants_count',
            'messages',
            'last_message',
            'created_at'
        ]
        extra_kwargs = {
            'conversation_id': {'read_only': True},
            'created_at': {'read_only': True}
        }

    def get_participants_count(self, obj):
        """Return the number of participants in the conversation"""
        return obj.participants_id.count()

    def get_last_message(self, obj):
        """Return the last message in the conversation"""
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return {
                'message_body': last_message.message_body,
                'sender_name': f"{last_message.sender_id.first_name} {last_message.sender_id.last_name}".strip(),
                'sent_at': last_message.sent_at
            }
        return None

    def validate(self, data):
        """Validate conversation data"""
        # Add any conversation-level validation here
        return data


# Additional serializer for creating conversations with participants
class ConversationCreateSerializer(serializers.ModelSerializer):
    participants_emails = serializers.CharField(write_only=True, help_text="Comma-separated list of participant emails")

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_emails', 'created_at']
        extra_kwargs = {
            'conversation_id': {'read_only': True},
            'created_at': {'read_only': True}
        }

    def validate_participants_emails(self, value):
        """Validate participant emails"""
        if not value:
            raise serializers.ValidationError("At least one participant email is required.")

        emails = [email.strip() for email in value.split(',')]
        if len(emails) < 1:
            raise serializers.ValidationError("At least one participant is required.")

        # Check if all emails exist in the system
        for email in emails:
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError(f"User with email '{email}' does not exist.")

        return emails

    def create(self, validated_data):
        """Create conversation with participants"""
        emails = validated_data.pop('participants_emails')
        conversation = Conversation.objects.create()

        # Add participants
        for email in emails:
            user = User.objects.get(email=email)
            conversation.participants_id.add(user)

        return conversation