# coding: utf-8

"""
    PyLucid DecodeUnicode plugin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~   

    :copyleft: 2007-2010 by the PyLucid team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details
"""


import unicodedata

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from pylucid_project.apps.pylucid.decorators import render_to
from DecodeUnicode.forms import SlugValidationForm, SelectBlock, SearchForm
from DecodeUnicode.unicode_data import unicode_block_data
from django.core.exceptions import SuspiciousOperation


def lucidTag(request):
    msg = "[obsolete lucidTag DecodeUnicode]"
    if request.user.is_staff or settings.DEBUG:
        messages.error(request,
            "DecodeUnicode is a PluginPage,"
            " please remove lucidTag 'DecodeUnicode' tag / delete the page"
            " and create a new PluginPage!"
        )
    return msg


def index(request):
    block_slug = None

    if request.GET:
        form = SlugValidationForm(request.GET)
        if form.is_valid():
            block_slug = form.cleaned_data['block']
        else:
            msg = "Block unknown!"
            if request.user.is_staff or settings.DEBUG:
                msg += " (slug is invalid: %r)" % request.GET["block"]
            messages.error(request, msg)

    if block_slug is None:
        first_block = unicode_block_data.get_first_block()
        block_slug = first_block.slug

    url = reverse("DecodeUnicode-display_block", kwargs={"block_slug":block_slug})
    return HttpResponseRedirect(url)

def search(request):
    if not request.POST:
        raise SuspiciousOperation

    form = SearchForm(request.POST)
    if not form.is_valid():
        raise SuspiciousOperation("Form not valid.")

    char = form.cleaned_data['char']
    block = unicode_block_data.get_block_by_char(char)
    block_slug = block.slug

    url = reverse("DecodeUnicode-display_block", kwargs={"block_slug":block_slug})
    url += "#char_%s" % ord(char)
    messages.info(request, "Found character '%s' in unicode block: '%s'" % (char, block.name))
    return HttpResponseRedirect(url)


@render_to("DecodeUnicode/display.html")
def display_block(request, block_slug):
    try:
        unicode_block = unicode_block_data[block_slug] # get a UnicodeBlock() instance
    except KeyError:
        msg = "Block unknown!"
        if request.user.is_staff or settings.DEBUG:
            msg += " (block slug: %r)" % block_slug
        messages.error(request, msg)
        return index(request)

    char_list = unicode_block.get_char_list()
    select_block_form = SelectBlock(initial={"block":block_slug})
    search_form = SearchForm()

    context = {
        "select_block_form": select_block_form,
        "search_form":search_form,

        "prior_block": unicode_block_data.get_prior_block(unicode_block),
        "next_block": unicode_block_data.get_next_block(unicode_block),

        "block_name": unicode_block.name,

        "range_hex1": "0x%04X" % unicode_block.start,
        "range_hex2": "0x%04X" % unicode_block.end,

        "char_list": char_list,

        "unidata_version": unicodedata.unidata_version,
    }
    return context
