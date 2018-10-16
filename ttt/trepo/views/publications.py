from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from trepo.models import Pub, Tag, CompanyTag

def publications(request,tag_slug=None,op=None):

    context = {}
    context['mainid'] = 'repo'
    context['subid'] = 'repo-publications'

    status_filter = None
    if not request.user.is_authenticated:
        status_filter = ['review','reviewed','published']

    if status_filter:
        pubs = Pub.objects.filter(status__in=status_filter)
    else:
        pubs = Pub.objects.all()

    if op=='tag':
        pubs = pubs.filter(tags__slug__exact=tag_slug)
        context['filterop'] = 'tag'
        context['tagname'] = Tag.objects.get(slug=tag_slug).name
        
    elif op=='companytag':
        pubs = pubs.filter(companytags__slug__exact=tag_slug)
        context['filterop'] = 'companytag'
        context['tagname'] = CompanyTag.objects.get(slug=tag_slug).name


    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    paginator = Paginator(pubs, 10)
    try:
        pubs = paginator.page(page)
    except PageNotAnInteger:
        pubs = paginator.page(1)
    except EmptyPage:
        pubs = paginator.page(paginator.num_pages)

    context['pubs'] = pubs

    return render(request, 'trepo/pub_search.html', context)
