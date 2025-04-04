# =================================== IMPORTS ================================= #
#  
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
import os
import dash
from dash import dcc, html
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
df = df[(df['Date of Activity'].dt.month >= 1) & (df['Date of Activity'].dt.month <= 3)]
df['Month'] = df['Date of Activity'].dt.month_name()

df_oct = df[df['Month'] == 'January']
df_nov = df[df['Month'] == 'February']
df_dec = df[df['Month'] == 'March']

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

# ------------------------ Total Engagements DF ---------------------------- #

# Total number of engagements:
total_engagements = len(df)
# print('Total Engagements:', total_engagements)

# ------------------------ Engagement Hours DF ---------------------------- #

# print(df['Activity Duration (minutes):'].unique())

df['Activity Duration (minutes):'] = (
    df['Activity Duration (minutes):']
    .str.lower()               # make all text lowercase
    .str.strip()               # remove leading/trailing spaces
    .replace({
        "6 hrs": 360,
        "5 hrs": 300,
        "nan": 0,
    })
)

# fill missing values with 0:
df['Activity Duration (minutes):'] = df['Activity Duration (minutes):'].fillna(0)

df['Activity Duration (minutes):'] = pd.to_numeric(df['Activity Duration (minutes):'], errors='coerce')

print(df['Activity Duration (minutes):'].unique())

df_oct = df[df['Month'] == 'January']
df_nov = df[df['Month'] == 'February']
df_dec = df[df['Month'] == 'March']

# Sum of 'Activity Duration (minutes):' dataframe converted to hours:
engagement_hours = df['Activity Duration (minutes):'].sum()/60
engagement_hours = round(engagement_hours)
# print('Sum Engagement Hours:', engagement_hours)

# Engagement hours October:
engagement_hours_oct = df_oct['Activity Duration (minutes):'].sum()/60
engagement_hours_oct = round(engagement_hours_oct)

# Engagement hours November:
engagement_hours_nov = df_nov['Activity Duration (minutes):'].sum()/60
engagement_hours_nov = round(engagement_hours_nov)

# Engagement hours December:
engagement_hours_dec = df_dec['Activity Duration (minutes):'].sum()/60
engagement_hours_dec = round(engagement_hours_dec)

# Hours DF:
df_hours_q1 = pd.DataFrame({
    'Month': ['October', 'November', 'December'],
    'Engagement Hours': [engagement_hours_oct, engagement_hours_nov, engagement_hours_dec]
})

# Engagment Hours Bar Chart:
engagement_hours_fig = px.bar(
    df_hours_q1,
    x='Month',
    y='Engagement Hours',
    color = 'Month',
    text='Engagement Hours',
    title='Q1 Engagement Hours',
    labels={
        'Engagement Hours': 'Engagement Hours',
        'Month': 'Month'
    }
).update_layout(
    title_x=0.5,
    xaxis_title='Month',
    yaxis_title='Engagement Hours',
    height=900,  # Adjust graph height
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        tickmode='array',
        tickvals=df_hours_q1['Month'].unique(),
        tickangle=-35  # Rotate x-axis labels for better readability
    ),
).update_traces(
    texttemplate='%{text}',  # Display the count value above bars
    textfont=dict(size=20),  # Increase text size in each bar
    textposition='auto',  # Automatically position text above bars
    textangle=0, # Ensure text labels are horizontal
    hovertemplate=(  # Custom hover template
        '<b>Name</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'  
    ),
)


# ------------------------ Total Travel Time DF ---------------------------- #

# sum 'Total travel time (minutes):' dataframe:
total_travel_time = df['Total travel time (minutes):'].sum()
total_travel_time = round(total_travel_time)

# --------------------------------- Activity Status DF -------------------------------- #

# Group by 'Activity Status:' dataframe
activity_status_group = df.groupby('Activity Status:').size().reset_index(name='Count')

status_fig = px.pie(
    activity_status_group,
    names='Activity Status:',
    values='Count',
).update_layout(
    title='Q1 Engagements Activity Status:',
    title_x=0.5,
    height=500,
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    )
).update_traces(
    textposition='auto',
    # textinfo='label+percent',
    texttemplate='%{value}<br>%{percent:.0%}',  # Format percentage as whole numbers
    hovertemplate='<b>Status</b>: %{label}<br><b>Count</b>: %{value}<extra></extra>'
)

