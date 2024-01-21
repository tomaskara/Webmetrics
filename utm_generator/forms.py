from django import forms


class UtmBuilder(forms.Form):
    base_url = forms.URLField()
    utm_source = forms.CharField()
    utm_medium = forms.CharField()
    utm_campaign = forms.CharField()
    utm_content = forms.CharField()
    utm_term = forms.CharField()