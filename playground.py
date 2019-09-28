import dash_table
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import dash_ui as dui
from dash.dependencies import Input, Output, State
import datetime
from dateutil.relativedelta import relativedelta
import yfinance as yf
import plotly.graph_objects as go
import requests
import pandas as pd
from Screening_Logic import execute

app = Dash()
external_stylesheets = ['https://codepen.io/rmarren1/pen/mLqGRg.css']
app = Dash(__name__, external_stylesheets=external_stylesheets, )

colors = {
    'background': '#050505',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    dcc.Input(id = 'ticker', value = 'AMZN', type = 'text'),
    html.Button('Screen!', id='button'),
    html.Div(id = 'testing'),
])

# @app.callback(
#     Output(component_id='testing', component_property='children'),
#     [Input(component_id='ticker', component_property='value')]
# )

@app.callback(
    Output('testing', 'children'),
    [Input('button', 'n_clicks')],
    [State('ticker', 'value')])

def update_page(n_clicks, ticker):
    grid = dui.Grid(_id="grid", num_rows=12, num_cols=12, grid_padding=0)

    # Black Border
    grid.add_element(col=1, row=1, width=12, height=1, element=html.Div(
        style={"background-color": "black", "height": "100%", "width": "100%"}
    ))

    grid.add_element(col=1, row=12, width=12, height=1, element=html.Div(
        style={"background-color": "black", "height": "100%", "width": "100%"}
    ))

    grid.add_element(col=1, row=2, width=1, height=10, element=html.Div(
        style={"background-color": "black", "height": "100%", "width": "100%"}
    ))

    grid.add_element(col=12, row=2, width=1, height=10, element=html.Div(
        style={"background-color": "black", "height": "100%", "width": "100%"}
    ))

    # Stock Chart
    start = datetime.datetime.today() - relativedelta(years=5)
    end = datetime.datetime.today()

    try:
        price_data = yf.download(ticker, start, end)
    except:
        return "Could not get data"
    trace_close = go.Scatter(x=list(price_data.index), y=list(price_data.Close), name="close",
                             line=dict(color="#03b1fc"))
    data = [trace_close]
    layout = dict(title=ticker + " - Historic Stock Price", showlegend=False)
    fig = dict(data=data, layout=layout)
    stock_chart = dcc.Graph(id="Stock Graph", figure=fig)

    grid.add_element(col=2, row=2, width=6, height=5, element=(stock_chart))

    # Company Description
    def find_description(list):
        test = []
        for item in list:
            if (len(item) > 100):
                test.append(item)
        return test
    try:
        page = requests.get('https://finance.yahoo.com/quote/' + ticker + '/profile?p=' + ticker)
        from lxml import html as html2
        tree = html2.fromstring(page.content)
        data = tree.xpath('//p/text()')
        description = find_description(data)[0]
        description = str(description)
        description_output = html.Div([html.H1('Company Description'),
                                       html.P(description)])
    except:
        description_output = html.Div([html.P("Could not find description")])

    grid.add_element(col=8, row=2, width=4, height=6, element=description_output)

    grid.add_element(col=8, row=7, width=4, height=5, element=html.Div(
        style={"background-color": "yellow", "height": "100%", "width": "100%"}
    ))

    fast_df = execute(ticker)[0]
    fast = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in fast_df.columns],
        data=fast_df.to_dict('records'),
        style_cell = {'textAlign' : 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {
                    'column_id': 'Status',
                    'filter_query': '{Status} eq "True"'
                },
                'backgroundColor': '#ACFC6A',
                'color': 'black',
            },
            {
                'if': {
                    'column_id': 'Status',
                    'filter_query': '{Status} eq "False"'
                },
                'backgroundColor': '#FF8787',
                'color': 'black',
            },
            {
                'if': {
                    'column_id': 'Status'},
                'width': '25%'
            }
        ],
    )

    grid.add_element(col=2, row=7, width=3, height=3, element=fast)

    stalwart_df = execute(ticker)[1]
    stalwart = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in stalwart_df.columns],
        data=stalwart_df.to_dict('records'),
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {
                    'column_id': 'Status',
                    'filter_query': '{Status} eq "True"'
                },
                'backgroundColor': '#ACFC6A',
                'color': 'black',
            },
            {
                'if': {
                    'column_id': 'Status',
                    'filter_query': '{Status} eq "False"'
                },
                'backgroundColor': '#FF8787',
                'color': 'black',
            },
            {
                'if': {
                    'column_id': 'Status'},
                'width': '25%'
            }
        ],
    )

    grid.add_element(col=2, row=9, width=3, height=2, element=stalwart)

    surfer_df = execute(ticker)[2]
    surfer = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in surfer_df.columns],
        data=surfer_df.to_dict('records'),
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {
                    'column_id': 'Status',
                    'filter_query': '{Status} eq "True"'
                },
                'backgroundColor': '#ACFC6A',
                'color': 'black',
            },
            {
                'if': {
                    'column_id': 'Status',
                    'filter_query': '{Status} eq "False"'
                },
                'backgroundColor': '#FF8787',
                'color': 'black',
            },
            {
                'if': {
                    'column_id': 'Status'},
                'width': '25%'
            }
        ],
    )

    grid.add_element(col=2, row=11, width=3, height=2, element=surfer)

    dead_df = execute(ticker)[3]
    dead = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in dead_df.columns],
        data=dead_df.to_dict('records'),
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {
                    'column_id': 'Status',
                    'filter_query': '{Status} eq "True"'
                },
                'backgroundColor': '#ACFC6A',
                'color': 'black',
            },
            {
                'if': {
                    'column_id': 'Status',
                    'filter_query': '{Status} eq "False"'
                },
                'backgroundColor': '#FF8787',
                'color': 'black',
            },
            {
                'if': {
                    'column_id': 'Status'},
                'width': '25%'
            }
        ],
    )

    grid.add_element(col=5, row=7, width=3, height=2, element=dead)

    fad_df = execute(ticker)[4]
    fad = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in fad_df.columns],
        data=fad_df.to_dict('records'),
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {
                    'column_id': 'Status',
                    'filter_query': '{Status} eq "True"'
                },
                'backgroundColor': '#ACFC6A',
                'color': 'black',
            },
            {
                'if': {
                    'column_id': 'Status',
                    'filter_query': '{Status} eq "False"'
                },
                'backgroundColor': '#FF8787',
                'color': 'black',
            },
            {
                'if': {
                    'column_id': 'Status'},
                'width': '25%'
            }
        ],
    )

    grid.add_element(col=5, row=9, width=3, height=2, element=fad)

    hot_df = execute(ticker)[5]
    hot = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in hot_df.columns],
        data=hot_df.to_dict('records'),
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {
                    'column_id': 'Status',
                    'filter_query': '{Status} eq "True"'
                },
                'backgroundColor': '#ACFC6A',
                'color': 'black',
            },
            {
                'if': {
                    'column_id': 'Status',
                    'filter_query': '{Status} eq "False"'
                },
                'backgroundColor': '#FF8787',
                'color': 'black',
            },
            {
                'if': {
                    'column_id': 'Status'},
                    'width': '25%'
            }
        ],
    )

    grid.add_element(col=5, row=11, width=3, height=2, element=hot)

    return dui.Layout( grid=grid)

if __name__ == "__main__":
    app.run_server(debug=True)