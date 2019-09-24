from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_path(context):
    path = context["request"].META.get('HTTP_REFERER')
    if path is None:
        path = context["request"].GET.get("next")
    return path
