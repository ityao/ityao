from django import template

register = template.Library()

@register.simple_tag
def active(path, pattern):
    import re
    if re.search(pattern, path):
        return 'active'
    return ''
