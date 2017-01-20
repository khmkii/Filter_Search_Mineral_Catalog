from django import template
from django.template.defaultfilters import stringfilter

import string


register = template.Library()


@register.inclusion_tag('minerals/letter_nav.html')
def letters_for_nav():
    letters = string.ascii_uppercase
    return {'letters': letters}


@register.inclusion_tag('minerals/group_nav.html')
def groups_nav():
    group_names = [
        'silicates', 'oxides', 'sulfates', 'sulfides', 'carbonates', 'halides', 'sulfosalts',
        'phosphates', 'borates', 'organic minerals', 'arsenates', 'native elements', 'other'
    ]
    return {'group_names': group_names}


@register.inclusion_tag('minerals/streak_nav.html')
def streak_nav():
    streak_names = [
        'red', 'yellow', 'pink', 'green', 'black', 'white', 'orange', 'grey',
        'purple', 'blue',
    ]
    return {'streak_names': streak_names}


@register.filter(name='pretty_output')
@stringfilter
def pretty_output(toRender):
    if '_' in toRender:
        list_1 = [word.title() for word in toRender.split('_')]
        return ' '.join(list_1)
    else:
        return toRender.title()

