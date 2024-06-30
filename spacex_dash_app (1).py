# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Create a dash application
app = dash.Dash(__name__)

# Create a list of launch sites
launch_sites = spacex_df['Launch Site'].unique().tolist()

# Create options list for the dropdown menu
options = [{'label': 'All Sites', 'value': 'ALL'}]
options += [{'label': site, 'value': site} for site in launch_sites]

# Create the layout of the application
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    # TASK 1: Add a Launch Site Drop-down Input Component
    dcc.Dropdown(id='site-dropdown',
                 options=options,
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True
                 ),
    html.Br(),
    
    # TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # TASK 3: Add a Range Slider to Select Payload
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000', 5000: '5000',
                           6000: '6000', 7000: '7000', 8000: '8000', 9000: '9000', 10000: '10000'},
                    value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]),

    html.Br(),
    # TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
                     names='Launch Site',
                     title='Total Success Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class',
                     title=f'Total Success Launches for site {entered_site}')
        return fig

# TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color="Booster Version Category",
                         title='Payload vs. Outcome for all Sites')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color="Booster Version Category",
                         title=f'Payload vs. Outcome for site {entered_site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
