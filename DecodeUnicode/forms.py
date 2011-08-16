# coding: utf-8

"""
    PyLucid DecodeUnicode forms
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~   

    :copyleft: 2007-2011 by the PyLucid team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details
"""


from django import forms

from DecodeUnicode.unicode_data import unicode_block_data


class SlugValidationForm(forms.Form):
    block = forms.SlugField()

class SelectBlock(forms.Form):
    block = forms.ChoiceField(choices=unicode_block_data.get_choices(),
        label=""
    )

class SearchForm(forms.Form):
    char = forms.CharField(max_length=1, min_length=1,
        label="Search for a unicode character",
        widget=forms.TextInput(attrs={"required":"required"})
    )
