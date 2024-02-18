from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Story


@receiver(post_save, sender=Story)
def check_and_delete_expired_stories(sender, instance, created, **kwargs):
    """
    Auto o'chiradi agar is_expired true bo'lsa va is_expired modelsda yozilgan
    """
    if created:  # Only check for expiration on newly created stories
        if instance.is_expired():
            instance.delete()
