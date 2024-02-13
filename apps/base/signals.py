from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import File

from PIL import Image

@receiver(post_save, sender=File)
def process_image(sender, instance, **kwargs):
    try:
        image = Image.open(instance.file.path)
        width, height = image.size
        instance.width = width
        instance.height = height
        instance.save()
    except Exception as e:
        print(f"Error opening image: {e}")