"""
@Created on: Monday, April 24, 2023, 9:54:22 AM WAT

@Author: TelRich Data

"""
# Libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Setting page size and title
st.set_page_config(layout="wide", page_title='LinkedIn Data Insight App', page_icon='110.png' ) 

uploaded_file = st.file_uploader("Upload Your LinkedIn Conneection CSV File", type="csv")
# Check if a file was uploaded
if uploaded_file is not None:
    # Convert the file contents to a DataFrame using pandas
    df = pd.read_csv(uploaded_file)
    df['Connected On'] = pd.to_datetime(df['Connected On'], format="%d %b %Y")
    df1= df.copy()
    df1['Connected On'] = pd.to_datetime(df['Connected On'], format="%d %b %Y").dt.date


    # Process the DataFrame as needed
    # For example, you can display it, perform computations, or save it to disk
    # Here, we display the DataFrame using Streamlit's built-in DataFrame display function
    st.write(df1)

    # Display a message to indicate successful file upload
    st.success("CSV file uploaded successfully!")
    
    f"There are a total of {df.shape[0]} connections"
    
    # Ask the user to select a year
    year = st.number_input("Select a year", min_value=1900, max_value=2100, step=1)

    # Split the page into two column
    col1, col2= st.columns([5, 5], gap='small')
    
    # Display the selected year
    # year_select = st.write("Selected year:", int(year))
    
    
    df.set_index('Connected On', inplace=True)
    yearly = df.groupby(df.index.year).count()
    yearFig = px.bar(yearly, yearly.index, 'First Name', title='<b>Yearly Connections<b>',
                     text_auto=True, labels={'First Name': 'Connection Count', 'Connected On': ''})
    yearFig.update_yaxes(showticklabels=False)
    yearFig.update_traces(textposition='outside')
    with col1:
        st.plotly_chart(yearFig, use_container_width=True)
    
    monthly = df.groupby(df.index.month).count()
    monthlyFig = px.line(monthly, monthly.index, ['First Name', 'Company'])
    with col2:
        st.plotly_chart(monthlyFig, use_container_width=True)
        
    daily = df.groupby(df.index.day).count()
    dailyFig = px.line(daily, daily.index, 'First Name')
    
    st.plotly_chart(dailyFig)
    
else:
    # Display a message if no file was uploaded
    st.info("Please upload a CSV file.")