# ------------------------ Person Submitting Form DF ---------------------------- #

#  Duplicate values in 'Person submitting this form:' column:

# 0           Antonio Montggery       1
# 1           Antonio Montgomery      1
# 2              Cameron Morgan       1
# 3             Kiounis Williams      6
# 4            Kiounis Williams       3
# 5             Larry Wallace Jr     31

# Create a new dataframe with 'Person submitting this form:' and 'Date of Activity'
df_person = df[['Person submitting this form:', 'Date of Activity']].copy()

# Dictionary for replacements
replacements = {
    "Larry Wallace Jr": "Larry Wallace Jr.",
    "`Larry Wallace Jr": "Larry Wallace Jr.",
    "Antonio Montggery": "Antonio Montgomery"
}

# Remove trailing whitespaces and perform the replacements
df_person['Person submitting this form:'] = (
    df_person['Person submitting this form:']
    .str.strip()
    .replace(replacements)
)

# Extract month from 'Date of activity:' column (assuming the column exists)
df_person['Month'] = df_person['Date of Activity'].dt.month_name()

# Filter for October, November, and December
df_person_q4 = df_person[df_person['Month'].isin(['October', 'November', 'December'])]

# Group the data by 'Month' and 'Person submitting this form:' and count occurrences
df_person_counts = (
    df_person_q4.groupby(['Month', 'Person submitting this form:'], sort=True)
    .size()
    .reset_index(name='Count')
)

# Define the desired month order
month_order = ['October', 'November', 'December']

# Assign categorical ordering to the 'Month' column
df_person_counts['Month'] = pd.Categorical(
    df_person_counts['Month'],
    categories=month_order,
    ordered=True
)

# Sort df
df_person_counts = df_person_counts.sort_values(by=['Month', 'Person submitting this form:'])

# Create the grouped bar chart
person_fig = px.bar(
    df_person_counts,
    x='Month',
    y='Count',
    color='Person submitting this form:',
    barmode='group',
    text='Count',
    title='Person Submitting This Form by Month',
    labels={
        'Count': 'Number of Submissions',
        'Month': 'Month',
        'Person submitting this form:': 'Person'
    }
).update_layout(
    title_x=0.5,
    xaxis_title='Month',
    yaxis_title='Count',
    height=900,  # Adjust graph height
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        tickmode='array',
        tickvals=df_person_counts['Month'].unique(),
        tickangle=-35  # Rotate x-axis labels for better readability
    ),
    legend=dict(
        title='Person',
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        xanchor="left",  # Anchor legend to the left
        y=1,  # Position legend at the top
        yanchor="top"  # Anchor legend at the top
    ),
    hovermode='x unified',  # Display unified hover info
    bargap=0.08,  # Reduce the space between bars
    bargroupgap=0,  # Reduce space between individual bars in groups
).update_traces(
    textposition='outside',  # Display text above bars
    textfont=dict(size=30),  # Increase text size in each bar
    hovertemplate=(
        '<b>Month</b>: %{x}<br>'
        '<b>Count</b>: %{y}<br>'
        '<b>Person</b>: %{color}<extra></extra>'
    ),
    customdata=df_person_counts['Person submitting this form:'].values.tolist()
).add_vline(
    x=0.5,  # Adjust the position of the line
    line_dash="dash",
    line_color="gray",
    line_width=2
).add_vline(
    x=1.5,  # Position of the second line
    line_dash="dash",
    line_color="gray",
    line_width=2
)

df_pf = df[['Person submitting this form:', 'Date of Activity']].copy()

replacements1 = {
    "Larry Wallace Jr": "Larry Wallace Jr.",
    "`Larry Wallace Jr": "Larry Wallace Jr.",
    "Antonio Montggery": "Antonio Montgomery"
}

df_pf['Person submitting this form:'] = (
    df_pf['Person submitting this form:']
    .str.strip()
    .replace(replacements1)
)

# Group by person submitting form:
df_pf = df_pf.groupby('Person submitting this form:').size().reset_index(name='Count')

