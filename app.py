import dash
import dash_core_components as dcc
from dash_core_components import Dropdown

import dash_html_components as html
from dash_html_components import Div, P
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_components import Row, Col
from PlotlyGraphs import make_plot_for_all_countries, make_subplot

""" 
WEB LOCATION

https://ncov19-visualization.herokuapp.com/ | https://git.heroku.com/ncov19-visualization.git

"""

""" SETUP SOME INITIAL VARS """

cases = ['Deaths', 'Active']
country = 'Canada'
# fig = make_plot_for_all_countries(case)
explanatory_text = 'Visualize Covid-19 Data with me!'

""" PREPARE APP """

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = Div([

    html.H2('COVID-19 Data Visualization by Goldwin Stewart', style={'textAlign': 'center'}),
    Row([Col(Div(P(explanatory_text)))], justify='center'),

    Row([
        Col(
            Div(
                Dropdown(
                    id='dropdown',
                    options=[{'label': i, 'value': i} for i in ['Recovered', 'Deaths', 'Confirmed', 'Active']],
                    value=cases[0])), width=3),

        Col(
            Div(
                Dropdown(
                    id='dropdown2',
                    options=[{'label': i, 'value': i} for i in ['Recovered', 'Deaths', 'Confirmed', 'Active']],
                    value=cases[1])), width=3),

    ], justify='around'),

    # html.Div(id='display-value'),
    dcc.Graph(id='test'),
])


# @app.callback(Output('display-value', 'children'), [Input('dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)


@app.callback(Output('test', 'figure'), [Input('dropdown', 'value'), Input('dropdown2', 'value')])
def change_case(value1, value2):
    fig = make_subplot(value1, value2)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
