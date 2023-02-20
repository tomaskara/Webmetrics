from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from .forms import UrlForm, UserForm, ProfileForm
from .models import Urls, Profile, ProfileUrl
from .functions import get_api_data
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
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    profile = Profile.objects.get(user=request.user)
    return render(request=request, template_name="user.html",
                  context={"user": request.user, "user_form": user_form, "profile_form": profile_form, 'profile': profile})


def change_value(request):
    value = request.GET.get('value')
    url_id = int(request.GET.get('url_id'))
    profile_url_object = ProfileUrl.objects.get(id=url_id)
    profile_url_object.email_alert = value
    profile_url_object.save()
    return JsonResponse({'success': True})