# coding: utf-8

from django.conf.urls.defaults import patterns, url

from DecodeUnicode.views import index, display_block, search


urlpatterns = patterns('',
    url(r'^search/$', search, name='DecodeUnicode-search'),
    url(r'^(?P<block_slug>.*)/$', display_block, name='DecodeUnicode-display_block'),
    url(r'^', index, name='DecodeUnicode-index'),
)
