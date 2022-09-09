from typing import Iterator
from django import template
from math import ceil

register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def the_range(value, arg):
    return range(value+arg)
    
@register.filter
def select(value, arg):
    return value[arg]

@register.filter
def mult(value, arg):
    return round((value * arg) - ((value * arg)%-100)) #rounds up to the nearest 100