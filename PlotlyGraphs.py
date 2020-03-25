import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
import numpy as np
from scipy.optimize import curve_fit

""" LOAD DATA """
ncov = pd.read_csv('COVID-19 Cases.csv', parse_dates=['Date'])


def prepare_country_color_dict():
    """ Prepares a dictionary for plotly objects """
    get_rand = lambda: np.random.randint(55, 255)
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
    test_df = get_df_for_country(get_df_for_case(case), country)

    data = [get_scatter(test_df['Date'], test_df['Cases'], country)]
    layout = go.Layout(plot_bgcolor='#1a1c23', title='test')

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


def find_max_y_vals(plotly_go_obj):
    m = 0
    for elem in plotly_go_obj:
        if max(elem['y']) > m:
            m = max(elem['y'])
    return m


def make_subplot(case1, case2):
    """ Makes a subplot of multiple plots. Hard-coded right now. """

    sub_plts = make_subplots(
        rows=1,
        cols=2,
    )

    data1 = make_plot_for_all_countries(case1, show_legend=True)['data']
    data2 = make_plot_for_all_countries(case2, show_legend=False)['data']

    max_1 = find_max_y_vals(data1)
    max_2 = find_max_y_vals(data2)

    max_y_range = max(max_1, max_2)
    min_y_range = min(max_1, max_2)

    y_range = (max_y_range + min_y_range) // 2

    def append_traces(data, row, col):
        for i in range(len(data)):
            sub_plts.append_trace(data[i], row, col)

    append_traces(data1, row=1, col=1)
    append_traces(data2, row=1, col=2)

    sub_plts.update_layout(height=700, title_text="Side By Side Comparison: ")
    sub_plts.layout.plot_bgcolor = '#1a1c23'
    sub_plts.update_layout(paper_bgcolor="#1a1c23")
    sub_plts.update_layout(font={'color': 'white'})
    sub_plts.update_layout(yaxis={'range': [0, y_range]},
                           yaxis2={'range': [0, y_range]})

    return sub_plts


def make_model_fit_plot(case, country):
    data = make_plot_for_country(case, country)

    data.update_layout(height=700, title_text="Model fit: ")
    data.layout.plot_bgcolor = '#1a1c23'
    data.update_layout(paper_bgcolor="#1a1c23")
    data.update_layout(font={'color': 'white'})

    return data


def exponential_model(x, a, b):
    return a * b ** x


def model(case, country):
    data = get_df_for_country(get_df_for_case(case), country)
    fit_data = data.Cases

    uncertainty = [0.1] * fit_data.shape[0]
    x = np.arange(fit_data.shape[0])
    y = fit_data.tolist()

    init_guess = [1, 1]

    fit = curve_fit(exponential_model,
                    x,
                    y,
                    sigma=uncertainty,
                    p0=init_guess,
                    absolute_sigma=True)

    fit = tuple(fit[0])

    days_to_future_predict = 0

    data_age = 5
    pred_length = 57 + data_age + days_to_future_predict
    model_shift = 10

    # previous_n_days = fit_data.shape[0]
    print('predicting {} days into the future.'.format(days_to_future_predict))
    new_x = np.arange(pred_length)
    y = data.tolist()[:pred_length]
    model_predictions = [model(pt, *fit) for pt in new_x]
    shifted_model_predictions = [model(p + model_shift, *fit) for p in new_x]

    # if len(y) < len(new_x):
    #     y = y + [None] * (len(new_x) - len(y))

    # df = pd.DataFrame({"x": new_x,
    #                    'model_predictions': model_predictions,
    #                    'shifted_model_predictions': shifted_model_predictions,
    #                    'y': y,
    #                    'canada_pop': [35000000 for _ in range(len(y))]})
    # melted_df = df.melt(id_vars='x')

    return fit
