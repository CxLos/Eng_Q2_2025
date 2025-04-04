# =================================== IMPORTS ================================= #
import csv, sqlite3
import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.figure_factory as ff
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from folium.plugins import MousePosition
import plotly.express as px
import datetime
import folium
import os
import sys
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.development.base_component import Component
# 'data/~$bmhc_data_2024_cleaned.xlsx'
# print('System Version:', sys.version)
# -------------------------------------- DATA ------------------------------------------- #

current_dir = os.getcwd()
current_file = os.path.basename(__file__)
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = 'data/Engagement_Responses.xlsx'
file_path = os.path.join(script_dir, data_path)
data = pd.read_excel(file_path)
df = data.copy()

# Trim leading and trailing whitespaces from column names
df.columns = df.columns.str.strip()

# Define a discrete color sequence
# color_sequence = px.colors.qualitative.Plotly

# Filtered df where 'Date of Activity:' is between Ocotber to December:
df['Date of Activity'] = pd.to_datetime(df['Date of Activity'], errors='coerce')
df = df[(df['Date of Activity'].dt.month >= 10) & (df['Date of Activity'].dt.month <= 12)]

# print(df.head(10))
# print('Total Marketing Events: ', len(df))
# print('Column Names: \n', df.columns)
# print('DF Shape:', df.shape)
# print('Dtypes: \n', df.dtypes)
# print('Info:', df.info())
# print("Amount of duplicate rows:", df.duplicated().sum())

# print('Current Directory:', current_dir)
# print('Script Directory:', script_dir)
# print('Path to data:',file_path)

# ================================= Columns ================================= #

# Column Names: 

        # 'Timestamp', 
        # 'Date of Activity', 
        # 'Person submitting this form:',
        # 'Activity Duration (minutes):',
        # 'Care Network Activity:',
        # 'Entity name:', 
        # 'Brief Description:', 
        # 'Activity Status:',
        # 'BMHC Administrative Activity:', 
        # 'Total travel time (minutes):',
        # 'Community Outreach Activity:',
        # 'Number engaged at Community Outreach Activity:'

# =============================== Missing Values ============================ #

# missing = df.isnull().sum()
# print('Columns with missing values before fillna: \n', missing[missing > 0])

# ============================== Data Preprocessing ========================== #

# Check for duplicate columns
# duplicate_columns = df.columns[df.columns.duplicated()].tolist()
# print(f"Duplicate columns found: {duplicate_columns}")
# if duplicate_columns:
#     print(f"Duplicate columns found: {duplicate_columns}")



# ========================= Filtered DataFrames ========================== #

# Total number of engagements:
total_engagements = len(df)
print('Total Engagements:', total_engagements)

# Sum of 'Activity Duration (minutes):' dataframe converted to hours:
engagement_hours = df['Activity Duration (minutes):'].sum()/60
engagement_hours = round(engagement_hours)
print('Sum Engagement Hours:', engagement_hours)

# round to the nearest whole number:


#  Duplicate values in 'Person submitting this form:' column:

# 0           Antonio Montggery       1
# 1           Antonio Montgomery      1
# 2              Cameron Morgan       1
# 3             Kiounis Williams      6
# 4            Kiounis Williams       3
# 5             Larry Wallace Jr     31

# remove trailing whitespaces in 'Person submitting this form:' column
df['Person submitting this form:'] = df['Person submitting this form:'].str.strip()

df['Person submitting this form:'] = df['Person submitting this form:'].replace("Larry Wallace Jr", "Larry Wallace Jr.")

df['Person submitting this form:'] = df['Person submitting this form:'].replace("`Larry Wallace Jr", "Larry Wallace Jr.")

df['Person submitting this form:'] = df['Person submitting this form:'].replace("Antonio Montggery", "Antonio Montgomery")

# df['Person submitting this form:'] = df['Person submitting this form:'].replace("Kiounis Williams ", "Kiounis Williams")


# Group by 'Person submitting this form:' dataframe
person_group = df.groupby('Person submitting this form:').size().reset_index(name='Count')
# print(person_group.value_counts())

# Group by 'Entity type:' dataframe
# entity_group = df.groupby('Entity type:').size().reset_index(name='Count')

# Group by 'Entity name:' dataframe
# entity_name_group = df.groupby('Entity name:').size().reset_index(name='Count')

# Group by 'Activity Status:' dataframe
activity_status_group = df.groupby('Activity Status:').size().reset_index(name='Count')

# sum 'Total travel time (minutes):' dataframe:
total_travel_time = df['Total travel time (minutes):'].sum()
total_travel_time = round(total_travel_time)

# Group by 'BMHC Administrative Activity:' dataframe:
admin_activity = df.groupby('BMHC Administrative Activity:').size().reset_index(name='Count')

# Group by 'Care Network Activity:' dataframe:
care_network_activity = df.groupby('Care Network Activity:').size().reset_index(name='Count')

