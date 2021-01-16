from django import template
register=template.Library()


@register.filter(name='get_reps')
def get_reps(dic,key):
    return dic.get(key)