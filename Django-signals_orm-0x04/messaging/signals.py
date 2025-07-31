from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def create_history_on_message_update(sender, instance: Message, **kwargs):
    if not instance.pk:
        # This is a new message (not yet in the DB) -> Skip it
        return

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return # this is for the safety

    if instance.content != old_instance.content:
        MessageHistory.objects.create(
            message=old_instance,
            previous_content=old_instance.content,
            edited_by=instance.edited_by
        )

        instance.edited = True

@receiver(post_delete, sender=User)
def delete_user_details(sender, instance: User, **kwargs):

    # deletes the notifications
    Notification.objects.filter(user=instance).delete()

    # deletes the messages
    Message.objects.filter(sender=instance).delete()

    # deletes the message history
    MessageHistory.objects.filter(message__sender=instance).delete()

    print(f'.....................FINISHED DELETING EVERYTHING..................')