# Group by 'Community Outreach Activity:' dataframe:
community_outreach_activity = df.groupby('Community Outreach Activity:').size().reset_index(name='Count')

# # ========================== DataFrame Table ========================== #

# MarCom Table
engagement_table = go.Figure(data=[go.Table(
    # columnwidth=[50, 50, 50],  # Adjust the width of the columns
    header=dict(
        values=list(df.columns),
        fill_color='paleturquoise',
        align='center',
        height=30,  # Adjust the height of the header cells
        # line=dict(color='black', width=1),  # Add border to header cells
        font=dict(size=12)  # Adjust font size
    ),
    cells=dict(
        values=[df[col] for col in df.columns],
        fill_color='lavender',
        align='left',
        height=25,  # Adjust the height of the cells
        # line=dict(color='black', width=1),  # Add border to cells
        font=dict(size=12)  # Adjust font size
    )
)])

engagement_table.update_layout(
    margin=dict(l=50, r=50, t=30, b=40),  # Remove margins
    height=400,
    # width=1500,  # Set a smaller width to make columns thinner
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot area
)

# Entity Name Table
# entity_name_table = go.Figure(data=[go.Table(
#     header=dict(
#         values=list(entity_name_group.columns),
#         fill_color='paleturquoise',
#         align='center',
#         height=30,
#         font=dict(size=12)
#     ),
#     cells=dict(
#         values=[entity_name_group[col] for col in entity_name_group.columns],
#         fill_color='lavender',
#         align='left',
#         height=25,
#         font=dict(size=12)
#     )
# )])

# entity_name_table.update_layout(
#     margin=dict(l=50, r=50, t=30, b=40),
#     height=400,
#     paper_bgcolor='rgba(0,0,0,0)',
#     plot_bgcolor='rgba(0,0,0,0)'
# )

# ============================== Dash Application ========================== #

app = dash.Dash(__name__)
server= app.server 

app.layout = html.Div(
  children=[ 
    html.Div(
        className='divv', 
        children=[ 
          html.H1(
              'Partner Engagement Report Q1 2025', 
              className='title'),
          html.Div(
              className='btn-box', 
              children=[
                  html.A(
                    'Repo',
                    href='https://github.com/CxLos/Eng_Q1_2025',
                    className='btn'),
    ]),
  ]),    

# Data Table
# html.Div(
#     className='row0',
#     children=[
#         html.Div(
#             className='table',
#             children=[
#                 html.H1(
#                     className='table-title',
#                     children='Partner Engagement Table'
#                 )
#             ]
#         ),
#         html.Div(
#             className='table2', 
#             children=[
#                 dcc.Graph(
#                     className='data',
#                     figure=engagement_table
#                 )
#             ]
#         )
#     ]
# ),

# ROW 1
# ROW 1
html.Div(
    className='row1',
    children=[
        html.Div(
            className='graph11',
            children=[
            html.Div(
                className='high1',
                children=['Total Engagements:']
            ),
            html.Div(
                className='circle1',
                children=[
                    html.Div(
                        className='hilite',
                        children=[
                            html.H1(
                            className='high3',
                            children=[total_engagements]
                    ),
                        ]
                    )
 
                ],
            ),
            ]
        ),
        html.Div(
            className='graph22',
            children=[
            html.Div(
                className='high2',
                children=['Engagemnt Hours:']
            ),
            html.Div(
                className='circle2',
                children=[
                    html.Div(
                        className='hilite',
                        children=[
                            html.H1(
                            className='high4',
                            children=[engagement_hours]
                    ),
                        ]
                    )
 
                ],
            ),
            ]
        ),
    ]
),

# ROW 1
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph1',
            children=[
              # Activity Status group bar chart
                dcc.Graph(
                    id='activity_status_group',
                    figure=px.pie(
                        activity_status_group,
                        names='Activity Status:',
                        values='Count',
                    ).update_layout(
                        title='Activity Status:',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        textposition='auto',
                        textinfo='label+percent',
                        hovertemplate='<b>Status</b>: %{label}<br><b>Count</b>: %{value}<extra></extra>'
                    )
                )
            ]
        ),
        html.Div(
            className='graph2',
            children=[
                # Person group bar chart
                dcc.Graph(
                    id='person_group',
                    figure=px.bar(
                        person_group,
                        x='Person submitting this form:',
                        y='Count',
                        color='Person submitting this form:',
                        text='Count'
                    ).update_layout(
                        title='Person submitting this form:',
                        xaxis_title='Person',
                        yaxis_title='Count',
                       title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        textposition='auto',
                        hovertemplate='<b>Activity</b>: %{x}<br><b>Count</b>: %{y}<extra></extra>'
                    )
                )
            ]
        )
    ]
),

