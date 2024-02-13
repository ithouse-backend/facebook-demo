from django import template
from datetime import timedelta

register = template.Library()


@register.filter(name="time_display")
def time_display(value):
    if not isinstance(value, timedelta):
        return value

    days = value.days
    hours, remainder = divmod(value.seconds, 3600)

    if days > 0:
        return f"{days}d"
    elif hours > 0:
        return f"{hours}h"
    else:
        return "Just now"
