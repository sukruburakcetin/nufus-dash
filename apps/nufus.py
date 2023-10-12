import dash
from dash.dependencies import Output, Input, State
from dash import dcc, html, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import json
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, RidgeCV

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

access_token = 'pk.eyJ1IjoiYWJkdWxrZXJpbW5lc2UiLCJhIjoiY2s5aThsZWlnMDExcjNkcWFmaWUxcmh3YyJ9.s-4VLvmoPQFPXdu9Mcd6pA'
px.set_mapbox_access_token(access_token)

with open(r"./assets/istanbul-districts.json"
        ,encoding='utf-8') as response:

    ist_districts= json.load(response)

animated_nufus = pd.read_excel(r"./assets/animated_nufus.xlsx")
il_nufus = pd.read_excel(r"./assets/il_nufus.xlsx")
group_df = pd.read_excel(r"./assets/group_df.xlsx")
ilce_nufus = pd.read_excel(r"./assets/son_ilce_nufus_07_21.xlsx")
ilce_nokta = pd.read_excel(r"./assets/ilce_nokta.xlsx")

x = ilce_nufus[["YIL"]]
y = ilce_nufus.drop(['YIL'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=0.10,random_state=42)
lambdalar = 10 ** np.linspace(10, -2, 100) * 0.5
ridgecv = RidgeCV(alphas=lambdalar, scoring="neg_mean_squared_error", cv=10,
                  # normalize=True
                  )
ridgecv.fit(X_train, y_train)
ridge_tuned = Ridge(alpha=ridgecv.alpha_).fit(X_train, y_train)

ridge_actual_vs_predict = pd.read_excel(r"./assets/actual_vs_predict_ridge.xls")
predicted_values = pd.read_excel(r"./assets/predict_ridge.xls")

x = ridge_actual_vs_predict['YIL'].values
y = ridge_actual_vs_predict['value'].values
predicted_values = predicted_values["predicts_values"].values


animated_nufus = animated_nufus[animated_nufus["YIL"] != 2007]
ilce_nufus = ilce_nufus[ilce_nufus["YIL"] != 2007]
group_df = group_df[group_df["YIL"] != 2007]

layout = dbc.Container([

    dbc.Row([
        # dbc.Col([dcc.Input(id="slct_year", type='number',value=2008, min=2008, max=2030, step=1,
        #                    ),],
        #         style={'width':'90px'},xs=12, sm=12, md=5, lg=5, xl=5
        #         ),

        dbc.Col([html.P("""2008 - 2021 yılları arasındaki nüfus verileri TUİK'in yayınlamış olduğu verilerdir. 2021 yılından sonraki veriler ise Ridge Regresyon modeli ile tahmin edilmiştir.""",
                style={'color':'white','whiteSpace': 'pre-line','float':'left',}),#'font-size':'0.75em',"font-family": "Verdana, Geneva, Tahoma, sans-serif",
                    ],xs=12, sm=12, md=9, lg=9, xl=9),
        # dbc.Col([],xs=12, sm=12, md=1, lg=1, xl=1, style={"width":"60px"}),
        dbc.Col([dbc.CardBody([
            dbc.Button("Model Doğruluğu Hakkında", id="popover-bottom-target1", style={
                "text-decoration": "underline",  # overline
                'border': '2px solid #74a9cf',
                'cursor': 'pointer',
                'border-radius': '15px 50px', }),
            dbc.Popover([
                dbc.PopoverHeader("Gerçek Değer ile Tahmin Değerleri Kıyas"),
                dbc.PopoverBody(
                    dcc.Graph(id='actual_vs_predict_graph', figure={})
                ),
            ], id="popover1",
                target="popover-bottom-target1",
                placement="bottom",
                is_open=False,
                # style={"width":"400px", "height":"400px"}
            ),
        ]),
        ], xs=12, sm=12, md=1, lg=1, xl=1, className='buton1'),
        dbc.Col([dbc.CardBody([
            dbc.Button("Model Hakkında", id="popover-bottom-target", style={
                "text-decoration": "underline",  # overline
                'border': '2px solid #74a9cf',
                'cursor': 'pointer',
                'border-radius': '15px 50px', }),
            dbc.Popover([
                dbc.PopoverHeader("Ridge Regresyon"),
                dbc.PopoverBody(
                    "Çok değişkenli regresyon verilerini analiz etmede kullanılır. Amaç hata kareler toplamını minimize eden katsayıları, bu katsayılara bir ceza uygulayarak bulmaktır. Over-fittinge karşı dirençlidir. Çok boyutluluğa çözüm sunar. Tüm değişkenler ile model kurar, ilgisiz değişkenleri çıkarmaz sadece katsayılarını sıfıra yaklaştırır. Modeli kurarken alpha (ceza) için iyi bir değer bulmak gerekir."),
            ], id="popover",
                target="popover-bottom-target",
                placement="bottom",
                is_open=False,
            # style={'width':'450px', 'height':'450px'}
            )
        ],),
        ],style={"width":"150px"}, xs=12, sm=12, md=2, lg=2, xl=2),

    ], className='g-0'),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([dcc.Graph(id='left_indicator',figure={})],xs=12, sm=12, md=3, lg=3, xl=3),

        dbc.Col([dcc.Graph(id='map',figure={})],xs=12, sm=12, md=9, lg=9, xl=9),


    ],className='g-0'),
    dbc.Row([
        dbc.Col([], xs=12, sm=12, md=6, lg=6, xl=6),
        dbc.Col([html.P("...Yıl Seçiniz...")],
                style={'color': 'white','font-weight': 'bold'}, xs=12, sm=12, md=6, lg=6, xl=6),
        # dbc.Col([], xs=12, sm=12, md=1, lg=1, xl=1),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Slider(
            id='slct_year',  # any name you'd like to give it
            marks={
                2008: '2008',
                2009: '2009',
                2010: '2010',
                2011: '2011',
                2012: '2012',
                2013: '2013',
                2014: '2014',
                2015: '2015',
                2016: '2016',
                2017: '2017',
                2018: '2018',
                2019: '2019',
                2020: '2020',
                2021: '2021',
                2022: '2022',
                2023: '2023',
                2024: '2024',
                2025: '2025',
                2026: '2026',
                2027: '2027',
                2028: '2028',
                2029: '2029',
                2030: '2030',
            },
            value=2008,
            step=1,  # number of steps between values
            min=2008,
            max=2030,
        ),
    ], xs=12, sm=12, md=12, lg=12, xl=12),
]),
    dbc.Row([
        dbc.Col([dcc.Graph(id='bar_graph', figure={})],xs=12, sm=12, md=4, lg=4, xl=4),
        dbc.Col([dcc.Graph(id='line_graph', figure={})],xs=12, sm=12, md=4, lg=4, xl=4),
        dbc.Col([dcc.Graph(id='pie_graph', figure={})],xs=12, sm=12, md=4, lg=4, xl=4),

    ],className='g-0')

],style={'background-color':'#2b2b2b'},fluid=True)
#
@callback(
    Output("popover", "is_open"),
    Input("popover-bottom-target", "n_clicks"),
    State("popover", "is_open"),
)