# Bar chart for  Totals:
person_totals_fig = px.bar(
    df_pf,
    x='Person submitting this form:',
    y='Count',
    color='Person submitting this form:',
    text='Count',
).update_layout(
    height=850,  # Adjust graph height
    title=dict(
        x=0.5,
        text='Total Q1 Form Submissions by Person',  # Title text
        font=dict(
            size=35,  # Increase this value to make the title bigger
            family='Calibri',  # Optional: specify font family
            color='black'  # Optional: specify font color
        )
    ),
    xaxis=dict(
        tickfont=dict(size=18),  # Adjust font size for the month labels
        tickangle=-25,  # Rotate x-axis labels for better readability
        title=dict(
            text='',
            font=dict(size=20),  # Font size for the title
        ),
    ),
    yaxis=dict(
        title=dict(
            text='Number of Submissions',
            font=dict(size=22),  # Font size for the title
        ),
    ),
    bargap=0.08,  # Reduce the space between bars
).update_traces(
    texttemplate='%{text}',  # Display the count value above bars
    textfont=dict(size=20),  # Increase text size in each bar
    textposition='auto',  # Automatically position text above bars
    textangle=0, # Ensure text labels are horizontal
    hovertemplate=(  # Custom hover template
        '<b>Name</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'  
    ),
)

#  Pie chart:
person_pie = px.pie(
    df_pf,
    names='Person submitting this form:',
    values='Count',
    color='Person submitting this form:',
    height=800
).update_layout(
    title=dict(
        x=0.5,
        text='Q1 Form Submissions by Person',  # Title text
        font=dict(
            size=35,  # Increase this value to make the title bigger
            family='Calibri',  # Optional: specify font family
            color='black'  # Optional: specify font color
        ),
    ),  
).update_traces(
    rotation=90,  # Rotate pie chart 90 degrees counterclockwise
    textfont=dict(size=19),  # Increase text size in each bar
     texttemplate='%{value}<br>%{percent:.1%}',  # Format percentage as whole numbers
    hovertemplate='<b>%{label}</b>: %{value}<extra></extra>'
)

# --------------------- BMHC Administrative Activity DF ------------------------ # 

# Create a copy of the relevant columns
df_admin = df[['BMHC Administrative Activity:', 'Date of Activity']].copy()

# Extract month from 'Date of Activity' column
df_admin['Month'] = df_admin['Date of Activity'].dt.month_name()

# Filter for October, November, and December
df_admin_q4 = df_admin[df_admin['Month'].isin(['October', 'November', 'December'])]

# Group the data by 'Month' and 'BMHC Administrative Activity:' and count occurrences
df_admin_counts = (
    df_admin_q4.groupby(['Month', 'BMHC Administrative Activity:'], sort=True)
    .size()
    .reset_index(name='Count')
)

# Define the desired month order
month_order = ['October', 'November', 'December']

# Assign categorical ordering to the 'Month' column
df_admin_counts['Month'] = pd.Categorical(
    df_admin_counts['Month'],
    categories=month_order,
    ordered=True
)

# Sort df:
df_admin_counts = df_admin_counts.sort_values(by=['Month', 'BMHC Administrative Activity:'])

# Create the grouped bar chart
admin_fig = px.bar(
    df_admin_counts,
    x='Month',
    y='Count',
    color='BMHC Administrative Activity:',
    barmode='group',
    text='Count',
    title='BMHC Administrative Activity by Month',
    labels={
        'Count': 'Number of Activities',
        'Month': 'Month',
        'BMHC Administrative Activity:': 'Administrative Activity'
    }
).update_layout(
    title_x=0.5,
    xaxis_title='Month',
    yaxis_title='Count',
    height=900,  # Adjust graph height
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        tickmode='array',
        tickvals=df_admin_counts['Month'].unique(),
        tickangle=-35  # Rotate x-axis labels for better readability
    ),
    legend=dict(
        title='Administrative Activity',
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        xanchor="left",  # Anchor legend to the left
        y=1,  # Position legend at the top
        yanchor="top"  # Anchor legend at the top
    ),
    hovermode='x unified'  # Display unified hover info
).update_traces(
    textposition='outside',  # Display text above bars
    textfont=dict(size=30),  # Increase text size in each bar
    hovertemplate=(
        '<br>'
        '<b>Count: </b>%{y}<br>'  # Count
    ),
    customdata=df_admin_counts['BMHC Administrative Activity:'].values.tolist()
)

