import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


df = pd.read_csv("Airtel_Hour_Wise_Data_202310291658.csv")

# Streamlit app layout
st.set_page_config(layout="wide")

# Convert date column to datetime objects
df["my_date"] = pd.to_datetime(df["my_date"])

# # Display the DataFrame in Streamlit
# st.write("Data from CSV File:")
# st.dataframe(df)


# Set the name of the dashboard
st.title("Airtel Hourly Data 🔢 Dashboard")

st.markdown("---")


# Define a custom Streamlit theme with a light lavender color scheme
custom_css = f"""
    <style>
    .stApp {{
        background-color: #E6E6FA; /* Light Lavender */
    }}
    .stMarkdown, .stText {{
        color: #333333; /* Dark Gray Text */
    }}
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)



col1, col2 = st.columns(2)

## Date Range Selection ##
with col1:
# Create a subheader to select the date range
 st.subheader("Date Range Selection")

# Set a default value for start_date within the allowed range
min_date = df["my_date"].min()
max_date = df["my_date"].max()
default_start_date = max_date - timedelta(days=7)  # Default to 7 days before the max date

with col1:
# Select the start date
 start_date = st.date_input("Select Start Date", min_value=min_date, max_value=max_date, value=default_start_date)

# Determine the maximum allowed end date based on the start date and a maximum of 7 days
max_allowed_end_date = start_date + timedelta(days=7)

with col1:
# Select the end date within the allowed range
 end_date = st.date_input("Select End Date", min_value=start_date, max_value=max_allowed_end_date, value=max_allowed_end_date)

# Convert start_date and end_date to datetime64[ns]
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter the data for the selected date range
filtered_data = df[(df["my_date"] >= start_date) & (df["my_date"] <= end_date)]

st.markdown("---")





# KPIS #

# Calculate KPIs for the last 30 days' usage data
last_30_days_data = filtered_data.tail(30) 
# last_30_days_data = filtered_data[filtered_data['my_date'] >= pd.to_datetime('today') - pd.DateOffset(days=30)] 

#Total Usage Amount
total_usage_last_30_days = last_30_days_data['sum_of_amount'].sum()

 # Average Usage Amount
average_daily_usage_last_30_days = total_usage_last_30_days / 30 

 # Highest Usage Amount
max_daily_usage_last_30_days = last_30_days_data.groupby('my_date')['sum_of_amount'].max().max()

 # Lowest Usage Amount
min_daily_usage_last_30_days = last_30_days_data.groupby('my_date')['sum_of_amount'].min().min()



# Display the KPIS Title
# Define the color and border properties for the box
box_style = "background-color: #3498db; padding: 4px; border-radius: 4px;"
# Display the KPIS Title in a colored box
st.sidebar.markdown(f"<div style='{box_style}'><h4 style='color: white; font-size: 16px;'>Last 30 Days Usage Summary</h4></div>", unsafe_allow_html=True)



# Define the box styles for each KPI   #87CEEB
box_style_total_usage = "background-color: #87CEEB; padding: 5px; border-radius: 5px;"
box_style_average_usage = "background-color: #87CEEB; padding: 5px; border-radius: 5px;"
box_style_highest_usage = "background-color: #87CEEB; padding: 5px; border-radius: 5px;"
box_style_lowest_usage = "background-color: #87CEEB; padding: 5px; border-radius: 5px;"

# Total Usage Amount Display
total_usage_formatted = "{:,.2f}".format(total_usage_last_30_days)
st.sidebar.markdown(f"<div style='{box_style_total_usage}'><h7 style='color: white; font-size: 15px;'>Total Usage Amount:</h7></div>", unsafe_allow_html=True)
st.sidebar.subheader(f"৳ {total_usage_formatted}")



# Average Usage Amount Display
average_daily_usage_formatted = "{:,.2f}".format(average_daily_usage_last_30_days)
st.sidebar.markdown(f"<div style='{box_style_average_usage}'><h7 style='color: white; font-size: 15px;'>Average Usage Amount:</h7></div>", unsafe_allow_html=True)
# st.sidebar.subheader(f"৳ {average_daily_usage_last_30_days:.2f}")
st.sidebar.subheader(f"৳ {average_daily_usage_formatted}")

# Highest Usage Amount Display
max_daily_usage_formatted = "{:,.2f}".format(max_daily_usage_last_30_days)
st.sidebar.markdown(f"<div style='{box_style_highest_usage}'><h7 style='color: white; font-size: 15px;'>Highest Usage Amount:</h7></div>", unsafe_allow_html=True)
# st.sidebar.subheader(f"৳ {max_daily_usage_last_30_days:.2f}")
st.sidebar.subheader(f"৳ {max_daily_usage_formatted}")

# Lowest Usage Amount Display
min_daily_usage_formatted = "{:,.2f}".format(min_daily_usage_last_30_days)
st.sidebar.markdown(f"<div style='{box_style_lowest_usage}'><h7 style='color: white; font-size: 15px;'>Lowest Usage Amount:</h7></div>", unsafe_allow_html=True)
# st.sidebar.subheader(f"৳ {min_daily_usage_last_30_days:.2f}")
st.sidebar.subheader(f"৳ {min_daily_usage_formatted}")




# Combine 'my_hour' and 'my_date' into a new column 'Date and Hour of the Day'
filtered_data['Date and Hour of the Day'] = filtered_data['my_date'].dt.strftime('%Y-%m-%d') + ' ' + filtered_data['my_hour'].astype(str)



### KPIS ###
# Calculate KPIs for total usage amount in the selected date range
total_usage = filtered_data['sum_of_amount'].sum()

# Calculate the hour with the highest usage for each day
highest_usage_hour = filtered_data.groupby(['my_date'])['sum_of_amount'].idxmax()
highest_usage_hour_data = filtered_data.loc[highest_usage_hour]


# Create two columns to display content side by side
# col1, col2 = st.columns(2)

with col2:
    st.subheader("Total Usage Amount:")
    st.subheader(f"৳ {total_usage_formatted}")




# st.subheader("Highest Usage Hour Bar Chart:")

#     # Create a custom bar chart with amounts on top of bars
# fig = go.Figure()
    
# for date, data in highest_usage_hour_data.groupby('my_date'):
#         highest_hour = data['my_hour'].values[0]
#         am_pm = "AM" if highest_hour < 12 else "PM"
#         formatted_hour = f"{highest_hour % 12} {am_pm}"
#         fig.add_trace(go.Bar(x=[f"{date.strftime('%Y-%m-%d')}: {formatted_hour}"], y=[data['sum_of_amount'].values[0]], name=date.strftime('%Y-%d-%m')))
        
# fig.update_layout(barmode='group',
#         xaxis_title="Date",
#         yaxis_title="Amount",
#         height=250
#     )

# st.plotly_chart(fig, use_container_width=True)


# st.subheader("Highest Usage Hour Line Chart:")

# # Create a custom line chart with highest usage hours
# fig_line_chart = go.Figure()

# for date, data in highest_usage_hour_data.groupby('my_date'):
#     highest_hour = data['my_hour'].values[0]
#     am_pm = "AM" if highest_hour < 12 else "PM"
#     formatted_hour = f"{highest_hour % 12} {am_pm}"
#     fig_line_chart.add_trace(go.Scatter(x=[f"{date.strftime('%Y-%m-%d')} {formatted_hour}"], y=[data['sum_of_amount'].values[0]],
#                                         mode='lines+markers', name=date.strftime('%Y-%d-%m')))

# fig_line_chart.update_layout(
#     title="Highest Usage Hour Line Chart",
#     xaxis_title="Date and Hour",
#     yaxis_title="Amount",
#     height=250
# )

# st.plotly_chart(fig_line_chart, use_container_width=True)


# st.markdown("---")






# # Display filtered data
# st.subheader("Filtered Data")
# st.dataframe(filtered_data)






# Usage Charts
st.subheader("Usage Charts:")

# Create a custom bar chart with amounts on top of bars
fig_bar_chart = go.Figure()

for date, data in highest_usage_hour_data.groupby('my_date'):
    highest_hour = data['my_hour'].values[0]
    am_pm = "AM" if highest_hour < 12 else "PM"
    formatted_hour = f"{highest_hour % 12} {am_pm}"
    fig_bar_chart.add_trace(go.Bar(x=[f"{date.strftime('%Y-%m-%d')}: {formatted_hour}"], y=[data['sum_of_amount'].values[0]], name=date.strftime('%Y-%d-%m')))

fig_bar_chart.update_layout(
    barmode='group',
    title="Highest Usage Hour Bar Chart",
    xaxis_title="Date and Hour",
    yaxis_title="Amount",
    height=350,
    width=550,
)

# Create a custom line chart with highest usage hours
fig_line_chart = go.Figure()

for date, data in highest_usage_hour_data.groupby('my_date'):
    highest_hour = data['my_hour'].values[0]
    am_pm = "AM" if highest_hour < 12 else "PM"
    formatted_hour = f"{highest_hour % 12} {am_pm}"
    fig_line_chart.add_trace(go.Scatter(x=[f"{date.strftime('%Y-%m-%d')} {formatted_hour}"], y=[data['sum_of_amount'].values[0]],
                                         mode='lines+markers', name=date.strftime('%Y-%d-%m')))

    fig_line_chart.update_layout(
    title="Highest Usage Hour Line Chart",
    xaxis_title="Date and Hour",
    yaxis_title="Amount",
    height=350,
    width=550,
)

# Display the charts side by side
col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(fig_bar_chart, use_container_width=True)

with col4:
    st.plotly_chart(fig_line_chart, use_container_width=True)
    


# Date Range Charts
st.subheader("Date Range Charts:")

# Create a constant color for all dates (in this example, using black)
filtered_data['color'] = 'black'

# Create a bar plot with larger size
fig_bar = px.bar(
    filtered_data,
    x='Date and Hour of the Day',
    y='sum_of_amount',
    color='color',
    title='Selected Date Range Bar Plot',
    height=350,
    width=550,
)


# Sort the data by date and hour to ensure correct sequence
filtered_data = filtered_data.sort_values(by=["my_date", "my_hour"])

# Create a line chart where endpoints connect to the starting points of the next date
fig_line = px.line(
    filtered_data,
    x='Date and Hour of the Day',
    y='sum_of_amount',
    color='color',
    title='Selected Date Range Line Plot',
    height=350,
    width=550,
    category_orders={"my_date": filtered_data["my_date"].unique()}  # Ensure the date sequence is correct
)



# Display the charts side by side in the second row
col5, col6 = st.columns(2)

with col5:
    st.plotly_chart(fig_bar, use_container_width=True)

with col6:
    st.plotly_chart(fig_line, use_container_width=True)














       
        

