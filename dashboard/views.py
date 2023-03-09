from django.shortcuts import render
import plotly.express as px
from speedcheck.models import Urls, CruxHistory, Profile


def dashboard(request, url_id):
    url_object = Urls.objects.get(id=url_id)
    web_name = url_object.url
    data = CruxHistory.objects.filter(url=url_id)
    if request.POST.get('mobile'):
        device = request.POST.get('mobile')

    elif request.POST.get('desktop'):
        device = request.POST.get('desktop')
    else:
        device = "m"

    if request.POST.get('addurl'):
        url_to_add = Urls.objects.get(id=url_id)
        request.user.profile.urls.add(url_to_add)
    # lcp graph
    metric = "lcp"
    dates = [c.date for c in data]
    metrics = eval(f"[c.{metric}{device} for c in data]")
    clean_metrics = [item for item in metrics if item is not None]
    if metrics[0] != None:
        fig = px.line(x=dates, y=metrics)
        limits = [2500, 4000]
        colors = ['yellow', 'red']
        # add color stripes
        fig.add_shape(
            type='rect',
            x0=min(dates), x1=max(dates),
            y0=0, y1=2500,
            yref='y',
            fillcolor='lightgreen',
            layer='below',
            opacity=0.4,
            line_width=0
        )
        # TODO add color stripes - fig.add_shape
        fig.update_layout(
            title={
                'text': f"{metric}",
                'font': {'size': 24}
            },

            yaxis_range=[min(clean_metrics) - 5, max(clean_metrics) + 5],
        )
        config = dict({'modeBarButtonsToRemove': ['autoScale', 'zoom', 'pan', 'select', 'zoomIn', 'zoomOut']})
        chart = fig.to_html(config=config)
        return render(request, "dashboard/dashboard.html",
                      context={'chart': chart, 'web_name': web_name, 'device': device, "url_obj": url_object})
    else:
        return render(request, "dashboard/dashboard.html",
                      context={'chart': "Data nejsou k dispozici", 'nodata': True, 'web_name': web_name,
                               'device': device, "url_obj": url_object})

