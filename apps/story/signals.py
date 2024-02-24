from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Story


@receiver(post_save, sender=Story)
def check_and_delete_expired_stories(sender, instance, created, **kwargs):
    if created:
        if instance.is_expired():
            try:
                instance.delete()
            except Exception as e:
                print(f"Error deleting expired story: {e}")
