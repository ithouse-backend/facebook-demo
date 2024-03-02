from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_page, name="chat_home"),
    path("get-chats/", views.get_chats, name='get_chats'),
    path("send-message/", views.send_message, name='send_message')
]