def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


@callback(
    Output("popover1", "is_open"),
    Output("actual_vs_predict_graph", "figure"),
    Input("popover-bottom-target1", "n_clicks"),
    State("popover1", "is_open"),
)
def toggle_popover1(n, is_open):
    # Creating a scatter plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Gerçek Değerleri'))
    fig.add_trace(go.Scatter(x=x, y=predicted_values, mode='lines', name='Tahmin Değerleri'))

    # Adding labels and title
    fig.update_layout( xaxis_title='Yıl', yaxis_title='Nüfus',
                      margin={"r": 0, "t": 50, "l": 0, "b": 10},
                      # height = 450,
                      # width = 550,
                      plot_bgcolor="#2b2b2b",
                      paper_bgcolor="#2b2b2b",
                      font=dict(color="white")
                      )



    if n:
        return (not is_open), fig

    return is_open, fig




@callback(

    Output('left_indicator','figure'),
    Output('map','figure'),
    Output('bar_graph','figure'),
    Output('line_graph','figure'),
    Output('pie_graph','figure'),
    Input('slct_year', 'value'),

)

def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))



    if option_slctd <2022 and option_slctd >2007:
        # investor_str = """2008 - 2021 yılları arasındaki nüfus verileri TUİK tarafından paylaşılan verilerdir."""
        container = "{} Yılında ki İstanbul İlçe Nüfusları TUİK'yin yayınlamış olduğu veri setindeki değerlerdir.".format(option_slctd)
        group_df = pd.read_excel( r'./assets/ilce_nufus_toplam_cinsiyet_07_26.xls')
        group_df.sort_values(['ILCE', 'YIL'], ascending=[True, True], inplace=True)
        animated_nufus_copy = animated_nufus.copy()
        animated_nufus_copy = animated_nufus_copy[animated_nufus_copy["YIL"] == option_slctd]
        group_df_copy = group_df.copy()
        group_df_copy = group_df_copy[group_df_copy["YIL"] == option_slctd]
        il_nufus_copy = il_nufus.copy()
        il_nufus_copy = il_nufus_copy[il_nufus_copy["YIL"] == option_slctd]

        # LEFT INDICATOR
        top_nufus = il_nufus_copy['TOPLAM_NUFUS']
        fig_left_indicator = go.Figure(go.Indicator(
            title={
                'text': 'TOPLAM NÜFUS ({})'.format(option_slctd),
                'font': {'size': 17},
            },
            mode="number",
            value=int(top_nufus),

        ))
        fig_left_indicator.update_layout(plot_bgcolor="#2b2b2b", paper_bgcolor="#2b2b2b", font=dict(color="white"))


        # CHOROPLETH MAP
        fig = go.Figure()
        fig.add_trace(go.Scattermapbox(
            lat=ilce_nokta["Lat"],
            lon=ilce_nokta["Lon"],
            mode='text',
            textfont=dict(
                color="#252525",
                family='Arial',
                size=10,

            ),
            text=ilce_nokta["AD"],
            showlegend=False
        ))
        fig.add_trace(go.Choroplethmapbox(geojson=ist_districts,
                                          locations=animated_nufus_copy.ILCEKN,
                                          z=animated_nufus_copy["NUFUS"],
                                          customdata=animated_nufus_copy[['AD']].values.tolist(),
                                          hovertemplate="İlçe Adı: %{customdata}<br>Nüfus: %{z}<extra></extra>",
                                          showlegend=None,
                                          colorscale=[[0, "rgb(255, 255, 255)"],
                                                      [0.25, "rgb(144, 202, 249)"],
                                                      [0.5, "rgb(33, 150, 243)"],
                                                      [0.75, "rgb(25, 118, 210)"],
                                                      [1, "rgb(13, 71, 161)"]]))
        fig.update_layout(


            font=dict(color="white"),
            mapbox_style="mapbox://styles/abdulkerimnese/ckmeu15zk0m2f18np07gh8dwf",
            height = 400,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor='#2b2b2b',
            plot_bgcolor='#2b2b2b',
            mapbox=dict(center=dict(lat=41.1944, lon=28.9651), zoom=8, accesstoken=access_token,
                        # style="mapbox://styles/abdulkerimnese/ckmeu15zk0m2f18np07gh8dwf"
                        ))

        # BAR GRAPH

        fig_bar = px.bar(animated_nufus_copy.sort_values("NUFUS", ascending=False).head(10), x="NUFUS",
                         y='AD',
                         # color_discrete_map='identity',
                         color='NUFUS',
                         color_continuous_scale='blues',
                         orientation='h',
                         labels={'AD': 'İLÇE', 'NUFUS': 'NÜFUS', 'ERKEK_NUFUS': 'ERKEK NÜFUS'})

        fig_bar.update_layout(title=f'İSTANBUL İLÇE NÜFUSLARI ({option_slctd})', xaxis_tickfont_size=14,
                              # yaxis=dict(title='NÜFUS', titlefont_size=14, tickfont_size=14,),
                              xaxis_tickangle=320,
                              yaxis={'categoryorder': 'total ascending','title':'NÜFUS',
                                     'titlefont_size':14, 'tickfont_size':14},
                              # margin={"r": 0, "t": 0, "l": 0, "b": 0},
                              xaxis=dict(title='İLÇE', titlefont_size=14, tickfont_size=14),
                              plot_bgcolor="#2b2b2b",
                              paper_bgcolor="#2b2b2b",
                              font=dict(color="white"), xaxis_showgrid=False,
                              )
        # fig.update_xaxes(showline=False, linewidth=0.5, color='#969696')
        fig_bar.update_yaxes(showline=True, linewidth=0.5, linecolor='white')

        line_df = pd.read_excel(r'./assets/ridge_il_nufus_07_26_line.xls')
        line_df = line_df[line_df["YIL"] != 2007]
        line_df = line_df[line_df['YIL'] <= 2021]
        # line_df.sort_values(['ILCE', 'YIL'], ascending=[True, True], inplace=True)

        fig_line = px.line(line_df, x="YIL", y="value", color='gender', markers=True,
                           labels={'value': 'NÜFUS', 'gender': 'CİNSİYET'})
        #                 animation_frame='YIL',animation_group='ILCEKN',text='value')
        fig_line.update_layout(title='YILLARA GÖRE NÜFUS DEĞİŞİMİ', xaxis_tickfont_size=11,
                               yaxis=dict(title='NÜFUS', titlefont_size=14, tickfont_size=11),
                               xaxis=dict(title='YIL',tickmode='array', tickvals=line_df["YIL"],
                                ticktext=line_df["YIL"]),xaxis_tickangle=320,
                               #margin={"r": 0, "t": 0, "l": 0, "b": 0},
                               plot_bgcolor="#2b2b2b",
                               paper_bgcolor="#2b2b2b",
                               font=dict(color="white"), xaxis_showgrid=False)
        # fig.update_xaxes(showline=False, linewidth=0.5, color='#969696')
        fig_line.update_yaxes(showline=True, linewidth=0.5, linecolor='white')
        fig_line.update_traces(textposition="bottom right")

        # PIE GRAPH

        fig_pie = px.pie(group_df_copy, values='value', names='gender',hole=.6,
                         labels={'value': 'NÜFUS', 'gender': 'CİNSİYET', 'ILCE': 'İLÇE'},
                         # height=600

                         )
        fig_pie.update_layout(title=f'CİNSİYETE GÖRE TOPLAM NÜFUS ({option_slctd})', plot_bgcolor="#2b2b2b",
                              paper_bgcolor="#2b2b2b",
                              # margin={"r": 0, "t": 0, "l": 0, "b": 0},
                              font=dict(color="white"))

        return fig_left_indicator, fig, fig_bar, fig_pie, fig_line,

    else:

        container = "{} Yılında ki İlçe Nüfusları".format(option_slctd)
        # investor_str = """2008 - 2021 yılları arasındaki nüfus verileri TUİK tarafından paylaşılan verilerdir."""
        predict_option_slctd = ridge_tuned.predict([[option_slctd]])
        predict_option_slctd = predict_option_slctd.reshape(39, 3)
        predict_option_slctd = pd.DataFrame(predict_option_slctd)
        predict_option_slctd.columns = ["ERKEK_NUFUS", "KADIN_NUFUS", "NUFUS"]
        predict_option_slctd["YIL"] = option_slctd
        predict_option_slctd["AD"] = ['Adalar', 'Arnavutköy', 'Ataşehir', 'Avcılar', 'Bağcılar', 'Bahçelievler',
                                      'Bakırköy', 'Başakşehir', 'Bayrampaşa', 'Beşiktaş', 'Beykoz', 'Beylikdüzü',
                                      'Beyoğlu', 'Büyükçekmece', 'Çatalca', 'Çekmeköy', 'Esenler', 'Esenyurt',
                                      'Eyüpsultan', 'Fatih', 'Gaziosmanpaşa', 'Güngören', 'Kadıköy', 'Kağıthane',
                                      'Kartal', 'Küçükçekmece', 'Maltepe', 'Pendik', 'Sancaktepe', 'Sarıyer', 'Silivri',
                                      'Sultanate', 'Sultangazi', 'Şile', 'Şişli', 'Tuzla', 'Ümraniye', 'Üsküdar',
                                      'Zeytinburnu']
        predict_option_slctd["ILCEKN"] = ['1103', '2048', '2049', '2003', '2004', '2005', '1166', '2050', '1886',
                                          '1183', '1185', '2051', '1186', '1782', '1237', '2052', '2016', '2053',
                                          '1325', '1327', '1336', '2010', '1421', '1810', '1449', '1823', '2012',
                                          '1835', '2054', '1604', '1622', '2014', '2055', '1659', '1663', '2015',
                                          '1852', '1708', '1739']


        float_col = predict_option_slctd.select_dtypes(include=['float64'])
        for col in float_col.columns.values:
            predict_option_slctd[col] = predict_option_slctd[col].astype('int64')

        predict_option_slctd_indicator = predict_option_slctd.groupby(['YIL']).sum()

        predict_option_slctd_pie = predict_option_slctd.drop(columns=['ILCEKN', 'YIL', 'NUFUS'])
        predict_option_slctd_pie.rename(columns={'ERKEK_NUFUS': 'ERKEK', 'KADIN_NUFUS': 'KADIN'}, inplace=True)
        predict_option_slctd_pie = pd.melt(predict_option_slctd_pie, id_vars=['AD'], var_name='gender',value_name='value')

        # predict_option_slctd.to_excel(r"C:\Users\abdulkerim.nese\Desktop\2026-2030-nufus\{}_nufus.xlsx".format(option_slctd))

        # LEFT INDICATOR
        top_nufus = predict_option_slctd_indicator['NUFUS']
        fig_left_indicator = go.Figure(go.Indicator(
            title={
                'text': 'TOPLAM NÜFUS ({})'.format(option_slctd),
                'font': {'size': 17},
            },
            mode="number",
            value=int(top_nufus),

        ))
        fig_left_indicator.update_layout(plot_bgcolor="#2b2b2b", paper_bgcolor="#2b2b2b", font=dict(color="white"))

        # CHOROPLETH MAP
        fig = go.Figure()
        fig.add_trace(go.Scattermapbox(
            lat=ilce_nokta["Lat"],
            lon=ilce_nokta["Lon"],
            mode='text',
            textfont=dict(
                color="#252525",
                family='Arial',
                size=10,

            ),
            text=ilce_nokta["AD"],
            showlegend=False
        ))
        fig.add_trace(go.Choroplethmapbox(geojson=ist_districts,
                                          locations=predict_option_slctd.ILCEKN,
                                          z=predict_option_slctd["NUFUS"],
                                          customdata=predict_option_slctd[['AD']].values.tolist(),
                                          hovertemplate="İlçe Adı: %{customdata}<br>Nüfus: %{z}<extra></extra>",
                                          showlegend=None,
                                          colorscale=[[0, "rgb(255, 255, 255)"],
                                                      [0.25, "rgb(144, 202, 249)"],
                                                      [0.5, "rgb(33, 150, 243)"],
                                                      [0.75, "rgb(25, 118, 210)"],
                                                      [1, "rgb(13, 71, 161)"]]))
        fig.update_layout(
            font=dict(color="white"),
            mapbox_style="mapbox://styles/abdulkerimnese/ckmeu15zk0m2f18np07gh8dwf",
            height=400,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            paper_bgcolor='#2b2b2b',
            plot_bgcolor='#2b2b2b',
            mapbox=dict(center=dict(lat=41.1944, lon=28.9651), zoom=8, accesstoken=access_token,
                        # style="mapbox://styles/abdulkerimnese/ckmeu15zk0m2f18np07gh8dwf"
                        ))

        # BAR GRAPH
        fig_bar = px.bar(predict_option_slctd.sort_values("NUFUS", ascending=False).head(10), x="NUFUS",
                         y='AD',
                         color = "NUFUS",
                         color_continuous_scale='blues', orientation='h',
                         labels={'AD': 'İLÇE', 'NUFUS': 'NÜFUS', 'ERKEK_NUFUS': 'ERKEK NÜFUS'})

        fig_bar.update_layout(title=f'İLÇE NÜFUSLARI ({option_slctd})', xaxis_tickfont_size=14,
                              # yaxis=dict(title='NÜFUS', titlefont_size=14, tickfont_size=14),
                              yaxis={'categoryorder': 'total ascending', 'title': 'NÜFUS',
                                     'titlefont_size': 14, 'tickfont_size': 14},
                              xaxis_tickangle=320,
                              # margin={"r": 0, "t": 0, "l": 0, "b": 0},
                              xaxis=dict(title='İLÇE', titlefont_size=14, tickfont_size=14),
                              plot_bgcolor="#2b2b2b",
                              paper_bgcolor="#2b2b2b",
                              font=dict(color="white"), xaxis_showgrid=False)
        # fig.update_xaxes(showline=False, linewidth=0.5, color='#969696')
        fig_bar.update_yaxes(showline=True, linewidth=0.5, linecolor='white')

        line_df = pd.read_excel(r'./assets/ridge_il_nufus_07_26_line.xls')
        line_df = line_df[line_df["YIL"] != 2007]
        line_df = line_df[line_df['YIL'] <= option_slctd]

        fig_line = px.line(line_df, x="YIL", y="value", color='gender', markers=True,
                           labels={'value': 'NÜFUS', 'gender': 'CİNSİYET'})
        #                 animation_frame='YIL',animation_group='ILCEKN',text='value')
        fig_line.update_layout(title='İSTANBUL İLİNİN YILLARA GÖRE NÜFUS DEĞİŞİMİ', xaxis_tickfont_size=14,
                               yaxis=dict(title='NÜFUS', titlefont_size=14, tickfont_size=14),
                               xaxis=dict(title='YIL',
                                          tickmode='array', tickvals=line_df["YIL"], ticktext=line_df["YIL"]),
                               xaxis_tickangle=320,
                               #                           margin={"r": 0, "t": 0, "l": 0, "b": 0},
                               plot_bgcolor="#2b2b2b",
                               paper_bgcolor="#2b2b2b",
                               font=dict(color="white"), xaxis_showgrid=False)
        # fig.update_xaxes(showline=False, linewidth=0.5, color='#969696')
        fig_line.update_yaxes(showline=True, linewidth=0.5, linecolor='white')
        fig_line.update_traces(textposition="bottom right")

        # PIE GRAPH

        fig_pie = px.pie(predict_option_slctd_pie, values='value', names='gender',hole=.6,
                         labels={'value': 'NÜFUS', 'gender': 'CİNSİYET', 'ILCE': 'İLÇE'},
                         # height=600

                         )
        fig_pie.update_layout(title=f'CİNSİYETE GÖRE TOPLAM NÜFUS ({option_slctd})', plot_bgcolor="#2b2b2b",
                              paper_bgcolor="#2b2b2b",
                              # margin={"r": 0, "t": 0, "l": 0, "b": 0},
                              font=dict(color="white"))

        return fig_left_indicator, fig, fig_bar, fig_pie, fig_line



