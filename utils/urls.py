try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import settings_js

urlpatterns = [
    # javascript settings
    url(r'settings\.js', settings_js, name='js_settings'),
]
