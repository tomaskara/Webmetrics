import plotly.express as px


def create_plot(query_set, metric, device):
    dates = [c.date for c in query_set]
    metrics = eval(f"[c.{metric}{device} for c in query_set]")
    clean_metrics = [item for item in metrics if item is not None]
    if metrics[0] != None:
        fig = px.line(x=dates, y=metrics)
        if metric == 'lcp':
            limits = [2500, 4000]
        elif metric == 'fid':
            limits = [100, 300]
        else:
            limits = [0.1, 0.25]
        # add color stripes
        fig.add_shape(
            type='rect',
            x0=min(dates), x1=max(dates),
            y0=0, y1=limits[0],
            yref='y',
            fillcolor='lightgreen',
            layer='below',
            opacity=0.4,
            line_width=0
        )
        fig.add_shape(
            type='rect',
            x0=min(dates), x1=max(dates),
            y0=limits[0], y1=limits[1],
            yref='y',
            fillcolor='yellow',
            layer='below',
            opacity=0.4,
            line_width=0
        )
        fig.add_shape(
            type='rect',
            x0=min(dates), x1=max(dates),
            y0=limits[1], y1=limits[1]+100,
            yref='y',
            fillcolor='red',
            layer='below',
            opacity=0.4,
            line_width=0
        )
        if metric == 'cls':
            fig.update_layout(
                title={
                    'text': f"{metric}",
                    'font': {'size': 24}
                },

                yaxis_range=[min(clean_metrics) - 0.1, max(clean_metrics) + 0.1],
            )
        else:
            fig.update_layout(
                title={
                    'text': f"{metric}",
                    'font': {'size': 24}
                },

                yaxis_range=[min(clean_metrics) - 5, max(clean_metrics) + 5],
            )
        return fig
    else:
        return "Data nejsou k dispozici"