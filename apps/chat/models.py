from django.db import models
from apps.authentication.models import User


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_receiver')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return "%s %sga habar yubordi" % (self.sender.firstname, self.receiver.firstname)
    
    class Meta:
        unique_together = ['sender', 'receiver']

