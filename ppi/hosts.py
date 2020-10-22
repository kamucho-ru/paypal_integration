from django_hosts import patterns, host


host_patterns = patterns('ppi',
    host(r'www', 'urls', name='www'),
    host(r'support', 'urls_support', name='support'),
    host(r'(\w+)', 'urls_sub', name='dynamic'),
)