# --------------------- Care Network Activity DF ------------------------ #

custom_colors = {
    'January': 'Blues',
    'February': 'Greens',
    'March': 'Oranges',
    'April': 'Purples',
    'May': 'Reds',
    'June': 'Greys',
    'July': 'YlGn',
    'August': 'YlOrBr',
    'September': 'PuRd',
    'October': 'BuPu',
    'November': 'GnBu',
    'December': 'YlGnBu',
# The code snippet provided is a Python dictionary with a key-value pair. The key is 'Count'
# and the value is 'Number of Submissions'. This dictionary is used to store information
# related to the count of submissions.
}

# Group by 'Care Network Activity:' dataframe:
care_network_activity = df.groupby('Care Network Activity:').size().reset_index(name='Count')

# Create a copy of the relevant columns
df_care = df[['Care Network Activity:', 'Date of Activity']].copy()

# Extract month from 'Date of Activity' column
df_care['Month'] = df_care['Date of Activity'].dt.month_name()

# Filter for October, November, and December
df_care_q4 = df_care[df_care['Month'].isin(['October', 'November', 'December'])]

# Group the data by 'Month' and 'BMHC Administrative Activity:' and count occurrences
df_care_counts = (
    df_care_q4.groupby(['Month', 'Care Network Activity:'], sort=True)
    .size()
    .reset_index(name='Count')
)

# Define the desired month order
month_order = ['October', 'November', 'December']

# Assign categorical ordering to the 'Month' column
df_care_counts['Month'] = pd.Categorical(
    df_care_counts['Month'],
    categories=month_order,
    ordered=True
)

# Sort df
df_care_counts = df_care_counts.sort_values(by=['Month', 'Care Network Activity:'])

# Create the grouped bar chart
care_fig = px.bar(
    df_care_counts,
    x='Month',
    y='Count',
    color='Care Network Activity:',
    barmode='group',
    text='Count',
    title='BMHC Care Network Activity by Month',
    labels={
        'Count': 'Number of Activities',
        'Month': 'Month',
        'Care Network Activity:': 'Care Network Activity:'
    }
).update_layout(
    title_x=0.5,
    xaxis_title='Month',
    yaxis_title='Count',
    height=900,  # Adjust graph height
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        tickmode='array',
        tickvals=df_care_counts['Month'].unique(),
        tickangle=-35  # Rotate x-axis labels for better readability
    ),
    legend=dict(
        title='Activity',
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        xanchor="left",  # Anchor legend to the left
        y=1,  # Position legend at the top
        yanchor="top"  # Anchor legend at the top
    ),
    hovermode='x unified'  # Display unified hover info
).update_traces(
    textposition='outside',  # Display text above bars
    hovertemplate=(
        '<br>'
        '<b>Count: </b>%{y}<br>'  # Count
    ),
    customdata=df_care_counts['Care Network Activity:'].values.tolist()
)

# Group by Care Network Activity:
df_care_group = df.groupby('Care Network Activity:').size().reset_index(name='Count')

# Bar chart for  Totals:
care_totals_fig = px.bar(
    df_care_group,
    x='Care Network Activity:',
    y='Count',
    color='Care Network Activity:',
    text='Count',
).update_layout(
    height=850,  # Adjust graph height
    title=dict(
        x=0.5,
        text='Care Network Activities Q1 Totals',  # Title text
        font=dict(
            size=35,  # Increase this value to make the title bigger
            family='Calibri',  # Optional: specify font family
            color='black'  # Optional: specify font color
        )
    ),
    xaxis=dict(
        tickfont=dict(size=18),  # Adjust font size for the month labels
        tickangle=-25,  # Rotate x-axis labels for better readability
        title=dict(
            text=None,
            font=dict(size=20),  # Font size for the title
        ),
    ),
    yaxis=dict(
        title=dict(
            text='Number of Activities',
            font=dict(size=22),  # Font size for the title
        ),
    ),
    bargap=0.08,  # Reduce the space between bars
).update_traces(
    texttemplate='%{text}',  # Display the count value above bars
    textfont=dict(size=20),  # Increase text size in each bar
    textposition='auto',  # Automatically position text above bars
    textangle=0, # Ensure text labels are horizontal
    hovertemplate=(  # Custom hover template
        '<b>Activity</b>: %{label}<br><b>Count</b>: %{y}<extra></extra>'  
    ),
)

