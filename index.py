# import dash_core_components as dcc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
# Connect to main app.py file
import dash_bootstrap_components as dbc
import dash
# Connect to your app pages
from apps import animasyon, nufus

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

app.layout = html.Div([



dbc.NavbarSimple(
            children=[
        dbc.NavItem(dbc.NavLink('Nüfus Değişimi', href='/apps/nufus',style={
                                                                "text-decoration": "underline",#overline
                                                                'border': '2px solid #74a9cf',
                                                                'cursor': 'pointer',
                                                                'border-radius': '15px 50px',})),
        dbc.NavItem(dbc.NavLink('Animasyonu İzle', href='/apps/animasyon',style={
                                                                "text-decoration": "underline",#overline
                                                                'border': '2px solid #74a9cf',
                                                                'cursor': 'pointer',
                                                                'border-radius': '15px 50px',})),
    ],
    # style={'position': 'fixed','top': '0','z-index': '100'},
    links_left=True,
    # className="g-0",
    # className="g-0 flex-grow-1",
    # expand= 'md',
    fluid=True,
    brand="İSTANBUL İLÇE NÜFUSLARININ YILLARA GÖRE DEĞİŞİMİ (2008-2030)",
    brand_href="/",
    color="dark",
    dark=True,
    # align="center"
),
    # html.Pre(children="İSTANBUL KAYIT DIŞI SU TÜKETİMİNE AİT KAYIT DIŞI NÜFUS",
    #          style={"text-align": "center", "font-size": "23px", "color": "black", }),



    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[],)
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/nufus':
        return nufus.layout
    if pathname == '/apps/animasyon':
        return animasyon.layout
    else:
        return nufus.layout


if __name__ == '__main__':
    # app.run_server(debug=False)
    app.run_server(host="0.0.0.0", port=8055)