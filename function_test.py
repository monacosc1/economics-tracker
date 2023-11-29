import os
import pandas as pd
import folium
from folium.plugins import HeatMap
import streamlit as st

def read_data():
    data_folder = "Datas/Raw Datas"
    zearn_df = pd.read_csv(os.path.join(data_folder, 'Zearn - County - Weekly.csv'))
    unemep_df = pd.read_csv(os.path.join(data_folder, 'UI Claims - County - Weekly.csv'))
    job_df = pd.read_csv(os.path.join(data_folder, 'Job Postings - County - Weekly.csv'))
    emp_df = pd.read_csv(os.path.join(data_folder, 'Employment - County - Weekly.csv'))
    spend_df = pd.read_csv(os.path.join(data_folder, 'Affinity - County - Daily.csv'))
    
    loc = pd.read_csv('Datas/us_county_latlng.csv')
    loc = loc.rename(columns={'fips_code':'countyfips'})
    # return all of the dataframes.
    return zearn_df, unemep_df, job_df, emp_df, spend_df, loc

def create_date_index(df):
    # Rename the 'day' column to 'day_endofweek'
    df = df.rename(columns={'day_endofweek': 'day'})
    
    # Create a new datetime column by combining 'year', 'month', and 'day_endofweek'
    df['date_index'] = pd.to_datetime(df[['year', 'month', 'day']])

    # Set the 'date_index' column as the index
    df.set_index('date_index', inplace=True)
    
    # drop index column
    df = df.drop(['index'], axis=1)
    
    return df

def prepare_for_chart(df, colnames_to_cast, loc, drop_cols=[]):
    empty_columns = df.columns[df.eq('.').all()]
    empty_columns = list(empty_columns)
    empty_columns.extend(drop_cols)

    for col in colnames_to_cast:
        if col != 'name' and col in df.columns:
            if df[col].dtype != int:
                # Check if the column is of numeric type (float)
                if df[col].dtype == float:
                    df[col] = df[col].replace('.', '0').astype(float)
                elif df[col].dtype == object:
                    df[col] = df[col].str.replace('.', '0')
                    df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.reset_index()
    df = pd.merge(df, loc, on='countyfips')

    df = create_date_index(df)

    # Only keep 'name' once in the resulting DataFrame
    if 'name' in colnames_to_cast:
        colnames_to_cast.remove('name')

    df = df[['name'] + colnames_to_cast]
    
    return df


def prepare_and_save_chart_data(zearn_df,unemep_df, job_df, emp_df, spend_df,loc):
    # Prepare data for charts
    zearn_df_chart = prepare_for_chart(zearn_df, ['name', 'engagement', 'badges', 'break_engagement', 'break_badges'],loc)
    unemep_df_chart = prepare_for_chart(unemep_df, ['name', 'initclaims_rate_regular'],loc)
    job_df_chart = prepare_for_chart(job_df, ['name', 'bg_posts', 'bg_posts_jzgrp12', 'bg_posts_jzgrp345'],loc)
    emp_df_chart = prepare_for_chart(emp_df, ['name', 'emp_incq1', 'emp', 'emp_incq2', 'emp_incq3', 'emp_incmiddle', 'emp_incbelowmed'],loc)
    spend_df_chart = prepare_for_chart(spend_df, ['name', 'spend_all'],loc)

    # Create a folder to save chart data if it doesn't exist
    if not os.path.exists('./Datas/Chart Datas'):
        os.makedirs('./Datas/Chart Datas')

    # Save the prepared data to CSV files
    zearn_df_chart.to_csv("./Datas/Chart Datas/zearn_df_chart.csv")
    unemep_df_chart.to_csv("./Datas/Chart Datas/unemep_df_chart.csv")
    job_df_chart.to_csv("./Datas/Chart Datas/job_df_chart.csv")
    emp_df_chart.to_csv("./Datas/Chart Datas/emp_df_chart.csv")
    spend_df_chart.to_csv("./Datas/Chart Datas/spend_df_chart.csv")

    # Print information to the Streamlit app
    st.write("Chart data prepared and saved successfully!")

zearn_df, unemep_df, job_df, emp_df, spend_df, loc = read_data()

prepare_and_save_chart_data(zearn_df,unemep_df, job_df, emp_df, spend_df, loc)