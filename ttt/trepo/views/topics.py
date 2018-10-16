from django.shortcuts import render

from trepo.models import PubTopic

def topics(request):

    context = {}
    context['mainid'] = 'repo'
    context['subid'] = 'repo-all'

    status_filter = None
    if not request.user.is_authenticated:
        status_filter = ['reviewed','review','published']

    if status_filter:
        topics = PubTopic.objects.filter(level=0,status__in=status_filter)
    else:
        topics = PubTopic.objects.filter(level=0)
    context['topics'] = topics

    return render(request, 'trepo/alltopics.html', context)