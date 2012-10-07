from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def static_url():
    return getattr(settings, 'STATIC_URL', None)
