"""
WSGI config for ttt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os, sys, site

# for production setup with apache2 via wsgi

#site.addsitedir('')
#path=''
#if path not in sys.path:
#  sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ttt.settings")

application = get_wsgi_application()