from dash import Dash, html, dcc, callback, Input, Output
import plotly
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import plotly.io as pio

pio.templates.default = "none"

df_monthly = pd.read_csv("./monthly_rainfall/india_monthly_rainfall_data.csv")
df_india = pd.read_csv("./rainfall_in_india/rainfall in india 1901-2015.csv")
df_monthly.set_index("Year")

df = pd.read_csv("./rainfall_in_india/rainfall in india 1901-2015.csv")

def process_df_parcoords(df, subdivision):
    new_df = df[df['SUBDIVISION']==subdivision]
    new_df = new_df[['SUBDIVISION', 'YEAR', 'ANNUAL','Jan-Feb','Mar-May','Jun-Sep','Oct-Dec']]
    return new_df

# processed_df = process_df_parcoords(df_india, 'TAMIL NADU')
# figpar = px.parallel_coordinates(processed_df, dimensions=['YEAR','ANNUAL','Jan-Feb','Mar-May','Jun-Sep','Oct-Dec'], color='ANNUAL', color_continuous_scale='Turbo')
# figpar.update(layout_coloraxis_showscale=False)
def process_df_box_whisker(df,subdivision):
    new_df = df[df['SUBDIVISION'] == subdivision]
    new_df = new_df[['SUBDIVISION', 'YEAR'] + months]
    new_df = new_df.melt(id_vars=['SUBDIVISION', 'YEAR'], value_vars= months, var_name='Month', value_name='Rainfall')
    return new_df


ret = df_monthly[df_monthly["State"] == "Andhra Pradesh"]
months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
# marks for the year slider
marks = {i: "{}".format(i) for i in range(1901, 2002, 3)}


# function for giving average rainfall for given range
def avg_rain(df, state, district, min, max):
    dff = df[df["State"] == state]
    dff = dff[dff["District"] == district]
    dff = dff[dff["Year"] <= max]
    dff = dff[dff["Year"] >= min]
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    # print(dff)
    a = []
    for month in months:
        a.append(int(dff[month].mean()))
    return a


