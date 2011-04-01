from django import template
from django.utils.safestring import mark_safe

from web369.utils.strings import highlight_query


register = template.Library()


@register.filter
def highlight(text, query):
    text = highlight_query(text, query,
                           '<span class="comment-term">%s</span>')
    return mark_safe(text)
