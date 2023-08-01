from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.widgets import DateInput, Textarea

from speedcheck.models import Annotations, Profile, ProfileUrl, Urls


class UrlForm(ModelForm):
    class Meta:
        model = Urls
        fields = ["url"]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["urls"]


class AnnotationsForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profileurl"].queryset = ProfileUrl.objects.filter(
            profile__user=user
        )

    class Meta:
        model = Annotations
        fields = ["profileurl", "date", "annotation_title", "annotation_text"]
        widgets = {
            "date": DateInput(attrs={"type": "date"}),
            "annotation_text": Textarea(attrs={"rows": 3}),
        }
