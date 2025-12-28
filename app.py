import pandas as pd
import numpy as np
import streamlit as st
import plotly_express as px
import streamlit as st

df = pd.read_csv("future_jobs_dataset.csv", index_col="job_id")
df.columns = df.columns.str.strip().str.title()

# cleaning the data
df['Job_Title'] = df['Job_Title'].replace(['Quantum','Renewable','Smart'], '', regex=True)
df['Posting_Date'] = pd.to_datetime(df['Posting_Date'], errors='coerce').dt.date
df['Salary_Usd'] = pd.to_numeric(df['Salary_Usd'], errors='coerce')
st.set_page_config(layout="wide")

sidebar = st.sidebar
sidebar.header("🔍 Filtering section")
page = sidebar.radio("CLICK ON", ["HOME", "DASHBOARD"])

if page == "HOME":
    st.markdown("""
        <h1 style="text-align: center; color: #2E86C1;">🚀 Future Jobs Explorer Dashboard</h1>
        """, unsafe_allow_html=True)
    st.markdown("""
    ## 📊 About the Dataset
    
    The **Future Jobs Dataset** provides a structured view of emerging job opportunities across different industries, locations, and work arrangements. It is designed to help users         understand how the job market is evolving, which roles are gaining demand, and what skills are becoming increasingly important for the future workforce.
    Each row in the dataset represents a **single job posting**, identified by a unique job ID. The dataset combines information on job roles, industries, salaries, locations,              required skills, and posting dates to support meaningful data exploration and analysis.
    
    ### 🔍 Key Features of the Dataset
    - **Job Titles**: Describes the role being advertised. Titles are cleaned to remove repeated future-focused keywords for consistency.
    - **Industry**: Indicates the sector creating each job opportunity, helping identify industries with the highest demand.
    - **Location**: Shows where the job is based, allowing comparison of opportunities across regions.
    - **Posting Date** : Records when each job was posted, making it possible to analyze trends over time.
    - **Salary (USD)**: Represents estimated annual salaries, useful for comparing compensation levels across roles.
    - **Skills Required**: Lists the core skills needed for each role, helping highlight the most in-demand skills.
    - **Remote Option**: Indicates whether a role can be performed remotely, reflecting workplace flexibility.
    
    ### 🎯 Purpose of the Dataset
    This dataset supports:
    - Job seekers exploring high-demand career paths  
    - Students and graduates planning skill development  
    - Analysts studying future workforce trends  
    - Educators and policymakers assessing labor market needs  
    
    ### ❓ Key Questions Explored
    Using this dataset, the dashboard answers questions such as:
    - 🚀Which job roles are growing the fastest?
    - 🛠️What skills are most frequently required?
    - 🏭Which industries are creating the most job opportunities?
    - ⏳How are job postings changing over time?
    - 📈How common are remote work opportunities?
    - ❓What salary ranges are typical for future-focused roles?
    - 🌍Average salary by location
    
    Overall, this dataset provides a **data-driven snapshot of the future job market**, helping users make informed decisions about careers, skills, and employment trends.
    """)
    st.info("👈 **Switch to the DASHBOARD tab** in the sidebar to start exploring trends, filter jobs, and uncover insights!") 
        