#  Pie chart:
care_pie = px.pie(
    df_care_group,
    names='Care Network Activity:',
    values='Count',
    color='Care Network Activity:',
    height=850
).update_layout(
    title=dict(
        x=0.5,
        text='Q1 Care Network Activity',  # Title text
        font=dict(
            size=35,  # Increase this value to make the title bigger
            family='Calibri',  # Optional: specify font family
            color='black'  # Optional: specify font color
        ),
    )  # Center-align the title
).update_traces(
    textfont=dict(size=19),  # Increase text size in each bar
    texttemplate='%{value}<br>%{percent:.1%}',  # Format percentage as whole numbers
    hovertemplate='<b>%{label}</b>: %{value}<extra></extra>'
)

# Care Network Activity Treemap:
care_tree = px.treemap(
    df_care_counts,
    path=['Month', 'Care Network Activity:'],
    values='Count',
    color_continuous_scale='YlOrBr',
    title='BMHC Care Network Activity by Month',
    height=1000,
    labels={
        'Count': 'Number of Activities',
        'Month': 'Month',
        'Care Network Activity:': 'Care Network Activity:'
    }
).update_layout(
    title_x=0.5,
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    )
).update_traces(
    textinfo='label+value',  # Show label, count, and percent of parent
    textfont=dict(size=30),  # Increase text size in each bar
    hovertemplate='<b>%{label}</b>: %{value}<extra></extra>'
)

# Care Network Activity Sunburst:
care_sunburst = px.sunburst(
    df_care_counts,
    path=['Month', 'Care Network Activity:'],
    values='Count',
    color='Count',
    color_continuous_scale='YlOrBr',
    title='BMHC Care Network Activity by Month',
    labels={
        'Count': 'Number of Activities',
        'Month': 'Month',
        'Care Network Activity:': 'Care Network Activity:'
    }
).update_layout(
    height=700,
    title_x=0.5,
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    )
).update_traces(
    textinfo='label+value',  # Show label, count, and percent of parent
    textfont=dict(size=30),  # Increase text size in each bar
    hovertemplate='<b>%{label}</b>: %{value}<extra></extra>'
)

# Care Network Activity Pie chart:
# care_pie = px.pie(
#     df_care_counts,
#     names='Care Network Activity:',
#     values='Count',
#     color='Care Network Activity:',
#     # color_continuous_scale='YlOrBr',
#     title='BMHC Care Network Activity',
#     labels={
#         'Count': 'Number of Activities',
#         'Month': 'Month',
#         'Care Network Activity:': 'Care Network Activity:'
#     }
# ).update_layout(
#     height=900,
#     # width=2000,
#     title_x=0.5,
#     font=dict(
#         family='Calibri',
#         size=17,
#         color='black'
#     )
# ).update_traces(
#     textinfo='label+percent',  # Show label, count, and percent of parent
#     textfont=dict(size=15),  # Increase text size in each bar
#     hovertemplate='<b>%{label}</b>: %{value}<extra></extra>'
# )

# --------------------- Community Outreach Activity DF ------------------------ #

# Create a copy of the relevant columns
df_comm = df[['Community Outreach Activity:', 'Date of Activity']].copy()

# Extract month from 'Date of Activity' column
df_comm['Month'] = df_comm['Date of Activity'].dt.month_name()

# Filter for October, November, and December
df_comm_q4 = df_comm[df_comm['Month'].isin(['October', 'November', 'December'])]

# Group the data by 'Month' and 'Community Outreach Activity:' and count occurrences
df_comm_counts = (
    df_comm_q4.groupby(['Month', 'Community Outreach Activity:'], sort=False)
    .size()
    .reset_index(name='Count')
)

# Define the desired month order
month_order = ['October', 'November', 'December']

