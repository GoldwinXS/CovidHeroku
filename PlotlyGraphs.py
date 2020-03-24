# import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import plotly

""" LOAD DATA """
ncov = pd.read_csv('COVID-19 Cases.csv', parse_dates=['Date'])


def remove_regions(df):
    df = df.groupby(['Date', 'Country_Region']).sum().reset_index()
    return df


def get_df_for_case(case, remove_regions=True):
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
    return df[df['Country_Region'] == country]


def get_scatter(x, y, name):
    obj = go.Scatter(x=x,
                     y=y,
                     mode='lines',
                     name=name
                     )
    return obj


def make_plot(case, country):
    test_df = get_df_for_country(get_df_for_case('Active'), country)

    data = [get_scatter(test_df['Date'], test_df['Cases'], case)]
    layout = {
        'title': 'test'
    }
    fig = go.Figure(data=data, layout=layout)

    return fig


def make_plot_for_all_countries(case):
    df = get_df_for_case(case)
    countries = df['Country_Region'].unique()

    data = []

    for country in countries:
        country_df = get_df_for_country(df, country)
        data.append(get_scatter(country_df['Date'], country_df['Cases'], country))

    layout = {'title': 'Cases of {} for all countries.'.format(case)}
    # fig = go.Figure(data=data, layout=layout)
    return dict(data=data, layout=layout)

# fig = make_plot('Active','Canada')
