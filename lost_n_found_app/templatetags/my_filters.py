from django import template
from lost_n_found_app.models import *

register = template.Library()

# ITEMS FILTER
@register.filter()
def missing(value):
    return value.filter(found=False)


@register.filter()
def found(value):
    return value.filter(found=True)


@register.filter()
def at_campus(value, campus):
    return value.filter(campus=campus)


@register.filter()
def exclude_user(value, user_id):
    return value.exclude(id=user_id)


@register.filter()
def mine(value, user):
    return value.filter(owner=user)