# print(ret.District.unique()[0])
app = Dash(__name__)
app.layout = html.Div(
    [
        
        html.Main(

            children=[
                        dcc.Markdown(
                            '''
                                ## CS661 - Course Project
                                ### Group 28 (190928 and 190593)
                            '''
                        ),
                        html.Br(),
                        html.H2(children="Year-Round rainfall levels"),
                        html.P(children="You can see the graphs for a state of your choice and a district within that state for the selected year range. Apart from comparing the rainfall patterns in different states, variations within a state can be explored.", style={"padding-inline-start": "16px"}),
                html.Section(
                    children=[
                        dcc.Dropdown(
                            df_monthly.State.unique(),
                            np.random.choice(df_monthly.State.unique()),
                            id="state-selection",
                        ),
                        dcc.Dropdown(
                            id="district-selection",
                        ),
                        dcc.RangeSlider(
                            1901,
                            2002,
                            1,
                            marks=None,
                            value=[1992, 2002],
                            tooltip={"placement": "bottom", "always_visible": True},
                            id="year-range",
                        ),
                    ],
                    className="filter-container",
                ),
                html.Div(id="array"),
                html.Div(
                    children=[
                        dcc.Graph(id="monthly-rainfall-state"),
                        dcc.Graph(id="monthly-rainfall-district"),
                    ],
                    className="graph-container",
                ),
                        html.Hr(),
                      html.H2(children="Monthly Rainfall Over the Years"),
                        html.P(children=''' Most regions in India see rainfall in in June to Septmeber, 
                        however there is much diversity like retreating monsoon from October to December
                         in Southern India. You can select a month and see the rainfall levels for the state 
                         and district selected above through the year range. ''', style={"padding-inline-start": "16px"}),
                dcc.Dropdown(months, "Jan", id="select-month"),
                html.Div(
                    children=[
                        dcc.Graph(id="Monthly-trends-state"),
                        dcc.Graph(id="Monthly-trends-district"),
                    ],
                    className="graph-container",
                ),
                        html.Hr(),
                      html.H2(children="Parallel Coordinates plot for Subdivisions"),
                        html.P(children= ''' Extreme weather events can be visualized by selecting different ranges 
                        of different values on vertical axes rainfall range, like annual rainfall on the second vertical axes. 
                        You can also visualize changing patterns in rainfall by selecting years range.''', style={"padding-inline-start": "16px"}),
                html.Div(
                    #dcc.Dropdown(months, "Jan", id="select-division"),
                    children=[
                        dcc.Dropdown(id='parcords-dd',options=df_india.SUBDIVISION.unique(),value=np.random.choice(df_india.SUBDIVISION.unique())),
                        dcc.Graph(id='parcords'),
                    ],
                ),
                    html.Hr(),
                    html.H2(children="SubDivision-wise Box-Whisker Plots"),
                    html.P(children="This graph visualizes the overall distribution rainfall in month for subdivisions over the years.", style={"padding-inline-start": "16px"}),
                html.Div(
                    #dcc.Dropdown(months, "Jan", id="select-division"),
                    children=[
                        dcc.Dropdown(id='box-whisker-dd',options=df_india.SUBDIVISION.unique(),value=np.random.choice(df_india.SUBDIVISION.unique())),
                        dcc.Graph(id='box-whisker'),
                    ],
                ),
                    html.Hr(),
                    html.H2(children="SubDivision-wise Choropleth and Heatmap Plots"),
                    html.P(children="The Choropleth map represents the annual rainfall of different subdivisions of India on a colorscale, the heatmap on the other hand displays the year round levels of rainfall. Use the slider to select an year.  ", style={"padding-inline-start": "16px"}),
                html.Div(
                    children = [
                        dcc.Slider(1901,2015,value=1901,marks=None,tooltip={"placement": "bottom", "always_visible": True},included=False,id='year-choropleth'),
                        
                    ],

                ),
                html.H3(children = "",id="choropleth-heading",style={'text-align':'center'}),

                
                html.Div(
                    children = [
                        dcc.Graph(id='Choropleth'),
                        dcc.Graph(id='heatmap-1'),
                    ],
                    className="graph-container",
                ),
            ],
            className="main",
        ),
    ]
)



@app.callback(
    Output("district-selection", "options"), Input("state-selection", "value")
)
def update_dd_options(state_name):
    # print(state_name)
    ret = df_monthly[df_monthly["State"] == state_name]
    return ret.District.unique()


@app.callback(Output("district-selection", "value"), Input("state-selection", "value"))
def update_dd_value(state_name):
    # print(state_name)
    ret = df_monthly[df_monthly["State"] == state_name]
    print(ret.District.unique()[0])
    return ret.District.unique()[0]


0


def update_smin(value):
    return "Min = {}".format(value[0])


# @app.callback(
#     Output('sliderMax','children'),
#     Input('year-range','value')
# )
# def update_smin(value):
#     return 'Max = {}'.format(value[1])

# @app.callback(
#     Output('monthly-rainfall-district','figure'),
#     [Input('district-selection','value'),
#     Input('state-selection','value'),
#     Input('year-range','value'),
#     ]
# )
# def update_graph(district,state,value):
#     a = avg_rain(df_monthly,state,district,value[0],value[1])
#     cols = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
#     print(a)
#     b = a
#     for x in b:
#         x = x+20
#     fig = px.scatter(y=a,x=cols,size=b)
#     fig.update_layout()
# return fig


@app.callback(
    Output("monthly-rainfall-district", "figure"),
    [
        Input("district-selection", "value"),
        Input("state-selection", "value"),
        Input("year-range", "value"),
    ],
)
def update_graph(district, state, value):
    a = avg_rain(df_monthly, state, district, value[0], value[1])
    cols = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    print(a)
    b = a
    for x in b:
        x = x + 20
    fig = px.scatter(
        y=a,
        x=cols,
        size=b,
        color=b,
        color_continuous_scale='Viridis_r',
        labels={"x": "Months", "y": "Rainfall in mm","color":"Rainfall in mm"},
        title="Monthly average for {}-{} in {}".format(value[0], value[1], district),
    )
    fig.update_layout()
    return fig


