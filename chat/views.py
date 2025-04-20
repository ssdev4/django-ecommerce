from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Message

User = get_user_model()

@login_required
def chat_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/chat_list.html', {'users': users})

@login_required
def chat_detail(request, username):
    other_user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            return redirect('chat:chat_detail', username=other_user.username)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    return render(request, 'chat/chat_detail.html', {
        'other_user': other_user,
        'messages': messages
    })