if page == "DASHBOARD":
    filtered_df = df.copy()
    
    job_titles = sorted(df['Job_Title'].dropna().unique())
    selected_job = sidebar.selectbox("**Job Title**", options=job_titles, index = None)
    # job filter
    if selected_job:
        filtered_df = filtered_df[
            filtered_df['Job_Title'].str.strip().str.lower() == selected_job.strip().lower()
        ]
    

    locations = sorted(df['Location'].dropna().unique())
    selected_location = sidebar.selectbox("**Location**", options=locations, index = None)
     # Location filter
    if selected_location:
        filtered_df = filtered_df[
            filtered_df['Location'].str.strip().str.lower() == selected_location.strip().lower()
        ]


    # date
    date = sidebar.checkbox("📅Click to Apply Date Filter", value=False)
    if date:
        date_range = sidebar.date_input(
            "**Please Select date range**",
            value=(df['Posting_Date'].min(), df['Posting_Date'].max()),
            min_value=df['Posting_Date'].min(),   
            max_value=df['Posting_Date'].max(), 
            key="date_range_picker"
        )
        # filter date
        if len(date_range) == 2:
            start_date, end_date = sorted(date_range)  
            filtered_df = filtered_df[
                filtered_df['Posting_Date'].between(start_date, end_date)
            ]
 # salary
    min_sal = int(df['Salary_Usd'].min() / 1000)
    max_sal = int(df['Salary_Usd'].max() / 1000)
    salary_range = sidebar.slider(
        "**Salary Range (USD)**",
        min_value=min_sal,
        max_value=max_sal,
        value=(min_sal, max_sal),
        format="$%dK"
    )
     # Salary filter
    filtered_df = filtered_df[
        (filtered_df['Salary_Usd'] >= salary_range[0]*1000) &
        (filtered_df['Salary_Usd'] <= salary_range[1]*1000)
    ]

    #  Metrics 
    metric_df = filtered_df.copy()
    total_jobs = len(metric_df)
    average_salary = metric_df['Salary_Usd'].mean()
    
    # fastest growing role
    fastest_growing = metric_df['Job_Title'].value_counts().idxmax()
    
    remote_count = metric_df['Remote_Option'].str.lower().eq('yes').sum()
    remote_pct = (remote_count / total_jobs) * 100
    st.title("📈 Dashboard Metrics")
    col1, col2, col3, col4 = st.columns([1.2, 1.6, 1.6, 1.4])
    col1.metric(label="**💼 Total Jobs**", value=f"{total_jobs:,}", border = True)
    col2.metric( label="**💰 Average Salary**", value=f"${average_salary/1000:.2f}k", border=True)
    col3.metric(label="**🚀 Fastest Growing Role**", value=fastest_growing, border = True)
    col4.metric(label="**🏠 Remote Jobs**", value=f"{remote_count:,} ({remote_pct:.1f}%)", border = True)

    insight_text = f"""
    The dashboard shows a snapshot of the current job market. There are **{total_jobs:,} active postings**, 
    with an **average salary of ${average_salary:,.2f}**. 
    The **fastest-growing role is {fastest_growing}**, highlighting strong demand in that area. 
    Additionally, **{remote_count:,} positions ({remote_pct:.1f}%)** shows the amount of remote work, showing the level of flexibility in these opportunities. 
    Together, these metrics give a clear view of market demand, compensation trends, and work flexibility.
    """
    st.markdown(insight_text)
    col1, col2, col3, col4= st.columns([1,1,1,1])
    with col1:
        st.image("https://www.shutterstock.com/image-photo/salary-increase-concept-businessman-260nw-2218122365.jpg", caption = "", width = 200)
    with col2:
        st.image("https://as2.ftcdn.net/v2/jpg/03/07/47/79/1000_F_307477935_TgRybpcXe0lyyhLYXs898EDNFbYGlti5.jpg", caption = "", width = 200)
    with col3: 
        st.image("https://ergos.com/wp-content/uploads/remote-work-resized.png", caption = "", width = 200)
    with col4:
        st.image("https://th.bing.com/th/id/OIP.6dXIWiyBSKIxe5bUixMPrwHaE8?w=243&h=180&c=7&r=0&o=7&cb=ucfimg2&dpr=1.5&pid=1.7&rm=3&ucfimg=1", caption = "",  
                 width = 200)
            
    st.markdown("### 📋 Filtered Job Listings")
    st.dataframe(filtered_df)




    # question 1
    # Which job roles are expected to grow the fastest in the future?
    st.markdown("### 🚀 Top Fastest Growing Job Roles")
    role_counts = filtered_df['Job_Title'].value_counts().reset_index()
    role_counts.columns = ['Job_Title', 'Number_of_Postings']
    top_roles = role_counts.head(10)
    st.dataframe(
    top_roles.style.background_gradient(cmap='Blues'),
        use_container_width=True,
        hide_index=True
    )
    max_role = top_roles.iloc[0]
    st.success(f""" The role **{max_role['Job_Title']}** leads with **{max_role['Number_of_Postings']:,} postings**, 
    indicating the strongest current demand and likely fastest growth in the near future.
    """)

    fig = px.bar(
        top_roles,
        x='Number_of_Postings',
        y='Job_Title',
        orientation='h',
        text='Number_of_Postings',
        color='Number_of_Postings',
        color_continuous_scale='Plasma',
        title="Top 10 Job Roles by Demand"
    )
    
    fig.update_layout(
        height=450,
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title="Number of Job Postings",
        yaxis_title="Job Title"
    )
    fig.update_traces(textposition='outside')
    
    st.plotly_chart(fig, use_container_width=True)
    
    #Question 2 What skills are most frequently required for future jobs?
    st.markdown("### 🛠️ Most In Demand Skills")
    all_skills = (filtered_df['Skills_Required'].dropna().str.split(',').explode().str.strip())

    skill_counts = all_skills.value_counts().reset_index()
    skill_counts.columns = ['Skill', 'Number_of_Jobs_Requiring']
    top_skills = skill_counts.head(10)
    st.dataframe(
        top_skills.style.background_gradient(cmap='Oranges', subset=['Number_of_Jobs_Requiring']),
        use_container_width=True,
        hide_index=True
    )
    top_skill = top_skills.iloc[0]
    st.info(f"""**{top_skill['Skill']}** is the most in demand skill, 
    required in **{top_skill['Number_of_Jobs_Requiring']:,} job postings**
    a must-have for anyone preparing for future roles!
    """)
    fig_skills = px.bar(
        top_skills,
        x='Number_of_Jobs_Requiring',
        y='Skill',
        orientation='h',
        text='Number_of_Jobs_Requiring',
        color='Number_of_Jobs_Requiring',
        color_continuous_scale='Oranges',     
        title="Top Most Required Skills"
    )

    fig_skills.update_layout(
        height=500,
        yaxis={'categoryorder': 'total ascending'},  
        xaxis_title="Number of Job Postings Requiring Skill",
        yaxis_title="Skill"
    )
    fig_skills.update_traces(textposition='outside')

    st.plotly_chart(fig_skills, use_container_width=True)


    # Question 3 Which industries will create the most future job opportunities?
    st.markdown("### 🏭 Industries with the Most Job Opportunities")
    industry_counts = filtered_df['Industry'].value_counts().reset_index()
    industry_counts.columns = ['Industry', 'Number_of_Postings']
    top_industries = industry_counts.head(10)
    st.dataframe(
        top_industries.style.background_gradient(cmap='Greens', subset=['Number_of_Postings']),
        use_container_width=True,
        hide_index=True
    )
    top_industry = top_industries.iloc[0]
    st.success(f"""The **{top_industry['Industry']}** industry leads with **{top_industry['Number_of_Postings']:,} job postings**, 
    making it the sector creating the most opportunities right now and likely into the future.
    """)
    fig_industry = px.bar(
        top_industries,
        x='Number_of_Postings',
        y='Industry',
        orientation='h',
        text='Number_of_Postings',
        color='Number_of_Postings',
        color_continuous_scale='Greens', 
        title="Top Industries by Job Postings"
    )

    fig_industry.update_layout(
        height=500,
        yaxis={'categoryorder': 'total ascending'}, 
        showlegend=False,
        xaxis_title="Number of Job Postings",
        yaxis_title="Industry"
    )
    fig_industry.update_traces(textposition='outside')

    st.plotly_chart(fig_industry, use_container_width=True)

   # Question 4: How are job postings trending over time?
    st.markdown("### 📈 Job Posting Trends Over Time")
    trend_df = filtered_df.copy()
    trend_df['Posting_Date'] = pd.to_datetime(trend_df['Posting_Date'])
    
    monthly_postings = (
        trend_df.groupby(trend_df['Posting_Date'].dt.to_period('M'))
        .size()
        .reset_index()
        .rename(columns={'Posting_Date': 'Month', 0: 'Number_of_Postings'})
    )
    
    monthly_postings['Month'] = monthly_postings['Month'].dt.to_timestamp()
    monthly_postings = monthly_postings.sort_values('Month')
    
    
    growth_pct = 0
    
    # Line chart
    fig_trend = px.line(
        monthly_postings,
        x='Month',
        y='Number_of_Postings',
        markers=True,
        title="Monthly Job Posting Trends",
        labels={
            'Month': 'Posting Month',
            'Number_of_Postings': 'Number of New Postings'
        }
    )
    
    fig_trend.update_traces(
        line=dict(color='#FF8C00', width=4),
        marker=dict(color='#FFA500', size=12)
    )
    
    fig_trend.update_layout(
        height=500,
        xaxis_title="Month",
        yaxis_title="Number of Job Postings",
        hovermode='x unified'
    )
    
    if len(monthly_postings) > 1:
        first = monthly_postings['Number_of_Postings'].iloc[0]
        last = monthly_postings['Number_of_Postings'].iloc[-1]
        growth_pct = ((last - first) / first * 100) if first > 0 else 0
    
        fig_trend.add_annotation(
            x=0.02, y=0.95,
            xref="paper", yref="paper",
            text=f"Overall Growth: <b>{growth_pct:+.1f}%</b>",
            showarrow=False,
            font_size=16,
            bgcolor="rgba(0,166,118,0.8)",
            font_color="white"
        )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    if len(monthly_postings) > 0:
        latest_month = monthly_postings['Month'].iloc[-1].strftime('%B %Y')
        latest_count = monthly_postings['Number_of_Postings'].iloc[-1]

        if growth_pct > 10:
            message = "The market is growing strongly!"
        elif growth_pct > 0:
            message = "Postings are stable with slight growth."
        else:
            message = "The market is currently stagnant."

    st.success(
        f"In **{latest_month}**, there were **{latest_count:,} new job postings**. {message}"
    )


    # Question 5 Average salary by location
    st.markdown("### 🌍 Salary Distribution by Location")
    
    # Calculate average salary by location
    location_salary = (filtered_df.groupby('Location')['Salary_Usd'].mean().reset_index().dropna().sort_values('Salary_Usd', ascending=False))
    
    top_locations = location_salary.head(10)
    
    top_locations['Salary_Formatted'] = top_locations['Salary_Usd'].apply(lambda x: f"${x:,.0f}")
    st.dataframe(
    top_locations[['Location', 'Salary_Usd', 'Salary_Formatted']].style.background_gradient(cmap='Purples', subset=['Salary_Usd']),use_container_width=True,hide_index=True)
    top_location = top_locations.iloc[0]
    st.success(
        f"In **{top_location['Location']}**, the highest average salary is offered,"
        f"with an average pay of **${top_location['Salary_Usd']:,.0f}**. "
        "This suggests that location plays a significant role in salary levels for future job roles."
    )
    
    # Bar chart
    fig_location_salary = px.bar(
        top_locations,
        x='Salary_Usd',  
        y='Location',
        orientation='h',
        text=top_locations['Salary_Formatted'],  
        color='Salary_Usd',
        color_continuous_scale='Purples',
        title="Top Locations by Average Salary"
    )
    
    fig_location_salary.update_layout(
        height=500,
        xaxis_title="Average Salary (USD)",
        yaxis_title="Location",
        yaxis={'categoryorder': 'total ascending'}
    )
    
    fig_location_salary.update_traces(textposition='outside')
    fig_location_salary.update_xaxes(tickprefix="$", separatethousands=True)
    st.plotly_chart(fig_location_salary, use_container_width=True)
    
    
    
    












    
