from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models import Count

from django.contrib.flatpages.models import FlatPage
from tagulous import models as TagulousModels
from mptt.models import MPTTModel, TreeForeignKey

from .constants import PUB_TYPES, PUB_BACKGROUNDS, STATUS_CHOICES

# tagulous models

class Tag(TagulousModels.TagModel):
    class TagMeta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        force_lowercase = False
        space_delimiter = False

class CompanyTag(TagulousModels.TagModel):
    class TagMeta:
        verbose_name = 'Company Tag'
        verbose_name_plural = 'Company Tags'
        force_lowercase = False
        space_delimiter = False

# publication model

class Pub(models.Model):

    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        ordering = ['-date']

    DATE_DEFAULT = '1970/01/01'

    # metadata fields

    slug = models.SlugField(unique=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='pubs',
        blank=True,
        null=True,
    )

    creation_date = models.DateTimeField('Created',
        auto_now_add = True,
        editable = False,
    )

    modified_date = models.DateTimeField('Modified',
        auto_now = True,
        editable = False
    )

    status = models.CharField('Status',
        max_length = 10,
        blank = False,
        default = 'draft',
        choices = STATUS_CHOICES)

    # categories and tags

    pubtype = models.CharField('Publication Type',
        max_length = 20,
        blank = False,
        default = 'journalArticle',
        choices = PUB_TYPES)

    background = models.CharField('Background',
        max_length = 20,
        blank = False,
        default = 'other',
        choices = PUB_BACKGROUNDS)

    tags = TagulousModels.TagField(to=Tag,help_text='&nbsp;',blank=True)

    companytags = TagulousModels.TagField(to=CompanyTag,help_text='&nbsp;',blank=True)

    # related publications (m2m relation to self)

    relatedpubs = models.ManyToManyField('self',
        symmetrical=False,
        blank = True,
        related_name='is_related_to',
        verbose_name='publication(s)')

    # main fields

    title = models.CharField('Title',max_length=255,blank=False)

    description = models.TextField('Description',
        blank = True
    )

    authors = models.CharField('Author(s)',
        max_length = 255,
        blank = True,
        help_text = u'One or more authors, format e.g. Firstname Lastname, Firstname Middlename Lastname,...')

    publishers = models.CharField('Publisher or Institution(s)',
        max_length = 255,
        blank = True,
        help_text = u'One or more publishers, comma-separated, e.g. book publisher, institution, company, government agency,...')

    publication = models.CharField('Publication Name',
        max_length = 255,
        blank = True,
        help_text = u'Title of journal, magazine, news outlet, ')

    date_as_string = models.CharField('Publication Date',
        max_length = 10,
        default = DATE_DEFAULT,
        help_text = u'Format: either YYYY or YYYY/MM or YYYY/MM/DD')

    date = models.DateField(
        blank = True,
        default=datetime.strptime(DATE_DEFAULT,'%Y/%m/%d'),
        editable = False)

    url = models.URLField('URL', max_length=2000, blank=True)

    url_dl = models.URLField('URL Download', max_length=2000, blank=True)

    url_dl_preprint = models.URLField('URL Download (preprint)', max_length=2000, blank=True)

    url_archive_org = models.URLField('URL archive.org', max_length=2000, blank=True)

    url_archive_is = models.URLField('URL archive.is', max_length=2000, blank=True)

    doi = models.CharField('DOI', max_length=255, blank=True)

    isbn = models.CharField('ISBN', max_length=20, blank=True) #13

    issn = models.CharField('ISBN', max_length=10, blank=True) #8

    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)

        # list of authors
        self.authors_list = [author.strip() for author in self.authors.split(',')]

        # tests if title already ends with a punctuation mark
        self.title_ends_with_punct = self.title[-1] in ['.', '!', '?'] \
            if len(self.title) > 0 else False

        # further post processing: https://github.com/christianglodt/django-publications/blob/develop/publications/models/publication.py

    def get_relatedpubs_for_user(self, user):
        status_filter = None
        if not user.is_authenticated:
            status_filter = ['review','reviewed','published']
        if status_filter:
            return self.relatedpubs.filter(status__in=status_filter)
        else:
            return self.relatedpubs.all()


