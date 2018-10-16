from django.shortcuts import render, get_object_or_404

from trepo.models import Pub, PubTopic, PubCollection

def topic(request,topic_slug):

    context = {}
    context['mainid'] = 'repo'
    context['subid'] = 'repo-topic'

    status_filter = None
    if not request.user.is_authenticated:
        status_filter = ['reviewed','review','published']

    if status_filter:
        topic = get_object_or_404(PubTopic,slug=topic_slug,status__in=status_filter)
    else:
        topic = get_object_or_404(PubTopic,slug=topic_slug)

    collections = PubCollection.objects.filter(pubtopic=topic)

    context['topic'] = topic
    context['collections'] =collections

    return render(request, 'trepo/topic_collections.html', context)