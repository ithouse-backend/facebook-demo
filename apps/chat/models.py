from django.db import models
from apps.authentication.models import User


class ChatGroup(models.Model):
    users = models.ManyToManyField(User)
    created_ad = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "".join([user.firstname for user in self.users.all()])


class Chat(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='chat_sender')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='chat_receiver')
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "%s %sga habar yubordi" % (self.sender.firstname, self.receiver.firstname)
