from django_hosts import patterns, host

from AppMain import settings

host_patterns = patterns('', host(r'(prod|api|kweek-api)', settings.ROOT_URLCONF, name='api'), )
