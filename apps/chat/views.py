from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import json

from .models import Chat, ChatGroup


def chat_page(request):
    users_group = ChatGroup.objects.filter(users=request.user)
    chats = Chat.objects.filter(group__in=users_group)
    is_sender = [chat.sender == request.user for chat in chats]

    context = {
        "chats": zip(is_sender, chats)
    }
    return render(request, 'chat/chat.html', context)


def get_chats(request):
    chat = Chat.objects.filter(
        Q(sender=request.user) | 
        Q(receiver=request.user)
    ).exclude(
        sender=request.user,
        receiver=request.user
    )
    serialized_chats_loads = serializers.serialize('json', chat)
    context = {
        "data": serialized_chats_loads
    }
    return JsonResponse(context, safe=False)

def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        text = request.POST.get('text')
        
        try:
            # Create a new chat message
            Chat.objects.create(sender=request.user, receiver_id=receiver_id, text=text)
            return JsonResponse({'success': 'Message sent successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
