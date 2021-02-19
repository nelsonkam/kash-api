from django_hosts import patterns, host

from kweek_api import settings

host_patterns = patterns('',
    host(r'(prod|api)', settings.ROOT_URLCONF, name='api'),
    host(r'([\w\-\_]+)', "storefront.urls", name='storefront'),
)
