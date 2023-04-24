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

# App Setup
st.markdown("<h1 style='text-align:center;'>LinkedIn Data Insight App</h1>", unsafe_allow_html=True)



uploaded_file = st.file_uploader("Upload Your LinkedIn Conneection CSV File", type="csv")
# Check if a file was uploaded

def year_plot(dataframe):
    yearly = dataframe.groupby(dataframe.index.year).count()
    yearFig = px.bar(yearly, yearly.index, 'First Name', title='<b>Yearly Connections<b>',
                     text_auto=True, labels={'First Name': 'Connection Count', 'Connected On': ''})
    yearFig.update_yaxes(showticklabels=False)
    yearFig.update_traces(textposition='outside')
    return yearFig

def month_plot(dataframe):
    monthly = dataframe.groupby(dataframe.index.month).count()
    monthlyFig = px.line(monthly, monthly.index, ['First Name', 'Company'])
    return monthlyFig

if uploaded_file is not None:
    # Convert the file contents to a DataFrame using pandas
    df = pd.read_csv(uploaded_file)
    df['Connected On'] = pd.to_datetime(df['Connected On'], format="%d %b %Y")
    df1= df.copy()
    df1['Connected On'] = pd.to_datetime(df['Connected On'], format="%d %b %Y").dt.date
    df.set_index('Connected On', inplace=True)

    # Process the DataFrame as needed
    # For example, you can display it, perform computations, or save it to disk
    # Here, we display the DataFrame using Streamlit's built-in DataFrame display function
    st.write(df1)

    # Display a message to indicate successful file upload
    st.success("CSV file uploaded successfully!")
    
    month_order = [1,2,3,4,5,6,7,8,9,10,11,12]
    month_short = [ 'Jan','Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    
    f"There are a total of {df.shape[0]} connections"
    
    cola, colb = st.columns([1, 9])
    
    with cola:
        year = st.number_input("Select a year", min_value=1900, max_value=2100, step=1)
        col11, col22 = st.columns([1.2,1], gap="small")
        
        with col11:
            filter_button = st.button('Filter')
        with col22:
            reset_button = st.button('Reset')
        # Ask the user to select a year
        
        if filter_button:
            filtered = df[df.index.year == year]
            if len(filtered) == 0:
                st.write(f"No connection for year {year}")
                filtered = df
        elif reset_button:
            filtered = df
        else:
            filtered = df
        
    # Split the page into two column
    col1, col2= st.columns([5, 5], gap='medium')
    
    
    yearly = df.groupby(df.index.year).count()
    yearFig = px.bar(yearly, yearly.index, 'First Name', title='<b>Yearly Connections<b>',
                     text_auto=True, labels={'First Name': 'Connection Count', 'Connected On': ''})
    yearFig.update_yaxes(showticklabels=False)
    yearFig.update_traces(textposition='outside')
    with col1:
        st.plotly_chart(yearFig, use_container_width=True)
        
    
    monthly = filtered.groupby(filtered.index.month).count()
    monthlyFig = px.line(monthly, monthly.index, 'First Name', title="<b>Monthly Connections<b>",
                         labels={'First Name': 'Connection Count', 'Connected On': ''}, text=monthly['First Name'])
    monthlyFig.update_layout(xaxis = dict(
        tickvals = month_order,
        ticktext = month_short
    ))
    monthlyFig.update_traces(textposition='top center')
    monthlyFig.update_yaxes(showticklabels=False)
    with col2:
        st.plotly_chart(monthlyFig, use_container_width=True)
        
        
    daily = filtered.groupby(filtered.index.day_name()).count().reindex(days)
    dailyFig = px.line(daily, daily.index, 'First Name', text=daily['First Name'],
                       title='<b>Connections by Day of the Week<b>', 
                       labels={'Connected On': '', 'First Name': 'Connections Count'})
    dailyFig.update_yaxes(showticklabels=False)
    dailyFig.update_traces(textposition='top center')
    with col1:
        st.plotly_chart(dailyFig, use_container_width=True)
    
    def top_plot(col, title):
        top_company = filtered[col].value_counts().to_frame(name='Count')[:5].sort_values(by='Count')
        topFig = px.bar(top_company, 'Count', top_company.index, title=title, labels={'index':''},
                        text_auto=True)
        topFig.update_traces(textposition='outside', cliponaxis=False)
        topFig.update_xaxes(showticklabels=False)
        return topFig
    
    topCom = top_plot('Company', '<b>Top 5 Connect Company<b>')
    topPos = top_plot('Position', '<b>Top 5 Connect Position<b>')
    with col2:
        st.plotly_chart(topCom, use_container_width=True)
    with col1:
        st.plotly_chart(topPos, use_container_width=True)
    
else:
    # Display a message if no file was uploaded
    st.info("Please upload a CSV file.")