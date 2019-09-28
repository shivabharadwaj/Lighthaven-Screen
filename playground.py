from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import dash_ui as dui
from dash.dependencies import Input, Output
import datetime
from dateutil.relativedelta import relativedelta
import yfinance as yf
import plotly.graph_objects as go

app = Dash()
external_stylesheets = ['https://codepen.io/rmarren1/pen/mLqGRg.css']
app = Dash(__name__, external_stylesheets=external_stylesheets, )

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

graph_test = dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )

app.layout = html.Div([
    dcc.Input(id = 'ticker', value = 'AMZN', type = 'text'),
    html.Div(id = 'testing'),
   # dui.Layout(
   #     grid=grid,
   # )
    # style={
    #     'height': '100vh',
    #     'width': '100vw'
    # }
])

@app.callback(
    Output(component_id='testing', component_property='children'),
    [Input(component_id='ticker', component_property='value')]
)

def update_page(input_value):
    start = datetime.datetime.today() - relativedelta(years=5)
    end = datetime.datetime.today()

    try:
        price_data = yf.download(input_value, start, end)
    except:
        trace_close = go.Scatter(x=list(price_data.index), y = list(price_data.Close), name = "close",
                                 line = dict(color="#03b1fc"))
        data = [trace_close]
        layout = dict(title="Stock Chart for " + input_value, showlegend = False)
        fig = dict(data=data, layout=layout)
        graph_test = dcc.Graph(id="Stock Graph", figure=fig)

    grid.add_element(col=2, row=2, width=5, height=5, element=(graph_test))




    grid = dui.Grid(_id="grid", num_rows=12, num_cols=12, grid_padding=0)

    grid.add_element(col=4, row=1, width=8, height=1, element=html.Div(
        style={"background-color": "orange", "height": "100%", "width": "100%"}
    ))

    grid.add_element(col=7, row=2, width=5, height=2, element=html.Div(
        style={"background-color": "green", "height": "100%", "width": "100%"}
    ))

    grid.add_element(col=7, row=4, width=5, height=3, element=html.Div(
        style={"background-color": "red", "height": "100%", "width": "100%"}
    ))

    grid.add_element(col=2, row=7, width=5, height=3, element=html.Div(
        style={"background-color": "green", "height": "100%", "width": "100%"}
    ))

    grid.add_element(col=7, row=7, width=5, height=2, element=html.Div(
        style={"background-color": "blue", "height": "100%", "width": "100%"}
    ))

    grid.add_element(col=2, row=9, width=5, height=2, element=html.Div(
        style={"background-color": "orange", "height": "100%", "width": "100%"}
    ))

    grid.add_element(col=7, row=9, width=5, height=2, element=html.Div(
        style={"background-color": "purple", "height": "100%", "width": "100%"}
    ))

    grid.add_element(col=2, row=11, width=5, height=2, element=html.Div(
        style={"background-color": "red", "height": "100%", "width": "100%"}
    ))

    grid.add_element(col=7, row=11, width=5, height=2, element=html.Div(
        style={"background-color": "yellow", "height": "100%", "width": "100%"}
    ))

    return dui.Layout( grid=grid)


if __name__ == "__main__":
    app.run_server(debug=True)