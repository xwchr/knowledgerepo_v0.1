from django.shortcuts import render

def home(request):

    context = {}
    context['mainid'] = 'home'

    return render(request, 'trepo/home.html', context)