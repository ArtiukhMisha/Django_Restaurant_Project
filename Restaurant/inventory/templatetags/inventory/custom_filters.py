from django import template

register = template.Library()


@register.filter
def get_item_by_id(dictionary, key):
    return dictionary.get(int(key))


@register.filter
def show_type(inst):
    return type(inst)
