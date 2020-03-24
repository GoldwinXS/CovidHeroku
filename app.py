import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

from PlotlyGraphs import make_plot_for_all_countries

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

""" 
WEB LOCATION

https://ncov19-visualization.herokuapp.com/ | https://git.heroku.com/ncov19-visualization.git


"""
case = 'Deaths'
country = 'Canada'

fig = make_plot_for_all_countries(case)

""" PREPARE APP """

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([

    html.H2('COVID-19 Data Visualization by Goldwin Stewart'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['Recovered', 'Deaths', 'Confirmed', 'Active']],
        value=case),
    dcc.Graph(id='test'),

    html.Div(id='display-value'),
])


@app.callback(Output('display-value', 'children'), [Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


@app.callback(Output('test', 'figure'), [Input('dropdown', 'value')])
def change_case(value):
    fig = make_plot_for_all_countries(value)
    return fig


# app.run_server()

if __name__ == '__main__':
    app.run_server(debug=True)
