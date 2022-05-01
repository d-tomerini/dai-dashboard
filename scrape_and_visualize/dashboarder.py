from dash import Dash, html, dcc, dash_table, Input, Output, State, callback_context
import plotly.express as px
import pandas as pd
from services.database import Session
from dash_app.utils import age_category, format_time


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
# app = Dash(__name__)

presentation = """
This dashboard provides a representation of the runners of the Zürich marathon from
2014 to 2018. 

The data is obtained from the [datasport.com](https://datasport.com/de/) website.
The data is provided for *demonstrative* purposes only.

## Usage
The raw data can be filtered for *marathon year* and *age bracket*.
At the bottom of the page a table is presented with the filtered data; it can be furthermore filtered and 
sorted.

A download button is provided at the bottom of the page to obtain a *csv* file with the data 
selected by the dropdowns.
"""

def query_runners():
    with Session() as session:
        # query = 'SELECT "Id", "Age_year", "total_time", "run_year" FROM runners'
        query = 'SELECT * FROM runners'
        return pd.read_sql_query(query, session.bind, index_col=None)


df_sql = query_runners()
df = df_sql.dropna()
df = df.astype({'Age_year': 'Int64'})
df['age'] = df.run_year - df.Age_year
df['age_decade'] = df['age'].apply(age_category)
df['total_time'] = df_sql.total_time.apply(format_time)


year_indicator = sorted(df.run_year.unique())
age_decade_indicator = sorted(df.age_decade.unique())

# sort is an unfortunate hack to show the legend of the graph in the right order
df_graph = df.groupby(["run_year", "age_decade"], as_index=False).count().sort_values(by="age_decade")


@app.callback(
    Output('runners_fig', 'figure'),
    Input('year_run_selector', 'value'),
    Input('runner_age_bracket_selector', 'value')
)
def update_graph(year_run_name, runner_age_name):
    dff = df_graph.copy()
    if runner_age_name is not None:
        dff = dff[dff['age_decade'] == runner_age_name]
    if year_run_name is not None:
        dff = dff[dff['run_year'] == year_run_name]

    fig = px.bar(
        dff,
        x="run_year",
        y="Age_year",
        color="age_decade",
        hover_data=['Age_year'],
        barmode='stack',
        labels={
            'run_year': 'Run Year',
            'age_decade': 'Age Group',
            'Age_year': 'Count of athletes'
        },
        title='Zürich marathon runners'
    )
    fig.update_xaxes(tick0=1900, dtick=1)
    return fig


@app.callback(
    Output('runners_table', 'children'),
    Input('year_run_selector', 'value'),
    Input('runner_age_bracket_selector', 'value')
)
def update_table(year_run_name, runner_age_name):
    dff = df.copy()
    if runner_age_name is not None:
        dff = dff[dff['age_decade'] == runner_age_name]
    if year_run_name is not None:
        dff = dff[dff['run_year'] == year_run_name]
    return dash_table.DataTable(
        dff.to_dict('records'),
        page_action='native',
        page_current=0,
        page_size=10,
        filter_action='native',
        sort_action="native",
        sort_mode="multi",
        columns=[{'name': x, 'id': x} for x in dff.columns]
    )


@app.callback(
    Output("download", "data"),
    Input("btn_csv", "n_clicks"),
    State('year_run_selector', 'value'),
    State('runner_age_bracket_selector', 'value'),
    prevent_initial_call=True
)
def data_download(n_clicks, year_run_name, runner_age_name):
    # state provides a way to not trigger the download on anything else than a click
    #    return
    dff = df.copy()
    age = 'all'
    year = 'all'
    if runner_age_name is not None:
        dff = dff[dff['age_decade'] == runner_age_name]
        age = runner_age_name
    if year_run_name is not None:
        dff = dff[dff['run_year'] == year_run_name]
        year = year_run_name
    return dcc.send_data_frame(dff.to_csv, filename=f"runners_year-{year}_age-{age}.csv")


app.layout = html.Div(children=[
    html.H1('Marathon dashboard'),
    html.Div([dcc.Markdown(presentation)]),
    html.Div([
        dcc.Dropdown(
            year_indicator,
            placeholder='Select a marathon year',
            id='year_run_selector'
        )], style={'width': '48%', 'display': 'inline-block'}
    ),
    html.Div([
        dcc.Dropdown(
            age_decade_indicator,
            placeholder='Select the age bracket',
            id='runner_age_bracket_selector'
        )], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}
    ),
    dcc.Graph(
        id='runners_fig',
    ),
    html.Div(id='runners_table'),
    html.Button("Download CSV", id="btn_csv"),
    dcc.Download(id="download")
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
