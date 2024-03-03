from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import json

from .models import Chat, ChatGroup


def chat_page(request):
    users_group = ChatGroup.objects.filter(users=request.user)
    is_sender = False

    # Iterate over each group
    for group in users_group:
        # Get the first chat associated with the group
        first_chat_in_group = group.chat_set.first()
        if first_chat_in_group:
            # Check if the sender of the chat is the current user
            if first_chat_in_group.sender == request.user:
                is_sender = True
        else:
            # Handle case where the group has no chats
            is_sender = False
    context = {
        "chats": users_group,
        "is_sender": is_sender,
    }
    return render(request, 'chat/chat.html', context)


def get_chats(request):
    group_id = request.GET.get("group_id")
    sender_lastname = None
    sender_firstname = None
    user = Chat.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user),
        group_id=group_id,
    ).exclude(
        sender=request.user,
        receiver=request.user
    ).first()
    if user.sender.id == request.user.id:
        sender_firstname = user.receiver.firstname
        sender_lastname = user.receiver.lastname
        sender_profile_avatar = user.receiver.profile.avatar.url
        sender_unique_id = user.receiver.unique_id

        chats = Chat.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user),
            group_id=group_id,
        ).exclude(
            sender=request.user,
            receiver=request.user
        )
        chat_data = [{
            'sender_id': chat.sender.id,
            'receiver': chat.receiver.id,
            'sender': chat.sender.firstname,
            'receiver': chat.receiver.firstname,
            'text': chat.text,
            'created_at': chat.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for chat in chats]
        context = {
            "data": chat_data,
            "sender_firstname": sender_firstname,
            "sender_lastname": sender_lastname,
            "sender_profile_avatar": sender_profile_avatar,
            "sender_unique_id": sender_unique_id
        }
        return JsonResponse(context, safe=False)
    else:
        sender_firstname = user.sender.firstname
        sender_lastname = user.sender.lastname
        sender_profile_avatar = user.sender.profile.avatar.url
        sender_unique_id = user.sender.unique_id

        chats = Chat.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user),
            group_id=group_id,
        ).exclude(
            sender=request.user,
            receiver=request.user
        )
        chat_data = [{
            'sender_id': chat.sender.id,
            'receiver': chat.receiver.id,
            'sender': chat.sender.firstname,
            'receiver': chat.receiver.firstname,
            'text': chat.text,
            'created_at': chat.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for chat in chats]
        context = {
            "data": chat_data,
            "sender_firstname": sender_firstname,
            "sender_lastname": sender_lastname,
            "sender_profile_avatar": sender_profile_avatar,
            "sender_unique_id": sender_unique_id
        }
        return JsonResponse(context, safe=False)


def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        text = request.POST.get('text')

        try:
            # Create a new chat message
            Chat.objects.create(sender=request.user,
                                receiver_id=receiver_id, text=text)
            return JsonResponse({'success': 'Message sent successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
