#from django import forms
#from simple_search import BaseSearchForm
from django.forms import ModelForm
from models import Site

class SiteForm(ModelForm):
    class Meta:
        model = Site