@app.callback(
    Output("monthly-rainfall-state", "figure"),
    [
        Input("state-selection", "value"),
        Input("year-range", "value"),
    ],
)
def update_graph(state, value):
    dff = df_monthly[df_monthly["State"] == state]
    dff = dff[dff["Year"] <= value[1]]
    dff = dff[dff["Year"] >= value[0]]
    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    a = []
    for month in months:
        a.append(dff[month].mean())
    b = a
    for x in b:
        if x > 70:
            x = 70
        if x < 5:
            x = 5
    fig = px.scatter(
        y=b,
        x=months,
        size=b,
        labels={"x": "Months", "y": "Rainfall in mm","color":"Rainfall in mm"},
        color=b,
        title="Monthly average for {}-{} in {}".format(value[0], value[1], state),
        color_continuous_scale = 'viridis_r',
    )
    fig.update_layout()
    return fig


@app.callback(
    Output("Monthly-trends-state", "figure"),
    [
        Input("state-selection", "value"),
        Input("year-range", "value"),
        Input("district-selection", "value"),
        Input("select-month", "value"),
    ],
)
def update_graph2_1(state, range, district, month):
    # State
    dff_1 = dff = df_monthly[df_monthly["State"] == state]
    dff = dff[dff["District"] == district]

    dff = dff[dff["Year"] <= range[1]]
    dff = dff[dff["Year"] >= range[0]]
    dff = dff[["Year", month]]
    dff = dff.astype({"Year": int})

    dff_1 = dff_1[dff_1["Year"] <= range[1]]
    dff_1 = dff_1[dff_1["Year"] >= range[0]]
    dff_1 = dff_1[["Year", month]]
    dff_1 = dff_1.astype({"Year": int})
    dff_1 = dff_1.groupby(["Year"]).mean()
    y = "Rainfall in State (mm)"
    dff_1.rename(
        columns={"Year": "Year", month: "Rainfall in State (mm)"}, inplace=True
    )
    # dff_1 = dff_1[['Year',month]]
    # dff_1 = dff_1.astype({'Year':int})

    # dff = dff.set_index('Year')
    # print(dff_1)
    print(dff_1)
    print(dff)
    # dict = {'District': px.scatter(dff,x='Year',y=month,size=dff[month].clip(10,70),template="seaborn"),
    # 'State': px.scatter(dff_1,x='Year',y=month,size=dff_1[month].clip[10,70],template="seaborn")}
    # fig = px.scatter(dff,x='Year',y=month,size=dff[month].clip(10,70))
    return px.scatter(
        dff_1,
        y=y,
        size=dff_1[y].clip(1, 70),
        color="Rainfall in State (mm)",
        color_continuous_scale='Viridis_r',
        title="Rainfall in {} between {}-{} in {}".format(
            month, range[0], range[1], state
        ),
    )


