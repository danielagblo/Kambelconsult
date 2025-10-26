"""
ASGI config for Kambel Consult Admin Panel.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kambel_admin.settings')

application = get_asgi_application()
