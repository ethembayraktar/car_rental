import logging

from django import template
import os, json
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='filename')
def filename(value):
    return os.path.basename(value.name)


@register.filter(name='my_float')
def my_float(value):
    try:
        return str(round(value, 2)).replace(",", ".")
    except Exception as e:
        return str(value).replace(",", ".")


@register.filter(name='lastname')
def lastname(value):
    """
    Returns the first character of lastname in lowercase for a given name
    """
    if value:
        return value[:2].upper()  # get the first letter of last name in lower case
    else:
        return "A"


@register.filter(name='name')
def name(created_by):
    """
    Returns the first character of lastname in lowercase for a given name
    """
    try:
        if created_by:
            return f"{created_by.first_name} {created_by.last_name.upper()}"
    except Exception as e:
        logging.exception(e)

    return "Consensus HUKUK"


@register.filter(name='js', is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))


@register.filter()
def my_range(n):
    return range(1, n + 1)


@register.filter()
def tckn_mask(tckn):
    if tckn is None or len(tckn) != 11:
        return tckn
    return tckn[:2] + "********" + tckn[-1]


@register.filter()
def vkn_mask(vkn):
    if vkn is None or len(vkn) != 10:
        return vkn
    return vkn[:2] + "*******" + vkn[-1]


@register.filter()
def phone_mask(phone):
    return phone[:3] + "*" * (len(phone) - 5) + phone[-2:]


@register.filter()
def email_mask(email):
    first_part = email.split("@")[0]
    second_part = email.split("@")[1]
    return first_part[:3] + "*" * (len(first_part) - 3) + "@" + second_part[:2] + "*" * (len(second_part) - 2)