# Assign categorical ordering to the 'Month' column
df_comm_counts['Month'] = pd.Categorical(
    df_comm_counts['Month'],
    categories=month_order,
    ordered=True
)

# Sort df
df_comm_counts = df_comm_counts.sort_values(by=['Month', 'Community Outreach Activity:'])

# Create the grouped bar chart
comm_fig = px.bar(
    df_comm_counts,
    x='Month',
    y='Count',
    color='Community Outreach Activity:',
    barmode='group',
    text='Count',
    title='Community Outreach Activity by Month',
    labels={
        'Count': 'Number of Activities',
        'Month': 'Month',
        'Community Outreach Activity:': 'Community Outreach Activity'
    }
).update_layout(
    title_x=0.5,
    xaxis_title='Month',
    yaxis_title='Count',
    height=900,  # Adjust graph height
    font=dict(
        family='Calibri',
        size=17,
        color='black'
    ),
    xaxis=dict(
        tickmode='array',
        tickvals=df_comm_counts['Month'].unique(),
        tickangle=-35  # Rotate x-axis labels for better readability
    ),
    legend=dict(
        title='Activity',
        orientation="v",  # Vertical legend
        x=1.05,  # Position legend to the right
        xanchor="left",  # Anchor legend to the left
        y=1,  # Position legend at the top
        yanchor="top"  # Anchor legend at the top
    ),
    hovermode='x unified'  # Display unified hover info
).update_traces(
    textposition='outside',  # Display text above bars
    hovertemplate=(
        '<br>'
        '<b>Count: </b>%{y}<br>'  # Count
    ),
    customdata=df_comm_counts['Community Outreach Activity:'].values.tolist()
)

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
    height=900,
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
              'BMHC Partner Engagement Report Q2 2025', 
              className='title'),
          html.H2( 
              '01/01/2025 - 3/31/2024', 
              className='title2'),
          html.Div(
              className='btn-box', 
              children=[
                  html.A(
                    'Repo',
                    href='https://github.com/CxLos/Eng_Q2_2025',
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
html.Div(
    className='row0',
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
                children=['Q1 Total Engagement Hours:']
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


html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    figure=engagement_hours_fig
                )
            ]
        )
    ]
),

# ROW 1
html.Div(
    className='row1',
    children=[
        html.Div(
            className='graph1',
            children=[
                dcc.Graph(
                    figure=status_fig
                )
            ]
        ),
        html.Div(
            className='graph44',
            children=[
            html.Div(
                className='high5',
                children=['Total Travel Time:']
            ),
            html.Div(
                className='circle1',
                children=[
                    html.Div(
                        className='hilite',
                        children=[
                            html.H1(
                            className='high6',
                            children=[total_travel_time]
                    ),
                        ]
                    )
 
                ],
            ),
            ]
        ),
    ]
),

# ROW 
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    figure=person_fig
                )
            ]
        )
    ]
),

# ROW 
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    figure=person_totals_fig
                )
            ]
        )
    ]
),
# ROW 
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    figure=person_pie
                )
            ]
        )
    ]
),
# ROW 
# html.Div(
#     className='row3',
#     children=[
#         html.Div(
#             className='graph0',
#             children=[
#                 dcc.Graph(
#                     figure=admin_fig
#                 )
#             ]
#         )
#     ]
# ),

# ROW 
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    figure=care_fig
                )
            ]
        )
    ]
),
# ROW 
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    figure=care_totals_fig
                )
            ]
        )
    ]
),
# ROW 
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                dcc.Graph(
                    figure=care_pie
                )
            ]
        )
    ]
),
# ROW 
# html.Div(
#     className='row3',
#     children=[
#         html.Div(
#             className='graph0',
#             children=[
#                 dcc.Graph(
#                     figure=comm_fig
#                 )
#             ]
#         )
#     ]
# ),

html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph0',
            children=[
                html.Div(
                    className='table',
                    children=[
                        html.H1(
                            className='table-title',
                            children='Engagements Table'
                        )
                    ]
                ),
                html.Div(
                    className='table2', 
                    children=[
                        dcc.Graph(
                            className='data',
                            figure=engagement_table
                        )
                    ]
                )
            ]
        ),
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