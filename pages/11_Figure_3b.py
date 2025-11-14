import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go
import plotly.express as px

# The actual page content is executed here by Streamlit
st.title("Path 2: Figure 3b")
st.markdown("---")


# Retrieve shared data from the Home page's session state
if 'student_data' not in st.session_state or st.session_state['student_data']['st11_df'].empty:
    st.warning("Data not loaded. Please ensure the main Home Page ran successfully and the data files exist.")
else:
    df = st.session_state['student_data']['st11_df']

    # --- Student Introductory Section ---
    st.header("1. Introduction and Project Goal")
    st.markdown("""
        **Data Description:** This dataset contains pageview data for five regions from 2017-2023 by capita.
                
        **Interaction:** Use the selection box below to select specific regions to view pageview data based on country and year.
    """)
    st.markdown("---")
    
    # prepare dataframe
    df['pageviews_per_capita'] = df['total_pageviews']/df['population']
    df['pageviews_per_capita_log'] = [math.log10(item) for item in df['pageviews_per_capita']]
    
    df_means = pd.DataFrame(df.groupby('region')['pageviews_per_capita'].mean())

    # --- Analysis Content ---
    st.header("2. Pageviews per Capita by Region")

    selected_region = st.multiselect(
        "Filter by Region:",
        df['region'].unique().tolist(),
        default=df['region'].unique().tolist()
    )

    df_plot = df[df['region'].isin(selected_region)].dropna(subset=['pageviews_per_capita_log', 'region'])
    df_means_plot = (df[df['region'].isin(selected_region)].groupby('region')['pageviews_per_capita_log'].mean().reset_index())

    # Create initial figure
    fig = px.strip(
        df_plot,
        x="pageviews_per_capita_log",
        y="region",
        labels={
        "pageviews_per_capita_log": "Pageviews per Capita (Log base 10)",
        "region": "Region"},
        color='region',
        hover_data=['country_year'],
        title=f'Pageviews per Capita (Regions: {", ".join(selected_region)})',
    )

    fig.update_traces(jitter=1)

    # Add the second strip plot trace (e.g., "Group 2")
    fig.add_trace(go.Scatter(
        x=df_means_plot['pageviews_per_capita_log'],
        y=df_means_plot['region'],
        mode='markers',
        name='Means',
        marker=dict(color='orange', size=14, opacity=1, symbol='triangle-up')))

    st.plotly_chart(fig, use_container_width=True)