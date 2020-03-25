import dash
import dash_core_components as dcc
from dash_core_components import Dropdown

import dash_html_components as html
from dash_html_components import Div, P
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_components import Row, Col
from PlotlyGraphs import make_subplot, make_model_fit_plot, ncov

""" 
WEB LOCATION

https://ncov19-visualization.herokuapp.com/ | https://git.heroku.com/ncov19-visualization.git

"""

""" SETUP SOME INITIAL VARS """

cases = ['Deaths', 'Active']
country = 'Canada'
explanatory_text = """

Welcome to my data exploration of **Covid-19!** 

Let's take a look at the data together to try and understand what's going on!



"""
markdown_text = """ 




## Fit a model to the data! ##

Try it out by adjusting the parameters.




"""

""" PREPARE APP """

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = Div([

    Div(html.H2('COVID-19 Data Visualization and Modeling', style={'textAlign': 'center'}),
        className='app-header'),

    Row([Col(Div(P(explanatory_text, style={'textAlign': 'center'})), className='background')]),

    Row([
        Col(
            Div(
                Dropdown(
                    id='dropdown',
                    options=[{'label': i, 'value': i} for i in ['Recovered', 'Deaths', 'Confirmed', 'Active']],
                    value=cases[0]), className='button'), width=3),
        Col(
            Div(
                Dropdown(
                    id='dropdown2',
                    options=[{'label': i, 'value': i} for i in ['Recovered', 'Deaths', 'Confirmed', 'Active']],
                    value=cases[1]), className='button'), width=3),

    ], justify='around', ),

    dcc.Graph(id='test'),

    dcc.Markdown(markdown_text,id = 'MarkdownText', style={'textAlign': 'center', 'backgroudColor': '#1a1c23'}),

    Row([
        Col(
            Div(
                Dropdown(id='country-selection',
                         options=[{'label': i, 'value': i} for i in ncov.Country_Region.unique()],
                         value='Canada',
                         className='button')
            )
        ),
        Col(
            Div(
                Dropdown(id='case-selection',
                         options=[{'label': i, 'value': i} for i in ['Recovered', 'Deaths', 'Confirmed', 'Active']],
                         value='Recovered',
                         className='button')
            )
        )
    ]),

    # html.Div(id='display-value'),

    Div(dcc.Graph(id='model-fit')),

], id='Main')


@app.callback(Output('test', 'figure'), [Input('dropdown', 'value'), Input('dropdown2', 'value')])
def change_case(value1, value2):
    fig = make_subplot(value1, value2)
    return fig


@app.callback(Output('model-fit', 'figure'), [Input('case-selection', 'value'), Input('country-selection', 'value')])
def make_model(value1, value2):
    fig = make_model_fit_plot(value1, value2)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
