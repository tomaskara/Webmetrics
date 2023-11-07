from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render

from speedcheck.models import (
    Annotations,
    CruxHistory,
    Profile,
    ProfileUrl,
    Urls,
    CruxWeeklyHistory,
)

from .functions import create_charts
from speedcheck.functions import get_api_history_data


def dashboard(request, url_id):
    """View function to create a dashboard containing charts and metrics for a given url

    Args:
        request: The HTTP request object.
        url_id: The ID of the URL from Urls model.
    """
    url_object = Urls.objects.get(id=url_id)
    web_name = url_object.url
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
    if request.method == "POST":
        if request.POST.get("mobile"):
            request.session["device"] = "m"
        elif request.POST.get("desktop"):
            request.session["device"] = "d"
        elif request.POST.get("daily"):
            request.session["source_of_data"] = "d"
        elif request.POST.get("weekly"):
            request.session["source_of_data"] = "w"
    else:
        # If the state does not exist in the session, use the default value
        if "device" not in request.session:
            request.session["device"] = "m"
        if "source_of_data" not in request.session:
            request.session["source_of_data"] = "d"

    device = request.session["device"]
    source_of_data = request.session["source_of_data"]

    if source_of_data == "d":
        data = CruxHistory.objects.filter(url=url_id)
    elif source_of_data == "w":
        get_api_history_data(web_name)
        data = CruxWeeklyHistory.objects.filter(url=url_id)

    chart1, chart2, chart3, chart4 = create_charts(data, device, annotations)

    return render(
        request,
        "dashboard/dashboard.html",
        context={
            "chart1": chart1,
            "chart2": chart2,
            "chart3": chart3,
            "chart4": chart4,
            "web_name": web_name,
            "device": device,
            "source_of_data": source_of_data,
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
