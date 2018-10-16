from django.shortcuts import render, get_object_or_404

from trepo.constants import PUB_TYPES_PUBLIC
from trepo.utils import get_formatted_pub_date
from trepo.models import Pub

def pubdetail(request,pub_slug):

    context = {}
    context['mainid'] = 'repo'
    context['subid'] = 'repo-pubdetail'

    status_filter = None
    if not request.user.is_authenticated:
        status_filter = ['review','reviewed','published']

    if status_filter:
        pub = get_object_or_404(Pub,slug=pub_slug,status__in=status_filter)
    else:
        pub = get_object_or_404(Pub,slug=pub_slug)

    context['pub'] = pub
    context['pubdate'] = get_formatted_pub_date(pub.date_as_string,pub.date)
    context['pubtype'] = PUB_TYPES_PUBLIC[pub.pubtype]


    return render(request, 'trepo/pub_detail.html', context)
