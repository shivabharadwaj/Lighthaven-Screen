from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import dash_ui as dui
# this is a test
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

grid = dui.Grid(_id="grid", num_rows=12, num_cols=12, grid_padding=0)

grid.add_element(col=1, row=1, width=3, height=4, element=(graph_test))

grid.add_element(col=4, row=1, width=9, height=4, element=html.Div(
    style={"background-color": "blue", "height": "100%", "width": "100%"}
))

grid.add_element(col=1, row=5, width=12, height=4, element=html.Div(
    style={"background-color": "green", "height": "100%", "width": "100%"}
))

grid.add_element(col=1, row=9, width=9, height=4, element=html.Div(
    style={"background-color": "orange", "height": "100%", "width": "100%"}
))

grid.add_element(col=10, row=9, width=3, height=4, element=html.Div(
    style={"background-color": "purple", "height": "100%", "width": "100%"}
))


app.layout = html.Div(
    dui.Layout(
        grid=grid,
    ),
    style={
        'height': '100vh',
        'width': '100vw'
    }
)



if __name__ == "__main__":
    app.run_server(debug=True)