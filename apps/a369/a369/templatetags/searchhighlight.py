import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def highlight(text, word):
    c = re.compile('(%s)' % re.escape(word), re.I)
    text = c.sub(r'<span class="comment-term">\1</span>', text)
    return mark_safe(text)
