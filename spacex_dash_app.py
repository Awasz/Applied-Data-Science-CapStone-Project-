# Import required libraries
import pandas as pd
import dash
from dash import dcc,html, Input,Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=[
                                {'label': 'All Sites', 'value': 'All'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                {'label' : 'KSC LC-39A', 'value' : 'KSC LC-39A'},
                                {'label' : 'CCAFS SLC-40' ,'value' : 'CCAFS SLC-40'}
                                    ],
                                 value='All',
                                 placeholder ='Select a Launch Site here',
                                 searchable=True
                                       ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000,step=1000,
                                marks={0: '0',100: '100'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value'))

def update_pie_chart(selected_site):
    if selected_site == 'All':
        # If 'ALL' sites are selected, use the entire DataFrame
        pie_chart_data = spacex_df
    else:
        # If a specific site is selected, filter the DataFrame
        pie_chart_data = spacex_df[spacex_df['Launch Site'] == selected_site]

    # Calculate the success and failed counts
    success_count = pie_chart_data[pie_chart_data['class'] == 1]['class'].count()
    failed_count = pie_chart_data[pie_chart_data['class'] == 0]['class'].count()

    # Create a pie chart
    fig = px.pie(
        names=['Success', 'Failed'],
        values=[success_count, failed_count],
        title=f'Success vs. Failed Launches at {selected_site}' if selected_site != 'ALL' else 'Total Success vs. Failed Launches'
    )

    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
              Input(component_id='site-dropdown',component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def update_scatter_chart(selected_site, payload_range) :
    if selected_site=='All':
        filtered_df=spacex_df
        
    else : 
        filtered_df=spacex_df[spacex_df['Launch Site']==selected_site]             
#Filter the date to fall in a certain range
    filtered_df = filtered_df[
        (filtered_df['Payload Mass (kg)'] >= payload_range[0]) &
        (filtered_df['Payload Mass (kg)'] <= payload_range[1])
    ]        
#Render a scatter plot to show relationship between 'Payload Mass (kg)' and 'class'
    fig=px.scatter(filtered_df,x='Payload Mass (kg)', y='class', color='Booster Version Category',
    title=f'Correlation between Payload Mass (kg) and Success  at {selected_site}')
    return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
