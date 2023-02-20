from django.forms import ModelForm
from django.contrib.auth.models import User
from speedcheck.models import Urls, Profile


class UrlForm(ModelForm):

    class Meta:
        model = Urls
        fields = ['url']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['urls']
