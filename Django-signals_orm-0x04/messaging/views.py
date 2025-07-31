from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from .models import Message

User = get_user_model()

# Create your views here.
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('show_users')

def show_users(request):
    users = User.objects.all()
    return render(request, 'users.html', context={'users': users})

@login_required
def conversation_view(request):
    top_level_messages = Message.objects.filter(
        parent_message__isnull=True,
        sender=request.user
    ).select_related('sender', 'receiver') \
     .prefetch_related(
         Prefetch('replies', queryset=Message.objects.select_related('sender'))
     )

    return render(request, 'conversation.html', {'messages': top_level_messages})

def get_all_replies(message):
    replies = []
    for reply in message.replies.all():
        replies.append(reply)
        replies.extend(get_all_replies(reply))  # recursive depth-first
    return replies

@login_required
def unread_messages_view(request):
    unread_messages = Message.unread.for_user(request.user)
    return render(request, 'unread_inbox.html', {'messages': unread_messages})
