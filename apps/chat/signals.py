from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Chat, ChatGroup
from django.db.models.aggregates import Count

@receiver(post_save, sender=Chat)
def create_or_get_group(sender, instance, created, **kwargs):
    """
    Signal handler to create a group if it doesn't exist, or get an existing group
    when a new chat is created.
    """
    if created:
        group_users = [instance.sender, instance.receiver]
        existing_group = ChatGroup.objects.filter(users__in=group_users).annotate(
            user_count=Count('users')
        ).filter(user_count=len(group_users))

        if not existing_group.exists():
            # If no group exists, create a new one
            group = ChatGroup.objects.create()
            group.users.add(*group_users)
        else:
            # If a group exists, use the first one found
            group = existing_group.first()

        # Assign the group to the chat
        instance.group = group
        instance.save()
