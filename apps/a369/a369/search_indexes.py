from haystack import indexes
from haystack import site

from .models import Documents


class DocumentsIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    i= indexes.IntegerField(model_attr='id')
    sourc = indexes.CharField(model_attr='source',)
    source_typ = indexes.CharField(model_attr='source_type',)
    date_birt = indexes.DateTimeField(model_attr='date_birth',)

site.register(Documents, DocumentsIndex)
