import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import json
import folium
from folium.plugins import MarkerCluster
import plotly.express as px

# Folium 맵 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)
# Folium 맵에 마커 추가
marker_cluster = MarkerCluster().add_to(m)
folium.Marker([37.5665, 126.9780], popup='Seoul').add_to(marker_cluster)

# Folium 맵을 HTML로 변환
folium_map_html = m._repr_html_()

# Dash 앱 생성
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Iframe(
        id='folium-map',
        srcDoc=folium_map_html,
        width='100%',
        height='700vh'
    ),
    html.Div(id='popup-content')
])

@app.callback(
    Output('popup-content', 'children'),
    [Input('folium-map', 'n_clicks')]
)
def update_popup_content(n_clicks):
    if n_clicks is None:
        return ''
    else:
        return html.P('Clicked on the map!')

if __name__ == '__main__':
    app.run_server(debug=True)
