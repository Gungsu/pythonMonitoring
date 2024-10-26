import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash(__name__)
fig = go.Figure(data=go.Scatter(x=[], y=[]))

bkColor = '#0c343d'

app.layout = html.Div(
    style={'backgroundColor': bkColor},
    children=[
    html.H1(children = "Comparação de sensores!", style={"textAlign": 'center','color':'white'}),
    dcc.Graph(id='live-graph', figure=fig),
    dcc.Interval(
        id='interval-component',
        interval=1*500, # em milissegundos
        n_intervals=0
    )
])

@app.callback(
    Output('live-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph_live(n):
    # Gerar novos dados aqui (substitua por seus próprios dados)
    fig = go.Figure(data=go.Scatter(x=[], y=[]),layout_yaxis_range=[0,4000],
                    layout={
                        'title': "Comparação de medidas",
                        'plot_bgcolor': '#D3D3D3',
                        'paper_bgcolor': bkColor,
                        'font' : {
                            'color':'#FFFFFF'
                        },
                        'height': 800
                        })
    df = pd.read_csv('arquivo.csv')
    numberSens = (len(df.keys())-1)*-1
    sensores = list(df.keys()[numberSens:])
    #print(sensores)
    for sen in sensores:
        fig.add_scatter(x=df['tempo'][-30:], y=df[sen][-30:], mode='lines',name=sen)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True,port=8050)