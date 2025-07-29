from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

# Create your tests here.
class SignalTest(TestCase):
    def test_notification_craeted_on_message(self):
        sender = User.objects.create_user(
            username='alice', password='alice'
        )

        receiver = User.objects.create_user(
            username='bob', password='bob'
        )

        message = Message.objects.create(sender=sender, receiver=receiver, content='Hello bob, this is alice')

        self.assertEqual(Notification.objects.count(), 1, 'Created one user already')

        notification = Notification.objects.first()

        self.assertEqual(notification.user, receiver)
        self.assertEqual(notification.message, message)