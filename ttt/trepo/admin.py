from datetime import datetime

from django.contrib import admin

from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.forms import FlatpageForm

from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from dal import autocomplete

import tagulous.admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from .models import Pub, Tag, CompanyTag, PubTopic, PubCollection, CustomFlatPage
from .forms import PubForm

tagulous.admin.register(Tag)
tagulous.admin.register(CompanyTag)

class TrepoAdminMixin(object):
    class Media:
        css = {
            'all': ('css/trepoadmin.css',),
        }


# taken from https://medium.com/@hakibenita/how-to-add-a-text-filter-to-django-admin-5d1db93772d8

class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice

class TagFilter(InputFilter):
    parameter_name = 'tags'
    title = 'Tag'
 
    def queryset(self, request, queryset):
        if self.value() is not None:
            tags = self.value()

            return queryset.filter(
#                 tags__name__icontains=tags
                Q(tags__name__icontains=tags) |
                Q(companytags__name__icontains=tags)
            ).distinct()


class PubAdmin(admin.ModelAdmin, TrepoAdminMixin):
    form = PubForm
    list_display = ["id", "title", "publication", "publishers", "authors", "date_as_string", "status"]
    list_display_links = ('title',)
    list_filter = ["status", TagFilter]
    search_fields = ["title", "authors", "publishers", "publication","tags__name","companytags__name"]
    prepopulated_fields = {"slug": ["title"]}
    ordering = ('id',)

    readonly_fields = ('created_by',)

    filter_horizontal = ('relatedpubs',)

    fieldsets = [
        (None, {'fields': ['title','slug','status','pubtype','background','date_as_string']}),
        (None, {'fields': ['description','authors','publishers','publication']}),
        (None, {'fields': ['tags','companytags']}),
        (None, {'fields': ['url','url_dl','url_dl_preprint','url_archive_org','url_archive_is','doi','isbn','issn']}),
        ('Related publications', {'fields': ['relatedpubs'], 'classes': ['collapse']}),
        ('Is related to publication', {'fields': ['is_related_to'], 'classes': ['collapse']}),
    ]


    def save_model(self, request, obj, form, change):

        if not obj.created_by:
            obj.created_by = request.user

        obj.date = datetime.strptime(form.cleaned_data.get('date_as_string_full'),'%Y/%m/%d')

        super().save_model(request, obj, form, change)

admin.site.register(Pub, PubAdmin)

class PubCollectionInline(SortableInlineAdminMixin, admin.StackedInline):
    model = PubCollection
    extra = 1

class PubTopicAdmin(DraggableMPTTAdmin, TrepoAdminMixin):
    list_display = ('tree_actions', 'indented_title','status')
    list_display_links = ('indented_title',)
    prepopulated_fields = {"slug": ["title"]}
    mptt_level_indent = 30
    inlines = (PubCollectionInline,)

admin.site.register(PubTopic, PubTopicAdmin)

# custom flatpages admin

class CustomFlatPageAdmin(admin.ModelAdmin):
    form = FlatpageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'description', 'content',)}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('registration_required', 'template_name'),
        }),
    )
    list_display = ('url', 'title')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.sites.set([1])

admin.site.register(CustomFlatPage, CustomFlatPageAdmin)
admin.site.unregister(FlatPage)

# remove sites framework admin
from django.contrib.sites.models import Site
admin.site.unregister(Site)