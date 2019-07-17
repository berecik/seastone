# -*- coding: utf-8 -*-

import logging
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.cache import caches, InvalidCacheBackendError

from . import log_level_dic

logger = logging.getLogger("command_logger_simple_time")


class Command(BaseCommand):
    """
    A command to clear the specified cache or all caches.
    ..usage:
        ./manage.py clear_memcache -k default
        ./manage.py clear_memcache -a
    """
    args = '<key>'
    help = "Clears the specified memcache cache"
    option_list = BaseCommand.option_list + (
        make_option('--key', '-k', dest='key', action="store", type="string", help='The cache to clear'),
        make_option('--all', '-a', dest='clear_all', action="store_true", default=False, help="Clears all caches"),
    )

    def handle(self, *args, **options):
        logger.setLevel(log_level_dic.get(int(options['verbosity']), 1))
        logger.debug("args: {}".format(args))
        logger.debug("options: {}".format(options))
        logger.warning('Clearing Caches')
        try:
            assert settings.CACHES
            all_keys = settings.CACHES.keys()
            if 'clear_all' in options:
                clear_all = options['clear_all']
            else:
                clear_all = False
            if clear_all:
                num_cleared = 0
                for x, key in enumerate(all_keys):
                    try:
                        logger.info('{}] Clearing Cache "{}"'.format(x + 1, key))
                        cache_to_clear = caches[key]
                        cache_to_clear.clear()
                        num_cleared += 1
                    except InvalidCacheBackendError:
                        logger.error('{}] Cache "{}" is invalid'.format(x + 1, key))
                logger.warning("Cleared {} Caches\n".format(num_cleared))
            elif options["key"]:
                key = options["key"]
                if key in all_keys:
                    try:
                        logger.info('Clearing Cache "{}"'.format(key))
                        cache_to_clear = caches[key]
                        cache_to_clear.clear()
                        logger.debug('Cache "{}" has been cleared!'.format(key))
                    except InvalidCacheBackendError:
                        logger.error('Cache "{}" is invalid'.format(key))
                else:
                    raise CommandError('Cache "{}" not found. Nothing cleared.'.format(key))
            else:
                raise CommandError("Key or All option missing, you must have at least one")
        except AttributeError:
            raise CommandError('You have no cache configured!')
