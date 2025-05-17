import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import time
import scipy.interpolate as spi
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import plotly.subplots as sp
import mysql.connector
import os
from utility import connect_mysql

BASE_DIR = os.path.abspath(os.path.dirname("__file__"))
CRED_DIR = os.path.join(BASE_DIR, "cred")
CRED_PATH = os.path.join(CRED_DIR, "credentials.json")
LOGO_DIR = os.path.join(BASE_DIR, "logo")

image_file = "airtel_logo.png"
image_path = os.path.join(LOGO_DIR, image_file)



# Function to fetch data from the database
def fetch_table_data_1():
    try:
        # Connect to the MySQL server
        myconn = connect_mysql(CRED_PATH)

        query = "SELECT * FROM Airtel_Hour_Wise_Data" 
        df_actual = pd.read_sql(query, myconn)
        myconn.close()
        return df_actual
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return pd.DataFrame()
    

# Function to fetch data from the database
def fetch_table_data_2():
    try:
        # Connect to the MySQL server
        myconn = connect_mysql(CRED_PATH)

        query = '''SELECT
                    *
                FROM
                    vr.airtel_daily_prediction
                ORDER BY
                    my_date ASC,
                    my_hour ASC;
                '''
        df_actual = pd.read_sql(query, myconn)
        myconn.close()
        return df_actual
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return pd.DataFrame()

   
def app():
    df_Usage = fetch_table_data_1()
    df_Prediction = fetch_table_data_2()
   
    if df_Usage.empty or df_Prediction.empty:
        st.error("No data fetched from the database.")
        return
    
    # Convert date column to datetime objects
    df_Usage["my_date"] = pd.to_datetime(df_Usage["my_date"])
    df_Prediction["my_date"] = pd.to_datetime(df_Prediction["my_date"])

    # Combine 'my_hour' and 'my_date' into a new column 'Date and Hour of the Day'
    df_Usage['Date and Hour of the Day'] = df_Usage['my_date'].dt.strftime('%Y-%m-%d') + ' ' + df_Usage['my_hour'].astype(str).str.zfill(2)
    df_Prediction['Date and Hour of the Day'] = df_Prediction['my_date'].dt.strftime('%Y-%m-%d') + ' ' + df_Prediction['my_hour'].astype(str).str.zfill(2)

    # Filter data for usage (last 7 days)
    last_3_days_data = df_Usage.tail(24 * 3)

    # Filter data for prediction (last 8 days)
    last_4_days_data = df_Prediction.tail(24 * 4)

    # Filter data for the forecast (last 1 day)
    last_1_day_data = df_Prediction.tail(24)

     
