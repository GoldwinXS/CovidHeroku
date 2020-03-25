import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
import numpy as np

""" LOAD DATA """
ncov = pd.read_csv('COVID-19 Cases.csv', parse_dates=['Date'])


def prepare_country_color_dict():
    """ Prepares a dictionary for plotly objects """
    get_rand = lambda: np.random.randint(0, 255)
    random_colors_rgb = [(get_rand(), get_rand(), get_rand()) for _ in range(len(ncov.Country_Region.unique()))]
    return {country: 'rgba' + str(color + (1,)) for country, color in
            zip(ncov.Country_Region.unique(), random_colors_rgb)}


country_color_dict = prepare_country_color_dict()


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
                     marker={'color': country_color_dict[name]},
                     name=name,
                     legendgroup=name,
                     showlegend=show_legend)
    return obj


def make_plot_for_country(case, country):
    """
    Returns figure data for a single country.

    @param country: str of country
    @type case: str to describe what data we're looking at
    """
    test_df = get_df_for_country(get_df_for_case('Active'), country)

    data = [get_scatter(test_df['Date'], test_df['Cases'], case)]
    layout = go.Layout(plot_bgcolor='#111111', title='test')
    # layout = {
    #     'title': 'test',
    #     'plot_bgcolor': '#111111',
    #     'paper_bgcolor': '#111111',
    #     'font': {'color': '#7FDBFF'}
    # }
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


def shift_dates_to_match(df):
    pivoted = df.pivot(index='Date', columns='Country_Region')
    pivoted = pivoted.reset_index()

    def shift_column(country):
        case_df = pivoted['Cases']
        # shift_amt = case_df.shape[0]-case_df.dropna().shape[0]
        non_nan_vals = case_df['Algeria'][case_df['Algeria'].fillna(0) != 0]
        case_df = case_df['Algeria'].shift(case_df.shape[0])
        case_df.iloc[:, :non_nan_vals.shape[0]] = non_nan_vals
        # case_df = case_df.shift(int(-shift_amt))
        pivoted['Cases'][country] = case_df

    for country in df['Cases']:
        shift_column(country)

    # shift_col = lambda country,shift_amt:pivoted['Cases']
    return df


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

    sub_plts.update_layout(height=700, title_text="Side By Side Comparison: ")
    sub_plts.layout.plot_bgcolor = '#1a1c23'
    sub_plts.update_layout(paper_bgcolor="#1a1c23")

    return sub_plts


make_plot_for_all_countries('Deaths', show_legend=True)
