from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
import json
from .forms import UrlForm, UserForm, ProfileForm, AnnotationsForm
from .models import Urls, Profile, ProfileUrl, Annotations
from .functions import get_api_data, get_api_history_data
from django.contrib.auth.decorators import login_required


def home(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UrlForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if Urls.objects.filter(url=form.cleaned_data['url']).exists():
                get_api_data(form.cleaned_data['url'])
                id_url = Urls.objects.get(url=form.cleaned_data['url']).id
                new_url = reverse('dashboard', args=[id_url])
                return HttpResponseRedirect(new_url)
            else:
                form.save()
                get_api_data(form.cleaned_data['url'])
                id_url = Urls.objects.get(url=form.cleaned_data['url']).id
                new_url = reverse('dashboard', args=[id_url])
                return HttpResponseRedirect(new_url)

        # if a GET (or any other method) we'll create a blank form
    else:
        form = UrlForm()
    return render(request, "home.html", {'form': form})

def test(request):
    return render(request, "test.html")


@login_required
def profilepage(request):
    if request.method == 'POST':
        annotation_form = AnnotationsForm(data=request.POST, user=request.user)
        if annotation_form.is_valid():
            annotation = Annotations(
                profileurl=annotation_form.cleaned_data['profileurl'],
                date=annotation_form.cleaned_data['date'],
                annotation_title=annotation_form.cleaned_data['annotation_title'],
                annotation_text=annotation_form.cleaned_data['annotation_text'],
            )
            annotation.save()
            return JsonResponse({'success': True, 'url': annotation.profileurl.url.url,
                                 'title': annotation.annotation_title,
                                 'text': annotation.annotation_text})
    else:
        annotation_form = AnnotationsForm(instance=request.user.profile,
                                          user=request.user)
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    profile = Profile.objects.get(user=request.user)
    return render(request=request, template_name="user.html",
                  context={"user": request.user, "user_form": user_form, "profile_form": profile_form,
                           'profile': profile, "annotation_form": annotation_form, 'messages': messages.get_messages(request)})


def change_value(request):
    value = request.GET.get('value')
    url_id = int(request.GET.get('url_id'))
    profile_url_object = ProfileUrl.objects.get(id=url_id)
    if value == "off":
        profile_url_object.email_alert = False
    else:
        profile_url_object.email_alert = True
        profile_url_object.sensitivity = int(value)
    profile_url_object.save()
    return JsonResponse({'success': True})

def delete_annot(request):
    Annotations.objects.get(id=request.GET.get('annot_id')).delete()
    return JsonResponse({'success': True})

def function_test(request):
    get_api_history_data("https://www.homecredit.cz/pujcky")
    return JsonResponse({'success': True})