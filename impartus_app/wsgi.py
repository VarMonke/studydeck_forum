"""
WSGI config for impartus_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'impartus_app.settings')

path = '/home/VarMonke/impartus_app'

if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'impartus_app.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
