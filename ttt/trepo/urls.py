from django.urls import path, re_path

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from django.contrib.flatpages.views import flatpage
from . import views

urlpatterns = [
    re_path(r'^favicon\.ico$',
        RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'),),
        name="favicon"
    ),
    path('browserconfig.xml',
        RedirectView.as_view(url=staticfiles_storage.url('img/browserconfig.xml'),),
        name="favicon"
    ),
    path('site.webmanifest',
        RedirectView.as_view(url=staticfiles_storage.url('img/site.webmanifest'),),
        name="favicon"
    ),

    path('', views.home, name='home'),
    path('researchdb/', views.topics, name='topics'),
    path('researchdb/tst/', views.tst, name='tst'),
    path('researchdb/tags/', views.tags, name='tags'),
    path('researchdb/companies/', views.companytags, name='companytags'),
    path('researchdb/pubdetail/<slug:pub_slug>/', views.pubdetail, name='pubdetail'),

    path('researchdb/pub/', views.publications, name='publications'),

    path('researchdb/pub/tag/<slug:tag_slug>/', views.publications, {'op' : 'tag'}, name='publications'),
    path('researchdb/pub/companytag/<slug:tag_slug>/', views.publications, {'op' : 'companytag'}, name='publications'),

    path('researchdb/topic/<slug:topic_slug>/', views.topic, name='topic'),

    re_path(r'^(?P<url>.*)$', flatpage),
]