from django import template
from django.utils.safestring import mark_safe

from web369.models import SearchQuery


register = template.Library()


@register.filter
def highlight(text, query):
    if not isinstance(query, SearchQuery):
        query = SearchQuery(query)
    return mark_safe( query.highlight(text) )
