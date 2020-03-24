import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots

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


def get_scatter(x, y, name, show_legend=True):
    """
    A function to abstract some Plotly interface.

    @param name: str name for the scatter plot
    @param y: pd.Series of the y values for this plot. Can be time in pd.datetime form
    @type x: pd.Series of the x values for this plot. Can be time in pd.datetime form
    """
    obj = go.Scatter(x=x,
                     y=y,
                     mode='lines',
                     name=name,
                     legendgroup=name,
                     showlegend=show_legend)
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


def make_plot_for_all_countries(case, show_legend):
    """
    A function that returns a dict for a plotly figure using covid 19 data.

    @type show_legend: bool to represent if we draw the legend or not
    @type case: str represents what case to grab for all countries
    """
    df = get_df_for_case(case)
    countries = df['Country_Region'].unique()

    data = []

    for country in countries:
        country_df = get_df_for_country(df, country)
        data.append(get_scatter(country_df['Date'], country_df['Cases'], country, show_legend))

    layout = {'title': '{} for all countries.'.format(case)}
    return dict(data=data, layout=layout)


def make_subplot(case1, case2):
    """ Makes a subplot of multiple plots. Hard-coded right now. """

    sub_plts = make_subplots(
        rows=1,
        cols=2,
    )

    data1 = make_plot_for_all_countries(case1, show_legend=True)['data']
    data2 = make_plot_for_all_countries(case2, show_legend=False)['data']

    def append_traces(data, row, col):
        for i in range(len(data)):
            sub_plts.append_trace(data[i], row, col)

    append_traces(data1, row=1, col=1)
    append_traces(data2, row=1, col=2)

    sub_plts.update_layout(height=600, title_text="Side By Side Comparison: ")
    return sub_plts
