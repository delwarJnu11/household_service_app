from django import template

register = template.Library()

@register.filter
def stars(value):
    full_stars = int(value)
    remaining = value - full_stars

    if remaining >= 0.75:
        return '⭐' * (full_stars + 1)
    elif remaining >= 0.25:
        return '⭐' * full_stars + '☆'
    else:
        return '⭐' * full_stars