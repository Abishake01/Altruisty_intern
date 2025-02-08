import base64
from django import template

register = template.Library()

@register.filter(name='to_base64')
def to_base64(binary_data):
    """Convert binary data to a Base64-encoded string."""
    if binary_data:
        return base64.b64encode(binary_data).decode('utf-8')
    return ''
