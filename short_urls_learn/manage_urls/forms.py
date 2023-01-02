from django import forms
from .models import Url


class EnterUrlForm(forms.ModelForm):
    original_url = forms.URLField(max_length=200)

    class Meta:
        model = Url
        fields = ['original_url']



