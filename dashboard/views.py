from django.shortcuts import render
import plotly.express as px
from speedcheck.models import Urls, CruxHistory, Profile, ProfileUrl
from .functions import create_plot
from django.http import JsonResponse


def dashboard(request, url_id):
    url_object = Urls.objects.get(id=url_id)
    web_name = url_object.url
    data = CruxHistory.objects.filter(url=url_id)
    url_added = None
    profile_url_id = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        url_added = profile.urls.filter(url=web_name).first()
    if url_added:
        profile_url_id = ProfileUrl.objects.get(url=url_id, profile__user=request.user).id
    if request.POST.get('mobile'):
        device = request.POST.get('mobile')

    elif request.POST.get('desktop'):
        device = request.POST.get('desktop')
    else:
        device = "m"

    # if request.POST.get('addurl'):
        # request.user.profile.urls.add(url_object)
    config = dict({'modeBarButtonsToRemove': ['autoScale', 'zoom', 'pan', 'select', 'zoomIn', 'zoomOut']})
    chart1 = create_plot(data, "lcp", device)
    if type(chart1) != str:
        chart1 = chart1.to_html(config=config, include_plotlyjs='cdn')

    chart2 = create_plot(data, "fid", device)
    if type(chart2) != str:
        chart2 = chart2.to_html(config=config, include_plotlyjs='cdn')

    chart3 = create_plot(data, "cls", device)
    if type(chart3) != str:
        chart3 = chart3.to_html(config=config, include_plotlyjs='cdn')
    return render(request, "dashboard/dashboard.html",
                      context={'chart1': chart1, 'chart2': chart2, 'chart3': chart3, 'web_name': web_name,
                               'device': device, "url_obj": url_object, 'url_added': url_added, 'profile_url_id': profile_url_id})


def remove_profile_url(request):
    url_id = int(request.GET.get('url_id'))
    profile_url_object = ProfileUrl.objects.get(profile__user=request.user, url_id=url_id)
    profile_url_object.delete()
    return JsonResponse({'success': True})


def add_profile_url(request):
    url_id = int(request.GET.get('url_id'))
    url_object = Urls.objects.get(id=url_id)
    request.user.profile.urls.add(url_object)
    return JsonResponse({'success': True})