@app.callback(
    Output("Monthly-trends-district", "figure"),
    [
        Input("state-selection", "value"),
        Input("year-range", "value"),
        Input("district-selection", "value"),
        Input("select-month", "value"),
    ],
)
def update_graph2_2(state, range, district, month):
    # District
    dff_1 = dff = df_monthly[df_monthly["State"] == state]
    dff = dff[dff["District"] == district]

    dff = dff[dff["Year"] <= range[1]]
    dff = dff[dff["Year"] >= range[0]]
    dff = dff[["Year", month]]
    dff = dff.astype({"Year": int})
    dff.rename(columns={"Year": "Year", month: "Rainfall in (mm)"}, inplace=True)

    dff_1 = dff_1[dff_1["Year"] <= range[1]]
    dff_1 = dff_1[dff_1["Year"] >= range[0]]
    dff_1 = dff_1[["Year", month]]
    dff_1 = dff_1.astype({"Year": int})
    dff_1 = dff_1.groupby(["Year"]).mean()
    # dff_1 = dff_1[['Year',month]]
    # dff_1 = dff_1.astype({'Year':int})

    # dff = dff.set_index('Year')
    # print(dff_1)
    print(dff_1)
    print(dff)

    # dict = {'District': px.scatter(dff,x='Year',y=month,size=dff[month].clip(10,70),template="seaborn"),
    # 'State': px.scatter(dff_1,x='Year',y=month,size=dff_1[month].clip[10,70],template="seaborn")}
    # fig = px.scatter(dff,x='Year',y=month,labels={},size=dff[month].clip(10,70))
    return px.scatter(
        dff,
        x="Year",
        y="Rainfall in (mm)",
        color="Rainfall in (mm)",
        labels={"x": "Year", "y": "Rainfall in District(mm)"},
        size=dff["Rainfall in (mm)"].clip(1, 70),
        title="Rainfall in {} between {}-{} in {}".format(
            month, range[0], range[1], district
        ),
        color_continuous_scale='Viridis_r'
    )

@app.callback(
    Output('parcords','figure'),
    Input('parcords-dd','value')
)
def update_parcord(subdivision):
    processed_df = process_df_parcoords(df_india, subdivision)
    figpar = px.parallel_coordinates(processed_df, 
    dimensions=['YEAR','ANNUAL','Jan-Feb','Mar-May','Jun-Sep','Oct-Dec'], 
    color='ANNUAL', color_continuous_scale='deep',title="SubDivision-Wise Rainfall <br>")
    figpar.update(layout_coloraxis_showscale=False)
    return figpar

@app.callback(
    Output('box-whisker','figure'),
    Input('box-whisker-dd','value')
)
def update_box_whisker(subdivision):
    df = df_india
    months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    new_df = df[df['SUBDIVISION'] == subdivision]
    new_df = new_df[['SUBDIVISION', 'YEAR'] + months]
    new_df = new_df.melt(id_vars=['SUBDIVISION', 'YEAR'], value_vars= months, var_name='Month', value_name='Rainfall')
  
    fig = px.box(new_df, x='Month', y='Rainfall', hover_data = 'YEAR', points='all',title="Monthly Rainfall distribution of India in 1901-015")
    fig.update_layout()
    return fig

@app.callback(
    Output('Choropleth','figure'),
    Input('year-choropleth','value')
)



def update_choropleth(year):
    df = df_india[df_india['YEAR']==year]
    fig = px.choropleth(
    df,
    geojson="https://gist.githubusercontent.com/utkjainiitk/8a3eada0d52355feca6ee4470339bf28/raw/9fddf77324adf0066163cef31ba4e03209f6aca3/sd.geojson",
    featureidkey='properties.subdivisio',
    locations='SUBDIVISION',
    color='ANNUAL',
    color_continuous_scale='deep',
    # projection='satellite'
        width=800,height=800
    )
    # fig.update(layout_coloraxis_showscale=False)
    fig.update_geos(fitbounds="geojson", visible=False,
                    projection_scale=1.5,  resolution = 50, lataxis_range=[-5,20], lonaxis_range=[0, 20])
    fig.update_layout(autosize=False, margin=dict(l=0, r=0, t=0, b=0,autoexpand=True,pad=0), title = 'Annual rainfall in India(in mm)')
    return fig

@app.callback(
    Output('heatmap-1','figure'),
    Input('year-choropleth','value')
)

def update_heatmap(year):
    months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    df = df_india[df_india['YEAR']==year]
    subdivs = df['SUBDIVISION']
    data = np.array(df[months])
    fig = px.imshow(data,
        y=subdivs,
        x = months,
        labels=dict(x="Months", y="Subdivisions",color="Rainfall"),
        color_continuous_scale  ='deep',)

    
    return fig

@app.callback(
    Output('choropleth-heading','children'),
    Input('year-choropleth','value')
)

def update_heading(year):
    return "Rainfall in subdivisions of India in {}".format(year)


if __name__ == "__main__":
    app.run_server(debug=True)
