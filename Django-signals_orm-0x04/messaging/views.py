from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('show_users')

def show_users(request):
    users = User.objects.all()
    return render(request, 'users.html', context={'users': users})