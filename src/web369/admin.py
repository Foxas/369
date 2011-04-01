from django.contrib import admin
from models import BaseWord


def action_merge_words(modeladmin, request, queryset):
    BaseWord.objects.merge(queryset)
action_merge_words.short_description = "Merge selected words"


class BaseWordAdmin(admin.ModelAdmin):
    search_fields = ['word', ]
    list_filter = ['stop_word', ]
    list_display_links = ('derivatives_display', )
    list_display = ['word', 'count', 'derivatives_display', 'stop_word']
    list_editable = ['word', 'stop_word']
    actions = [action_merge_words]

    def __init__(self, *args, **kwargs):
        super(BaseWordAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )


admin.site.register(BaseWord, BaseWordAdmin)