# publication topics and collections

class PubTopic(MPTTModel):

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    description = models.TextField('Description',blank=True)

    status = models.CharField('Status',
        max_length = 10,
        blank = False,
        default = 'draft',
        choices = STATUS_CHOICES)

    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children', db_index=True,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def delete(self):
        super(PubTopic, self).delete()

    delete.alters_data = True

    def get_slug_list(self):
        try:
          ancestors = self.get_ancestors(include_self=True)
        except:
          ancestors = []
        else:
          ancestors = [ i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
          slugs.append('/'.join(ancestors[:i+1]))
        return slugs

    class Meta(object):
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'

class PubCollection(models.Model):

    title = models.CharField('Title',max_length=255)

    tags_filter = models.TextField('Tags / Filter',
        blank = True
    )

    tags_exclude = models.TextField('Tags / Exclude',
        blank = True
    )

    pubtypeids_filter = models.CharField('Publication Type IDs / Filter',
        max_length=255,
        blank = True
    )

    pubtypeids_exclude = models.TextField('Publication Type IDs / Exclude',
        blank = True
    )

    backgroundids_filter = models.CharField('Publication Background IDs / Filter',
        max_length=255,
        blank = True
    )

    backgroundids_exclude = models.TextField('Publication Background IDs / Exclude',
        blank = True
    )

    pubtopic = models.ForeignKey(PubTopic, null=True, on_delete=models.CASCADE)

    my_order = models.PositiveIntegerField(blank=False, null=False)

    def tags_filter_list(self):
        rows_tmp = [v.strip() for v in self.tags_filter.splitlines() if v != ""]
        rows = []
        for s in rows_tmp:
            rows.append([v.strip() for v in s.split(',')])
        return rows

    def tags_exclude_list(self):
        return [v.strip() for v in self.tags_exclude.splitlines() if v != ""]

    def pubtypeids_filter_list(self):
        return [v.strip() for v in self.pubtypeids_filter.split(',') if v != ""]

    def pubtypeids_exclude_list(self):
        return [v.strip() for v in self.pubtypeids_exclude.splitlines() if v != ""]

    def backgroundids_filter_list(self):
        return [v.strip() for v in self.backgroundids_filter.split(',') if v != ""]

    def backgroundids_exclude_list(self):
        return [v.strip() for v in self.backgroundids_exclude.splitlines() if v != ""]

    def get_pubs_for_user(self, user):
        status_filter = None
        if not user.is_authenticated:
            status_filter = ['review','reviewed','published']

        if status_filter:
            pubs = Pub.objects.filter(status__in=status_filter)
        else:
            pubs = Pub.objects.all()

        for tagnameseq in self.tags_filter_list():
            pubs = pubs.filter(tags__name__in=tagnameseq)
        bids = self.backgroundids_filter_list()
        if bids:
            pubs = pubs.filter(background__in=bids)
        ptids = self.pubtypeids_filter_list()
        if ptids:
            pubs = pubs.filter(pubtype__in=ptids)

        for tagname in self.tags_exclude_list():
            pubs = pubs.exclude(tags__name__in=[tagname])
        for bid in self.backgroundids_exclude_list():
            pubs = pubs.exclude(background=bid)
        for ptid in self.pubtypeids_exclude_list():
            pubs = pubs.exclude(pubtype=ptid)

        pubs = pubs.filter(is_related_to=None).annotate(cnt=Count('relatedpubs'))

        return pubs.distinct()

    class Meta(object):
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'
        ordering = ['my_order']

class CustomFlatPage(FlatPage):

    class Meta:
        verbose_name = 'Static Page'
        verbose_name_plural = 'Static Pages'

    description = models.TextField('Description',blank=True)

