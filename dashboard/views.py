from django.shortcuts import render
import plotly.express as px
from speedcheck.models import Urls, CruxHistory, Profile
from .functions import create_plot


def dashboard(request, url_id):
    url_object = Urls.objects.get(id=url_id)
    web_name = url_object.url
    data = CruxHistory.objects.filter(url=url_id)
    profile = Profile.objects.filter(user=request.user).first()
    url_added = profile.urls.filter(url=web_name)
    if request.POST.get('mobile'):
        device = request.POST.get('mobile')

    elif request.POST.get('desktop'):
        device = request.POST.get('desktop')
    else:
        device = "m"

    if request.POST.get('addurl'):
        request.user.profile.urls.add(url_object)
    config = dict({'modeBarButtonsToRemove': ['autoScale', 'zoom', 'pan', 'select', 'zoomIn', 'zoomOut']})
    chart1 = create_plot(data, "lcp", device)
    if type(chart1) != str:
        chart1 = chart1.to_html(config=config, include_plotlyjs=False)

    chart2 = create_plot(data, "fid", device)
    if type(chart2) != str:
        chart2 = chart2.to_html(config=config, include_plotlyjs=False)

    chart3 = create_plot(data, "cls", device)
    if type(chart3) != str:
        chart3 = chart3.to_html(config=config, include_plotlyjs=False)
    return render(request, "dashboard/dashboard.html",
                      context={'chart1': chart1,'chart2': chart2, 'chart3': chart3, 'web_name': web_name,
                               'device': device, "url_obj": url_object, 'url_added': url_added})


