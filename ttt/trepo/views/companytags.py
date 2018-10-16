from django.shortcuts import render

from trepo.models import CompanyTag

def companytags(request):

    context = {}
    context['mainid'] = 'repo'
    context['subid'] = 'repo-companytags'

    tags = CompanyTag.objects.all()
    context['tags'] = tags

    return render(request, 'trepo/allcompanytags.html', context)
