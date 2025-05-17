from django import forms
from .models import Category, Condition


class AdForm(forms.Form):
    title = forms.CharField(label="Title of ad", max_length=255)
    description = forms.CharField(label="Description of ad", widget=forms.Textarea)
    image_url = forms.URLField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    condition = forms.ModelChoiceField(queryset=Condition.objects.all())
