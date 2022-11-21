# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u1832256/data/www/paberu.ru/guitarstore')
sys.path.insert(1, '/var/www/u1832256/data/djangoenv/lib/python3.9/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'guitarstore.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()