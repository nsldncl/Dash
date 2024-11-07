import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Create app

app = dash.Dash(__name__)

# Clear the layout and do not display exception until callback gets executed

app.config.suppress_callback_exceptions = True

df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

df["Month"] = pd.to_datetime(df["Date"]).dt.month_name()
df["Year"] = pd.to_datetime(df["Date"]).dt.year

# Add title to outer division

app.layout = html.Div(children=[html.H1("Australia Wildfires Dashboard",
style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 26}),

#Add first inner division

    html.Div([
        
        # Add first inner division of first inner division

        html.Div([

        # Add radio items

        html.H2("Select region"),
        dcc.RadioItems([
        {"label": "New South Wales", "value": "NSW"},
        {"label": "Victoria", "value": "VI"},
        {"label": "Queensland", "value": "QL"},
        {"label": "South Australia", "value": "SA"},
        {"label": "Western Australia", "value": "WA"},
        {"label": "Tasmania", "value": "TA"},
        {"label": "Northern Territory", "value": "NT"}
    ], value="NSW", id="region", inline=True)]),
    
    #Add second inner division of first inner division

    html.Div([

        # Add dropdown 

        html.H2("Select year", style={"margin-right": "2em"}),
        dcc.Dropdown(df.Year.unique(), value=2005, id='year')
    ]),

# Add second inner division

html.Div([

    # Add first inner division of second inner division

    html.Div([], id="plot1"),

    # Add second inner division of second inner division

    html.Div([], id="plot2")
], style={}),


    ])

]) # outer division / app layout ends

# Add Output and Input to callback decorator

@app.callback([Output(component_id="plot1", component_property="children"),
               Output(component_id="plot2", component_property="children")],
               [Input(component_id="region", component_property="value"),
                Input(component_id="year", component_property="value")])

# Add callback function

def reg_year_display(input_region, input_year):
    region_data = df[df["Region"] == input_region]
    year_region_data = region_data[region_data["Year"]==input_year]

    # Plot one: monthly average estimated fire area

    fire_area = year_region_data.groupby("Month")["Estimated_fire_area"].mean().reset_index()

    fig1 = px.pie(fire_area, values= "Estimated_fire_area", names="Month", title="{} : Monthly Average Estimated Fire Area in year {}".format(input_region,input_year))

    # Plot two: monthly average count of pixels

    pixel_count = year_region_data.groupby("Month")["Count"].mean().reset_index()

    fig2 = px.bar(pixel_count, x="Month", y="Count", title='{} : Average Count of Pixels for Presumed Vegetation Fires in year {}'.format(input_region,input_year))

    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]

if __name__ == "__main__":
    app.run_server()
