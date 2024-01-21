from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.urls import reverse

from .forms import AnnotationsForm, ProfileForm, UrlForm, UserForm
from .functions import get_api_data
from .models import Annotations, Profile, ProfileUrl, Urls


def home(request):
    """View function to create homepage"""
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            if Urls.objects.filter(url=form.cleaned_data["url"]).exists():
                get_api_data(form.cleaned_data["url"])
                id_url = Urls.objects.get(url=form.cleaned_data["url"]).id
                new_url = reverse("dashboard", args=[id_url])
                return HttpResponseRedirect(new_url)
            else:
                form.save()
                get_api_data(form.cleaned_data["url"])
                id_url = Urls.objects.get(url=form.cleaned_data["url"]).id
                new_url = reverse("dashboard", args=[id_url])
                return HttpResponseRedirect(new_url)

    else:
        form = UrlForm()
    return render(request, "home.html", {"form": form})


@login_required
def profilepage(request):
    """View function to create user page with list of followed urls, list of anotations,
    create annotations etc."""
    if request.method == "POST":
        annotation_form = AnnotationsForm(data=request.POST, user=request.user)
        if annotation_form.is_valid():
            annotation = Annotations(
                profileurl=annotation_form.cleaned_data["profileurl"],
                date=annotation_form.cleaned_data["date"],
                annotation_title=annotation_form.cleaned_data["annotation_title"],
                annotation_text=annotation_form.cleaned_data["annotation_text"],
            )
            annotation.save()
            return JsonResponse(
                {
                    "success": True,
                    "url": annotation.profileurl.url.url,
                    "title": annotation.annotation_title,
                    "text": annotation.annotation_text,
                }
            )
    else:
        annotation_form = AnnotationsForm(
            instance=request.user.profile, user=request.user
        )
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    profile = Profile.objects.get(user=request.user)
    return render(
        request=request,
        template_name="user.html",
        context={
            "user": request.user,
            "user_form": user_form,
            "profile_form": profile_form,
            "profile": profile,
            "annotation_form": annotation_form,
            "messages": messages.get_messages(request),
        },
    )

@login_required
def userpage(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, ('Vaše údaje byly uspěšně upraveny!'))
        else:
            messages.error(request, ('Úpravu nelze provést.'))
        return redirect("userpage")
    user_form = UserForm(instance=request.user)
    return render(request, "updateuser.html", {"user": request.user, "user_form": user_form})

def change_value(request):
    """Handle JS request from templates to change email alert settings."""
    value = request.GET.get("value")
    url_id = int(request.GET.get("url_id"))
    profile_url_object = ProfileUrl.objects.get(id=url_id)
    if value == "off":
        profile_url_object.email_alert = False
    else:
        profile_url_object.email_alert = True
        profile_url_object.sensitivity = int(value)
    profile_url_object.save()
    return JsonResponse({"success": True})


def delete_annot(request):
    """Handle JS request from templates to delete annotations."""
    Annotations.objects.get(id=request.GET.get("annot_id")).delete()
    return JsonResponse({"success": True})

def test_page(request):
    return render(request,"test.html")

def tools(request):
    return render(request, "tools.html")
