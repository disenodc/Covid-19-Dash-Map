import plotly.graph_objects as go
from graphs.plotly_renders.data import request_map_data
from graphs.BadWayToRequestData.mathdro import map_data
import plotly.express as px
import time
from graphs.objects import tabe_view_data_async

def request_map_date(date):
    r = tabe_view_data_async.main(date)

    # for x in r['confirmed_size']:
    #     print(x)
    r['confirmed_size'] = r['confirmed'].apply(lambda x: int(x)/500)
    r['death_size'] = r['deaths'].apply(lambda x: int(x) / 500)
    r['recovered_size'] = r['recovered'].apply(lambda x:int( x )/ 500)
    # r['time'] = r['lastUpdate'].apply(lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x)))

    map_confirmed = go.Scattermapbox(
        name='Confirmed Cases',
        lon=r['long'].values,
        lat=r['lat'].values,
        text=r['countryRegion'].values,
        customdata=r.loc[:, ['confirmed']],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Confirmed: %{customdata[0]}<br>" +
        "<extra></extra>",
        mode='markers',
        fillcolor='mediumturquoise',
        showlegend=True,
        marker=go.scattermapbox.Marker(
            size=r['confirmed_size'].values,
            color='mediumturquoise',
            opacity=0.5
        ),
        opacity=0.5,

    )

    map_deaths = go.Scattermapbox(
        name='Deaths',
        lon=r['long'].values,
        lat=r['lat'].values,
        text=r['countryRegion'],
        customdata=r.loc[:, ['deaths']],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Deaths: %{customdata[0]}<br>" +
        "<extra></extra>",
        mode='markers',
        fillcolor='rgb(242, 177, 172)',
        showlegend=True,
        marker=go.scattermapbox.Marker(
            size=r['death_size'],
            color='salmon',
            opacity=0.5
        ),
        opacity=0.5,
    )

    map_recovered = go.Scattermapbox(
        customdata=r.loc[:, ['recovered']],
        # deaths = r['deaths'],
        # recovered = r['recovered'],
        name='recovered',
        lon=r['long'].values,
        lat=r['lat'].values,
        text=r['countryRegion'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Recovered: %{customdata[0]}<br>" +
        "<extra></extra>",
        mode='markers',
        fillcolor='purple',
        showlegend=True,
        marker=go.scattermapbox.Marker(
            size=r['recovered_size'],
            color='green',
        ),
        opacity=0.5,
    )

    layout = go.Layout(
        height=800,
        mapbox_style="white-bg",
        autosize=True,
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            }
        ],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    data = [map_confirmed, map_recovered, map_deaths]

    fig = go.Figure(data=data, layout=layout)

    return fig


if __name__ == '__main__':
    request_map_date('2020-03-24').show()
    print(request_map_date('2020-03-24'))