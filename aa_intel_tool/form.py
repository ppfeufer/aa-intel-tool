"""
Our forms
"""

# Django
from django import forms
from django.utils.translation import gettext_lazy as _


class IntelForm(forms.Form):
    """
    Intel form
    """

    eve_intel = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 15,
                "input_type": "textarea",
                "placeholder": _("Paste here …"),
                "autofocus": "autofocus",
            }
        ),
        required=True,
        label="",  # Make sure there is no form label, we don't need it
    )
