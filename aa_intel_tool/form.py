"""
our forms
"""

# Django
from django import forms


class IntelForm(forms.Form):
    """
    SRP request reject form
    """

    eve_intel = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 15,
                "input_type": "textarea",
                "placeholder": "Paste here ...",
            }
        ),
        required=True,
        label="",
    )
