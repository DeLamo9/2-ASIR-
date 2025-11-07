"""
WSGI config for Proyecto_IAW project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https:/${PROJECT_ROOT}/docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Proyecto_IAW.settings')

application = get_wsgi_application()
