import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Provide explanations or insights below the charts if necessary
st.markdown("### Airtel Hourly Data Visualization for Selected Date Range")
# st.write("Airtel Hour Wise Data")

df = pd.read_csv("Airtel_Hour_Wise_Data_202310291658.csv")

# Convert date column to datetime objects
df["my_date"] = pd.to_datetime(df["my_date"])

# # Display the DataFrame in Streamlit
# st.write("Data from CSV File:")
# st.dataframe(df)



# # sidebar to select particular days
# st.sidebar.header("Please Filter Here:")
# selected_dates = st.sidebar.multiselect(
#     "Select the My date:",
#     options=df["my_date"].unique(),
#     default=[df["my_date"].unique()[0]]  # Select the first date as the default
# )

# filtered_data = df[df["my_date"].isin(selected_dates)]



# Create a sidebar to select the date range
st.sidebar.header("Date Range Selection")

# Set a default value for start_date within the allowed range
min_date = df["my_date"].min()
max_date = df["my_date"].max()
default_start_date = max_date - timedelta(days=7)  # Default to 7 days before the max date

# Select the start date
start_date = st.sidebar.date_input("Select Start Date", min_value=min_date, max_value=max_date, value=default_start_date)

# Determine the maximum allowed end date based on the start date and a maximum of 7 days
max_allowed_end_date = start_date + timedelta(days=7)

# Select the end date within the allowed range
end_date = st.sidebar.date_input("Select End Date", min_value=start_date, max_value=max_allowed_end_date, value=max_allowed_end_date)

# Convert start_date and end_date to datetime64[ns]
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# # Filter the data for the selected date range
filtered_data = df[(df["my_date"] >= start_date) & (df["my_date"] <= end_date)]



# # Create a line chart for hourly  ##
# st.header("Hourly Data Visualization")


# Combine 'my_hour' and 'my_date' into a new column 'Date and Hour of the Day'
filtered_data['Date and Hour of the Day'] = filtered_data['my_date'].dt.strftime('%Y-%m-%d') + ' ' + filtered_data['my_hour'].astype(str)



# Create a constant color for all dates (in this example, using black)
filtered_data['color'] = 'black'


# Create a bar plot with larger size
fig_bar = px.bar(
    filtered_data,
    x='Date and Hour of the Day',
    y='sum_of_amount',
    # color='my_date',  # Color points by date
    color='color',
    title='Bar Plot for Selected Date Range',
    height=600,
    width=1000,
)

st.plotly_chart(fig_bar, use_container_width=True)




# Sort the data by date and hour to ensure correct sequence
filtered_data = filtered_data.sort_values(by=["my_date", "my_hour"])

# Create a line chart where endpoints connect to the starting points of the next date
fig_line = px.line(
    filtered_data,
    x='Date and Hour of the Day',
    y='sum_of_amount',
    color='color',  # Color lines by date
    title='Line Plot for Selected Date Range',
    height=600,
    width=1000,
    category_orders={"my_date": filtered_data["my_date"].unique()}  # Ensure the date sequence is correct
)

st.plotly_chart(fig_line, use_container_width=True)





## showing all selected dates in multiple charts ###


# Create a layout with two columns of equal width
# col1, col2 = st.columns(2)

# # Display bar charts in the first column
# with col1:
#     st.header("Bar Charts for Selected Date Range")
#     for date in filtered_data["my_date"].unique():
#         data_for_date = filtered_data[filtered_data["my_date"] == date]
#         fig_bar = px.bar(data_for_date, x='my_hour', y='sum_of_amount', title=f'Hourly Data for {date}')
#         st.plotly_chart(fig_bar, use_container_width=True)




# # Display bar charts in the first column
# with col2:
#     st.header("Line Charts for Selected Date Range")
#     for date in filtered_data["my_date"].unique():
#         data_for_date = filtered_data[filtered_data["my_date"] == date]
#         print(type(data_for_date))
#         fig_line = px.line(data_for_date, x='my_hour', y='sum_of_amount', title=f'Hourly Data for {date}')
#         st.plotly_chart(fig_line, use_container_width=True)









### showing multiple selected dates together in a single chart ###


# # Create a layout with two columns of equal width
# col1, col2 = st.columns(2)

# # Display the bar chart for the selected date range
# st.header("Bar Chart for Selected Date Range")
# fig_bar = px.bar(filtered_data, x='my_date', y='sum_of_amount', title="Hourly Data")
# st.plotly_chart(fig_bar, use_container_width=True)

# # Display the line chart for the selected date range
# st.header("Line Chart for Selected Date Range")
# fig_line = px.line(filtered_data, x='my_date', y='sum_of_amount', title="Hourly Data")
# st.plotly_chart(fig_line, use_container_width=True)



# # Display filtered data
# st.subheader("Filtered Data")
# st.dataframe(filtered_data)





















       
        

