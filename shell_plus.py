import sys; print('Python %s on %s' % (sys.version, sys.platform))
import django; print('Django %s' % django.get_version())
import logging
logging.basicConfig(format="%(levelname)-8s %(asctime)s %(name)s %(message)s", datefmt='%m/%d/%y %H:%M:%S', stream=sys.stdout )
log = logging.getLogger("root")

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from logging.config import dictConfig

dictConfig(getattr(settings, 'LOGGING', {}))
log.debug("Logging has been initialized at DEBUG")
log.setLevel( logging.DEBUG)
log.disabled = False

for _configs in apps.get_app_configs():
    for _class in _configs.get_models():
        if _class.__name__.startswith("Historical"): continue
        log.debug("Registering model {}".format(_class.__name__))
        globals()[_class.__name__] = apps.get_model(_configs.label, _class.__name__)

def debug_sql():
    from debug_toolbar.management.commands import debugsqlshell
    return