# ROW 2
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph11',
            children=[
            html.Div(
                className='high1',
                children=['Total Travel Time:']
            ),
            html.Div(
                className='circle1',
                children=[
                    html.Div(
                        className='hilite',
                        children=[
                            html.H1(
                            className='high5',
                            children=[total_travel_time]
                    ),
                        ]
                    )
 
                ],
            ),
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                html.Div(
                    className='table2', 
                    children=[
                    #   'BMHC Administrative Activity:' bar chart:
                        dcc.Graph(
                            id='admin_activity',
                            figure=px.bar(
                                admin_activity,
                                x='BMHC Administrative Activity:',
                                y='Count',
                                color='BMHC Administrative Activity:',
                                text='Count'
                            ).update_layout(
                                title='BMHC Administrative Activity:',
                                xaxis_title='Activity',
                                yaxis_title='Count',
                                title_x=0.5,
                                font=dict(
                                    family='Calibri',
                                    size=17,
                                    color='black'
                                )
                            ).update_traces(
                                textposition='auto',
                                hovertemplate='<b>Activity</b>: %{x}<br><b>Count</b>: %{y}<extra></extra>'
                            )
                        )
                    ]
                )
            ]
        ),
    ]),

    # ROW 1
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph1',
            children=[
              # 'Care Network Activity:' bar chart
                dcc.Graph(
                    id='care_network_activity',
                    figure=px.bar(
                        care_network_activity,
                        x='Care Network Activity:',
                        y='Count',
                        color='Care Network Activity:',
                        text='Count'
                    ).update_layout(
                        title='Care Network Activity:',
                        xaxis_title='Activity',
                        yaxis_title='Count',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        textposition='auto',
                        hovertemplate='<b>Activity</b>: %{x}<br><b>Count</b>: %{y}<extra></extra>'
                    )
                )
            ]
        ),
        html.Div(
            className='graph2',
            children=[
                # 'Community Outreach Activity:' bar chart
                dcc.Graph(
                    id='community_outreach_activity',
                    figure=px.bar(
                        community_outreach_activity,
                        x='Community Outreach Activity:',
                        y='Count',
                        color='Community Outreach Activity:',
                        text='Count'
                    ).update_layout(
                        title='Community Outreach Activity:',
                        xaxis_title='Activity',
                        yaxis_title='Count',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        textposition='auto',
                        hovertemplate='<b>Activity</b>: %{x}<br><b>Count</b>: %{y}<extra></extra>'
                    )
                )
            ]
        )
    ]
),
])

print(f"Serving Flask app '{current_file}'! 🚀")

if __name__ == '__main__':
    app.run_server(debug=True)
                #    False)
# =================================== Updated Database ================================= #

# updated_path = 'data/bmhc_q4_2024_cleaned.xlsx'
# data_path = os.path.join(script_dir, updated_path)
# df.to_excel(data_path, index=False)
# print(f"DataFrame saved to {data_path}")

# updated_path1 = 'data/service_tracker_q4_2024_cleaned.csv'
# data_path1 = os.path.join(script_dir, updated_path1)
# df.to_csv(data_path1, index=False)
# print(f"DataFrame saved to {data_path1}")

# -------------------------------------------- KILL PORT ---------------------------------------------------

# netstat -ano | findstr :8050
# taskkill /PID 24772 /F
# npx kill-port 8050

# ---------------------------------------------- Host Application -------------------------------------------

# 1. pip freeze > requirements.txt
# 2. add this to procfile: 'web: gunicorn impact_11_2024:server'
# 3. heroku login
# 4. heroku create
# 5. git push heroku main

# Create venv 
# virtualenv venv 
# source venv/bin/activate # uses the virtualenv

# Update PIP Setup Tools:
# pip install --upgrade pip setuptools

# Install all dependencies in the requirements file:
# pip install -r requirements.txt

# Check dependency tree:
# pipdeptree
# pip show package-name

# Remove
# pypiwin32
# pywin32
# jupytercore

# ----------------------------------------------------

# Name must start with a letter, end with a letter or digit and can only contain lowercase letters, digits, and dashes.

# Heroku Setup:
# heroku login
# heroku create mc-impact-11-2024
# heroku git:remote -a mc-impact-11-2024
# git push heroku main

# Clear Heroku Cache:
# heroku plugins:install heroku-repo
# heroku repo:purge_cache -a mc-impact-11-2024

# Set buildpack for heroku
# heroku buildpacks:set heroku/python

# Heatmap Colorscale colors -----------------------------------------------------------------------------

#   ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
            #  'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
            #  'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
            #  'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
            #  'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
            #  'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
            #  'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
            #  'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
            #  'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
            #  'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
            #  'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
            #  'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
            #  'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
            #  'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
            #  'ylorrd'].

# rm -rf ~$bmhc_data_2024_cleaned.xlsx
# rm -rf ~$bmhc_data_2024.xlsx
# rm -rf ~$bmhc_q4_2024_cleaned2.xlsx