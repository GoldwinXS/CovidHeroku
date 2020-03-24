import plotly.graph_objs as go
import pandas as pd

""" LOAD DATA """
ncov = pd.read_csv('COVID-19 Cases.csv', parse_dates=['Date'])


def get_df_for_case(case):
    """
    Prepares a df for a specific case such as Deaths, Recovered, Active, and Confirmed

    @type case: str
    """

    # get specific case
    specific_ncov = ncov[ncov['Case_Type'] == case]

    # get all for which cases > 10
    specific_ncov = specific_ncov[specific_ncov['Cases'] > 10]

    # remove regions
    specific_ncov = specific_ncov.groupby(by=['Country_Region', 'Date', 'Case_Type']).sum().reset_index()

    # sort the dates for plotly
    specific_ncov.sort_values(by='Date', inplace=True)

    return specific_ncov


def get_df_for_country(df, country):
    """
    A convenience function to return a df of a specified country

    @param country: str of country name
    @type df: pd.Dataframe
    """
    return df[df['Country_Region'] == country]


def get_scatter(x, y, name):
    """
    A function to abstract some Plotly interface.

    @param name: str name for the scatter plot
    @param y: pd.Series of the y values for this plot. Can be time in pd.datetime form
    @type x: pd.Series of the x values for this plot. Can be time in pd.datetime form
    """
    obj = go.Scatter(x=x,
                     y=y,
                     mode='lines',
                     name=name
                     )
    return obj


def make_plot_for_country(case, country):
    """ Returns figure data for a single country.

    @param country: str of country
    @type case: str to describe what data we're looking at
    """
    test_df = get_df_for_country(get_df_for_case('Active'), country)

    data = [get_scatter(test_df['Date'], test_df['Cases'], case)]
    layout = {
        'title': 'test',
    }
    fig = go.Figure(data=data, layout=layout)

    return fig


def make_plot_for_all_countries(case):
    """
    A function that returns a dict for a plotly figure.

    @type case: str represents what case to grab for all countries
    """
    df = get_df_for_case(case)
    countries = df['Country_Region'].unique()

    data = []

    for country in countries:
        country_df = get_df_for_country(df, country)
        data.append(get_scatter(country_df['Date'], country_df['Cases'], country))

    layout = {'title': '{} for all countries.'.format(case)}
    return dict(data=data, layout=layout)

