## dashboard title ##
       
    # Set up Streamlit columns
    col1, col2  = st.columns([1, 8])  

    # with col2:
    #     st.title("Airtel Usage Dashboard 📊")
    with col2:
        st.markdown(
            f'<h1 style="color:#91171f; font-size:40px;"><stong>Airtel Usage Dashboard 📊</strong></h1>',
            unsafe_allow_html=True
        )

    with col1:
        st.image(image_path, width=65)
    
    st.markdown("---")


    # Define a custom Streamlit theme with a light lavender color scheme
    custom_css = f"""
           <style>
        .stApp {{
            background-color: #F5E4E0; /* Light Lavender */
        }}
       .stMarkdown, .stText {{
           color: #333333; /* Dark Gray Text */
          }}
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    
    
## Date Range Selection Calendar ##

    box_style_total_usage = "background-color: #6a040f; padding: 4px; border-radius: 4px; display: inline-block;"
    st.markdown(f"<div style='text-align: center; {box_style_total_usage}'><h4 style='color: white; font-size: 16px;'>Daily Usage Analytics :</h4></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns((1, 2, 1))    
    
    with col1:    
  
      # Create a subheader to select the date range
      st.subheader("Date Range Selection")

      # Set a default value for start_date within the allowed range
      min_date = df_Usage["my_date"].min()
      max_date = df_Usage["my_date"].max()
      default_start_date = max_date - timedelta(days=7)  # Default to 7 days before the max date


      # Select the start date
      start_date = st.date_input("Select Start Date", min_value=min_date, max_value=max_date, value=default_start_date)

      # Determine the maximum allowed end date based on the start date and a maximum of 7 days
      max_allowed_end_date = start_date + timedelta(days=7)


      # Select the end date within the allowed range
      end_date = st.date_input("Select End Date", min_value=start_date, max_value=max_allowed_end_date, value=max_allowed_end_date)

      # Convert start_date and end_date to datetime64[ns]
      start_date = pd.to_datetime(start_date)
      end_date = pd.to_datetime(end_date)
    
    
    
 ## Selected Date Range Visualization ##
    
    # Filter the data for the selected date range
    filtered_data = df_Usage[(df_Usage["my_date"] >= start_date) & (df_Usage["my_date"] <= end_date)]

    # Combine 'my_hour' and 'my_date' into a new column 'Date and Hour of the Day'
    filtered_data['Date and Hour of the Day'] = filtered_data['my_date'].dt.strftime('%Y-%m-%d') + ' ' + filtered_data['my_hour'].astype(str).str.zfill(2)   
 
    
    
## Date Range Charts ##

    # Create a constant color for all dates (in this example, using black)
    filtered_data['color'] = 'black'

    # Create a bar plot with larger size
    fig_bar = px.bar(
       filtered_data,
       x='Date and Hour of the Day',
       y='sum_of_amount',
       title='Usage History For Selected Date Range',
       height=350,
       width=550,
       labels={
          'Date and Hour of the Day': 'Date and Hour', 
          'sum_of_amount': 'Total Amount'  
    },
       
    )
    # Update hovertemplate to include custom information
    fig_bar.update_traces(
        hovertemplate='<b>Date and Hour:</b> %{x}<br><b>Total Amount:</b> %{y:.3s}<extra></extra>',  
        marker_color='#ba181b'
    )
    
    # Update the layout to make the background transparent
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    with col2:
      st.plotly_chart(fig_bar, use_container_width=True)

    
    
    
## KPIS for Selected date range ##
    
    # Calculate total usage amount for the selected date range
    total_usage_selected_range = filtered_data['sum_of_amount'].sum()
    # Helper function to format amounts
    def format_amount(amount):
        if amount.is_integer():
            return f"৳ {amount:,.0f}"
        else:
            return f"৳ {amount:,.2f}"
    
    # Format total usage amount for the selected date range
    total_usage_selected_range_formatted = format_amount(total_usage_selected_range)

    
    # Display KPIs with custom font size and color in a box
    with col3:
    # Apply custom styling to the header
     st.markdown(
        '<div style="background-color:#c75146; padding:10px; border-radius:5px;">'
        '<h7 style="font-size:16px; color:white;">Total Usage Amount (selected date range)</h7>'
        '</div>',
        unsafe_allow_html=True
    )
    
     st.markdown(
         f'<p style="font-size:24px; ">{total_usage_selected_range_formatted}</p>',
         unsafe_allow_html=True
    )
     
    st.markdown("---")
    
    
## Highest Hourly Usage Charts ##

    #Title
    box_style_total_usage = "background-color: #6a040f; padding: 4px; border-radius: 4px; display: inline-block;"
    st.markdown(f"<div style='text-align: center; {box_style_total_usage}'><h4 style='color: white; font-size: 16px;'>Hourly Usage Analytics:</h4></div>", unsafe_allow_html=True)

## bar chart ##

    # Calculate the hour with the highest usage for each day
    highest_usage_hour_data = filtered_data.groupby(['my_date', 'my_hour']).agg({'sum_of_amount': 'sum'}).reset_index()

    # Create a custom bar chart with amounts on top of bars
    fig_bar_chart = go.Figure()
    formatted_hours = []
    max_amounts = []

    for date, data in highest_usage_hour_data.groupby('my_date'):
        highest_hour = data.loc[data['sum_of_amount'].idxmax(), 'my_hour']
        am_pm = "AM" if highest_hour < 12 else "PM"
        formatted_hour = f"{highest_hour % 12} {am_pm}, {date.strftime('%b%d')}"
        formatted_hours.append(formatted_hour)
        max_amounts.append(data['sum_of_amount'].max())
    # Format amounts to remove fractional part
    formatted_max_amounts = [f"{int(amount):,}" for amount in max_amounts]

    fig_bar_chart.add_trace(go.Bar(
        x=formatted_hours,
        y=max_amounts,
        text=formatted_max_amounts,
        textposition='inside',
        textangle=0,
        insidetextanchor='middle',
        name=date.strftime('%Y-%m-%d'),
        hovertemplate='<b>Date and Hour:</b> %{x}<br><b>Amount:</b> %{y:.3s}<extra></extra>',
        marker_color='#ba181b' 
    ))

    fig_bar_chart.update_layout(
        barmode='group',
        title="Highest Hourly Usage On Each Day",
        xaxis_title="Date and Hour",
        yaxis_title="Amount",
        height=350,
        width=550,
    )
    
    # Update the layout to make the background transparent
    fig_bar_chart.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )


## pie chart ##

    # Create a new column 'Time Interval'
    filtered_data['Time Interval'] = pd.cut(filtered_data['my_hour'], bins=[0, 5, 11, 17, 23], labels=['Midnight to 6AM', '6AM to 12PM', '12PM to 6PM', '6PM to Midnight'])

    # Group the data by 'Time Interval' and calculate the sum of amounts
    pie_data = filtered_data.groupby('Time Interval')['sum_of_amount'].sum().reset_index()

    # Define the order of time intervals for the pie chart
    time_interval_order = ['Midnight to 6AM', '6AM to 12PM', '12PM to 6PM', '6PM to Midnight']

    # Identify the index of the slice you want to pop out (e.g., the first slice)
    popout_slice_indices = [time_interval_order.index('Midnight to 6AM'), time_interval_order.index('6PM to Midnight')]

    # Set the size of the hole (0 to 1, where 0 is no hole and 1 is a full pie)
    hole_size = 0.4
    
    # Function to format amounts in '87.231k' or '87.231M' format
    def format_amount(amount):
        if amount >= 1_000_000:
            return f'{amount / 1_000_000:,.3f}M'
        elif amount >= 1_000:
            return f'{amount / 1_000:,.3f}k'
        return f'{amount:,}'
    
    # Create an interactive pie chart with specified category order and different pull values
    fig_pie = go.Figure(data=[
        go.Pie(
            labels=pie_data['Time Interval'],
            values=pie_data['sum_of_amount'],
            hole=hole_size,
            pull=[0 if i in popout_slice_indices else 0.05 for i in range(len(time_interval_order))],
            hovertemplate='<b>Time Of The Day:</b> %{label}<br><b>Amount:</b> %{customdata}<br><b>Percentage:</b> %{percent:.1%}<extra></extra>',
            customdata=[format_amount(val) for val in pie_data['sum_of_amount']]
        )
    ])
    

    fig_pie.update_layout(
        title='Usage Percentage In Different Parts Of The Day',
        height=400,
        width=600,
        showlegend=True,  # Hide legend for clarity
        legend=dict(
            font=dict(
                size=14  
            )
        )
    )
    
    # Update the layout to make the background transparent
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    
    col3, col4 = st.columns(2)
    with col3:
       st.plotly_chart(fig_bar_chart, use_container_width=True)

    with col4:
    #    st.plotly_chart(fig_line_chart, use_container_width=True)
       st.plotly_chart(fig_pie, use_container_width=True)
       
    st.markdown("---")  
       



    
## Live Graph  ##

    box_style_total_usage = "background-color: #6a040f; padding: 4px; border-radius: 4px; display: inline-block;"
    st.markdown(f"<div style='text-align: center; {box_style_total_usage}'><h4 style='color: white; font-size: 16px;'>Live Forecast Analytics:</h4></div>", unsafe_allow_html=True)

## Merging usage bar chart with forecast (last 1 day) and prediction (last 8 days) graphs ##

    # Create a combined figure
    fig_combined = go.Figure()

    # Add traces for the usage bar chart
    fig_combined.add_trace(go.Bar(
        x=last_3_days_data['Date and Hour of the Day'],
        y=last_3_days_data['sum_of_amount'],
        name='Usage Graph (Last 3 Days)',
        marker_color='#ba181b',
        showlegend=True
    ))

    # Add traces for the prediction line chart
    fig_combined.add_trace(go.Scatter(
        x=last_4_days_data['Date and Hour of the Day'],
        y=last_4_days_data['sum_of_amount'],
        name='Prediction Graph (Last 4 Days)',
        marker_color='blue',
        showlegend=True
    ))

    # Add traces for the forecast line chart
    fig_combined.add_trace(go.Scatter(
        x=last_1_day_data['Date and Hour of the Day'],
        y=last_1_day_data['sum_of_amount'],
        name='Forecast Graph (For Today)',
        marker_color='green',
        showlegend=True
    ))

    # Dropdown to select between 'Usage', 'Prediction', 'Forecast', or 'All'
    selected_chart = st.selectbox("", ['Usage + Prediction + Forecast Graph', 'Usage Graph', 'Prediction Graph', 'Forecast Graph'])

    # Initialize selected_fig outside the if statement 
    selected_fig = go.Figure()

    # Show only the selected chart
    if selected_chart == 'Usage + Prediction + Forecast Graph':
        selected_fig = fig_combined
    else:
        for trace in fig_combined.data:
            if trace.name is not None and selected_chart.lower() in trace.name.lower():
                selected_fig.add_trace(trace)

    selected_fig.update_layout(
        barmode='group',
        title=f"Showing : {selected_chart}",
        xaxis_title="Date and Hour",
        yaxis_title="Amount",
        height=350,
        width=650,
    )

    st.plotly_chart(selected_fig, use_container_width=True)



    
## KPIS for last 30 days ##

    # Filter data for the last 30 days
    last_30_days_data = df_Usage[df_Usage["my_date"] >= (datetime.today() - timedelta(days=30))]
    
    # Helper function to format amounts
    def format_amount(amount):
        if amount.is_integer():
            return f"৳ {amount:,.0f}"
        else:
            return f"৳ {amount:,.2f}"
        
    # Calculate and format total usage in the last 30 days
    total_usage_last_30_days = last_30_days_data['sum_of_amount'].sum()
    total_usage_last_30_days_formatted = format_amount(total_usage_last_30_days)


    # Highest Usage Day in the last 30 days
    grouped_data = last_30_days_data.groupby('my_date')['sum_of_amount'].sum()
    highest_usage_day = grouped_data.idxmax()
    highest_usage_day_amount = grouped_data.max()
    highest_usage_day_amount_formatted = format_amount(highest_usage_day_amount)
    highest_usage_day_str = highest_usage_day.strftime("%B %d, %Y")
    
    
    # Lowest Usage Day in the last 30 days
    grouped_data = last_30_days_data.groupby('my_date')['sum_of_amount'].sum()
    lowest_usage_day = grouped_data.idxmin()
    lowest_usage_day_amount = grouped_data.min()
    lowest_usage_day_amount_formatted = format_amount(lowest_usage_day_amount)
    lowest_usage_day_str = lowest_usage_day.strftime("%B %d, %Y")
    
    
    # Highest Usage Hour in the last 30 days
    grouped_data = last_30_days_data.groupby(['my_date', 'my_hour'])['sum_of_amount'].sum()
    highest_usage_hour = grouped_data.idxmax()
    highest_usage_hour_amount = grouped_data.max()
    highest_usage_hour_amount_formatted = format_amount(highest_usage_hour_amount)

    # Determine AM/PM for the highest usage hour
    am_pm = "AM" if highest_usage_hour[1] < 12 else "PM"
    formatted_hour = f"{highest_usage_hour[0].strftime('%b %d, %Y')}, {(highest_usage_hour[1] % 12) or 12} {am_pm}"

    # Display the highest usage hour in the desired format
    highest_usage_hour_str = f"{formatted_hour}"



    # Lowest Usage Hour in the last 30 days
    grouped_data = last_30_days_data.groupby(['my_date', 'my_hour'])['sum_of_amount'].sum()
    lowest_usage_hour = grouped_data.idxmin()
    lowest_usage_hour_amount = grouped_data.min()
    lowest_usage_hour_amount_formatted = format_amount(lowest_usage_hour_amount)

    # Determine AM/PM for the lowest usage hour
    am_pm = "AM" if lowest_usage_hour[1] < 12 else "PM"
    formatted_hour = f"{lowest_usage_hour[0].strftime('%b %d, %Y')}, {(lowest_usage_hour[1] % 12) or 12} {am_pm}"

    # Display the lowest usage hour in the desired format
    lowest_usage_hour_str = f"{formatted_hour}" 
   
   
   
   
       
    
    ## Display the KPIS Title
    
    # Define the color and border properties for the box
    box_style_total_usage = "background-color: #6a040f; padding: 10px; border-radius: 4px; width: 100%;"
    # Display the KPIS Title in a colored box
    st.sidebar.markdown(f"<div style='text-align: center; {box_style_total_usage}'><h4 style='color: white; font-size: 16px;'>Last 30 Days Usage Summary</h4></div>", unsafe_allow_html=True)
   
    st.sidebar.markdown("---")
    
    
    # Define the box styles for each KPI 
    box_style_total_usage = "background-color: #c75146; padding: 2px; border-radius: 3px; width: 100%;"
    
    #box_style_highest_day_usage= "background-color: #fb8500; padding: 2px; border-radius: 3px; width: 85%;"
    #box_style_lowest_day_usage= "background-color: #fb8500; padding: 2px; border-radius: 3px; width: 80%;"
    
    #box_style_highest_hour_usage= "background-color: #D28579; padding: 2px; border-radius: 3px; width: 75%;"
    #box_style_lowest_hour_usage= "background-color: #D28579; padding: 2px; border-radius: 3px; width: 70%;"



    # Total Usage Amount Display
    st.sidebar.markdown(f"<div style='text-align: center; {box_style_total_usage}'><h7 style='color: white; font-size: 12px;'><strong>Total Usage Amount (In Last 30 Days):</strong></h7></div>", unsafe_allow_html=True)

    # Display the total usage amount with a centered box
    st.sidebar.markdown(f"""
        <div style='text-align: center;'>
            <h3>{total_usage_last_30_days_formatted}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    
    #highest day
    box_style_outer = """background-color: #F5E4E0; border: 3px solid #6a040f; padding: 3px; border-radius: 3px; width: 100%; color: black; box-sizing: border-box; text-align: center; margin-bottom: 15px; display: flex; flex-direction: column; align-items: center; justify-content: center;"""
    box_style_title = """background-color: #f25c54; padding: 3px; border-radius: 3px; width: 85%; color: black; box-sizing: border-box; text-align: center;"""


    # Display the lowest usage hour with a title box inside the main box
    st.sidebar.markdown(f"""
    <div style='{box_style_outer}'>
        <div style='{box_style_title}'>
            <h7 style='color: white; font-size: 12px;'><strong>Highest Daily Usage (In Last 30 Days):</strong></h7>
        </div>
        <p style='text-align: center;'>{highest_usage_day_str}<br><strong>{highest_usage_day_amount_formatted}</strong></p>
    </div>
    """, unsafe_allow_html=True)
        
    
    #lowest day
    box_style_outer = """background-color: #F5E4E0; border: 3px solid #6a040f; padding: 3px; border-radius: 3px; width: 100%; color: black; box-sizing: border-box; text-align: center; margin-bottom: 15px; display: flex; flex-direction: column; align-items: center; justify-content: center;"""
    box_style_title = """background-color: #f25c54; padding: 3px; border-radius: 3px; width: 85%; color: black; box-sizing: border-box; text-align: center;"""


    # Display the lowest usage hour with a title box inside the main box
    st.sidebar.markdown(f"""
    <div style='{box_style_outer}'>
        <div style='{box_style_title}'>
            <h7 style='color: white; font-size: 12px;'><strong>Lowest Daily Usage (In Last 30 Days):</strong></h7>
        </div>
        <p style='text-align: center;'>{lowest_usage_day_str}<br><strong>{lowest_usage_day_amount_formatted}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    
    #highest hour
    box_style_outer = """background-color: #F5E4E0; border: 3px solid #6a040f; padding: 3px; border-radius: 3px; width: 100%; color: black; box-sizing: border-box; text-align: center; margin-bottom: 15px; display: flex; flex-direction: column; align-items: center; justify-content: center;"""
    box_style_title = """background-color: #D28579; padding: 3px; border-radius: 3px; width: 85%; color: black; box-sizing: border-box; text-align: center;"""

    # Display the lowest usage hour with a title box inside the main box
    st.sidebar.markdown(f"""
    <div style='{box_style_outer}'>
        <div style='{box_style_title}'>
            <h7 style='text-align: center; color: white; font-size: 12px;'><strong>Highest Hourly Usage (In Last 30 Days):</strong></h7>
        </div>
        <p style='text-align: center;'>{highest_usage_hour_str}<br><strong>{highest_usage_hour_amount_formatted}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    
    #lowest hour
    box_style_outer = """background-color: #F5E4E0; border: 3px solid #6a040f; padding: 3px; border-radius: 3px; width: 100%; color: black; box-sizing: border-box; text-align: center; margin-bottom: 15px; display: flex; flex-direction: column; align-items: center; justify-content: center;"""
    box_style_title = """background-color: #D28579; padding: 3px; border-radius: 3px; width: 85%; color: black; box-sizing: border-box; text-align: center;"""

    # Display the lowest usage hour with a title box inside the main box
    st.sidebar.markdown(f"""
    <div style='{box_style_outer}'>
        <div style='{box_style_title}'>
            <h7 style='text-align: center; color: white; font-size: 12px;'><strong>Lowest Hourly Usage (In Last 30 Days):</strong></h7>
        </div>
        <p style='text-align: center;'>{lowest_usage_hour_str}<br><strong>{lowest_usage_hour_amount_formatted}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    
   


    
    

 
   
    
    
    

  
    
    

  
    
    
    

    
   





 
        
    


    
    


