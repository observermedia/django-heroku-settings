from __future__ import unicode_literals

"""
WSGI config for a django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "co.settings")
from dj_static import Cling

from django.core.wsgi import get_wsgi_application
application = Cling(get_wsgi_application())

