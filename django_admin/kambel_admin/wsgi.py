"""
WSGI config for Kambel Consult Admin Panel.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kambel_admin.settings')

application = get_wsgi_application()
