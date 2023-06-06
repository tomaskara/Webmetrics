from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from speedcheck.models import Urls, CruxHistory, Profile, ProfileUrl, Annotations
from .functions import create_plot
from django.http import JsonResponse


def dashboard(request, url_id):
    url_object = Urls.objects.get(id=url_id)
    web_name = url_object.url
    data = CruxHistory.objects.filter(url=url_id)
    url_added = None
    profile_url_id = None
    annotations = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        url_added = profile.urls.filter(url=web_name).first()
        try:
            current_profile_url = ProfileUrl.objects.get(
                url=url_id, profile__user=request.user
            )
            annotations = Annotations.objects.filter(profileurl=current_profile_url)
            if url_added:
                profile_url_id = current_profile_url.id
        except ObjectDoesNotExist:
            pass
    if request.POST.get("mobile"):
        device = request.POST.get("mobile")

    elif request.POST.get("desktop"):
        device = request.POST.get("desktop")
    else:
        device = "m"

    config = dict(
        {
            "modeBarButtonsToRemove": [
                "autoScale",
                "zoom",
                "pan",
                "select",
                "zoomIn",
                "zoomOut",
            ],

        }
    )
    chart1 = create_plot(data, "fid", device, annotations)
    if type(chart1) != str:
        chart1 = chart1.to_html(config=config, include_plotlyjs=False)

    chart2 = create_plot(data, "lcp", device, annotations)
    if type(chart2) != str:
        chart2 = chart2.to_html(config=config, include_plotlyjs=False)

    chart3 = create_plot(data, "cls", device, annotations)
    if type(chart3) != str:
        chart3 = chart3.to_html(config=config, include_plotlyjs=False)
    return render(
        request,
        "dashboard/dashboard.html",
        context={
            "chart1": chart1,
            "chart2": chart2,
            "chart3": chart3,
            "web_name": web_name,
            "device": device,
            "url_obj": url_object,
            "url_added": url_added,
            "profile_url_id": profile_url_id,
        },
    )


def remove_profile_url(request):
    """Handle JS request from templates to remove url from ProfileUrl model."""
    url_id = int(request.GET.get("url_id"))
    profile_url_object = ProfileUrl.objects.get(
        profile__user=request.user, url_id=url_id
    )
    profile_url_object.delete()
    return JsonResponse({"success": True})


def add_profile_url(request):
    """Handle JS request from templates and add url to ProfileUrl model."""
    url_id = int(request.GET.get("url_id"))
    url_object = Urls.objects.get(id=url_id)
    request.user.profile.urls.add(url_object)
    return JsonResponse({"success": True})

