from django.shortcuts import render

from trepo.models import Tag

def tags(request):

    context = {}
    context['mainid'] = 'repo'
    context['subid'] = 'repo-tags'

    tags = Tag.objects.all()
    context['tags'] = tags

    return render(request, 'trepo/alltags.html', context)
