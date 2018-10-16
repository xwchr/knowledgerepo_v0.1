from django.utils.http import is_safe_url
from django.conf import settings

from django import template
register = template.Library()

from trepo.constants import PUB_TYPES_PUBLIC
from trepo.utils import get_formatted_pub_date

from trepo.models import Pub, Tag, CompanyTag

@register.inclusion_tag('trepo/pub_list.html', takes_context=True)
def pub_list(context):

    collection = context['collection']

    user = context['request'].user
    pubs = collection.get_pubs_for_user(user)

    context['pubs'] = pubs

    return context

@register.simple_tag(takes_context=True)
def get_relatedpubs(context):
    pub = context['pub']
    request = context['request']
    return pub.get_relatedpubs_for_user(request.user)

@register.inclusion_tag('trepo/pub_listitem.html', takes_context=True)
def pub_listitem(context):

    pub = context['pub']

    # publication date

    pubdate = None
    if pub.date_as_string != '1970/01/01':
        if len(pub.date_as_string) == 4:
            pubdate = pub.date.strftime('%Y')
        elif len(pub.date_as_string) == 7:
            pubdate = pub.date.strftime('%b %Y')
        else:
            pubdate = pub.date.strftime('%b %d, %Y')
    context['pubdate'] = get_formatted_pub_date(pub.date_as_string,pub.date)

    # authorstring

    authorstring = None
    if pub.authors and pub.publishers:
        authorstring = pub.publishers
    elif pub.authors:
        authorstring = pub.authors
    elif pub.publishers:
        authorstring = pub.publishers
    else:
        authorstring = None
    context['authorstring'] = authorstring

    context['pubstring'] = pub.publication

    context['pubtype'] = PUB_TYPES_PUBLIC[pub.pubtype].lower()

    if pubdate or pub.publication or pub.description:
        context['pubmeta'] = True
    else:
        context['pubmeta'] = False
    if pubdate or pub.publication:
        context['pubdatestring'] = True
    else:
        context['pubdatestring'] = False

    url_site = None
    if pub.url:
        url_site = pub.url
    url_dl = None
    if pub.url_dl:
        url_dl = pub.url_dl
    elif pub.url_dl_preprint:
        url_dl = pub.url_dl_preprint
    context['url_site'] = url_site
    context['url_dl'] = url_dl

    return context

@register.inclusion_tag('trepo/pub_listitem_short.html', takes_context=True)
def pub_listitem_short(context, pub):

    pubyear = None
    if pub.date_as_string != '1970/01/01':
        if len(pub.date_as_string) >= 4:
            pubyear = pub.date.strftime('%Y')
    context['pubyear'] = pubyear

    authorstring = None
    if pub.authors:
        authorstring = pub.authors
    elif pub.publishers:
        authorstring = pub.publishers
    else:
        authorstring = None
    context['authorstring'] = authorstring

    context['pubstring'] = pub.publication

    context['pub'] = pub

    return context

@register.inclusion_tag('trepo/pub_tags.html', takes_context=True)
def pub_tags(context, full=False):

    pub = context['pub']
    tags = pub.tags.tags
    context['tags'] = tags
    context['full'] = full

    return context

@register.inclusion_tag('trepo/pub_companytags.html', takes_context=True)
def pub_companytags(context, full=False):

    pub = context['pub']
    tags = pub.companytags.tags
    context['tags'] = tags
    context['full'] = full

    return context

@register.simple_tag
def all_tags_count():
    n = Tag.objects.all().count()
    return "{:,}".format(n)

@register.simple_tag
def all_companytags_count():
    n = CompanyTag.objects.all().count()
    return "{:,}".format(n)

@register.simple_tag
def all_pubs_count():
    n = Pub.objects.filter(status__in=['reviewed','published']).count()
    return "{:,}".format(n)

@register.simple_tag
def toplevelpath(path):
    pathseq = [v for v in path.split('/') if v != ""]
    if pathseq:
      return pathseq[0]
    else:
        return 'home'

@register.simple_tag
def get_safe_http_referer(request):
    referer = request.META['HTTP_REFERER']
    if is_safe_url(referer,allowed_hosts=settings.ALLOWED_HOSTS):
        return referer