import plotly.express as px


def create_plot(query_set, metric, device, annotations=None):
    """Creates a plotly graph.

    Args:
        query_set: query set of historical metrics filtered by url
        metric (str): short for metric (e.g. 'lcp', 'cls' etc.)
        device (str): short for device ('m' for mobile or 'd' for desktop)
        annotations: query set of annotations filtered by user and url

    Returns:
        Plotly figure object or string 'Data nejsou k dispozici' if query_set is empty.
    """
    dates = [c.date for c in query_set]
    metrics = eval(f"[c.{metric}{device} for c in query_set]")
    clean_metrics = [item for item in metrics if item is not None]
    try:
        if metrics[0] is not None:
            fig = px.line(x=dates, y=metrics)
            if metric == "lcp":
                limits = [2500, 4000]
                y_min = min(clean_metrics) - 100
                y_max = max(clean_metrics) + 100
            elif metric == "fid":
                limits = [100, 300]
                y_min = min(clean_metrics) - 10
                y_max = max(clean_metrics) + 10
            else:
                limits = [0.1, 0.25]
                y_min = min(clean_metrics) - 0.1
                y_max = max(clean_metrics) + 0.1
            if y_min < 0:
                y_min = 0

            # add color stripes
            fig.add_shape(
                type="rect",
                x0=min(dates),
                x1=max(dates),
                y0=0,
                y1=limits[0],
                yref="y",
                fillcolor="lightgreen",
                layer="below",
                opacity=0.4,
                line_width=0,
            )
            fig.add_shape(
                type="rect",
                x0=min(dates),
                x1=max(dates),
                y0=limits[0],
                y1=limits[1],
                yref="y",
                fillcolor="yellow",
                layer="below",
                opacity=0.4,
                line_width=0,
            )
            fig.add_shape(
                type="rect",
                x0=min(dates),
                x1=max(dates),
                y0=limits[1],
                y1=limits[1] + 100,
                yref="y",
                fillcolor="red",
                layer="below",
                opacity=0.4,
                line_width=0,
            )
            if annotations is not None:
                for annotation in annotations:
                    fig.add_shape(
                        type="line",
                        x0=annotation.date,
                        y0=0,
                        x1=annotation.date,
                        y1=y_max,
                        line=dict(color="red", width=2, dash="dashdot"),
                    )
                    fig.add_annotation(
                        x=annotation.date,
                        y=y_max,
                        text=annotation.annotation_title,
                        hovertext=annotation.annotation_text,
                        showarrow=True,
                        arrowhead=7,
                        ax=0,
                        ay=-20,
                    )

            fig.update_layout(
                title={"text": f"{metric}", "font": {"size": 24}},
                margin_r=40,
                margin_l=40,
                yaxis_range=[y_min, y_max],
            )
            fig.update_yaxes(title=None)
            fig.update_xaxes(title=None)
            return fig
        else:
            return "Data nejsou k dispozici"
    except IndexError:
        return "Data nejsou k dispozici"


def create_charts(query_set,device,annotations):
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
    chart1 = create_plot(query_set, "fid", device, annotations)
    if type(chart1) != str:
        chart1 = chart1.to_html(config=config, include_plotlyjs=False)

    chart2 = create_plot(query_set, "lcp", device, annotations)
    if type(chart2) != str:
        chart2 = chart2.to_html(config=config, include_plotlyjs=False)

    chart3 = create_plot(query_set, "cls", device, annotations)
    if type(chart3) != str:
        chart3 = chart3.to_html(config=config, include_plotlyjs=False)

    return chart1, chart2, chart3
