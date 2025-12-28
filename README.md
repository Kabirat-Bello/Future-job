# Future Jobs Dashboard (Streamlit App)

## Description
The **Future Jobs Dashboard** is an interactive Streamlit application that analyzes and visualizes trends in future job roles. Users can explore job demand, salary distribution, and posting trends using filters, metrics, and interactive charts.

This is a personal data analysis and visualization portfolio project built with Python and Streamlit.

## Motivation
To understand evolving job market trends, especially in future-oriented and technology-driven roles, while practicing:
- Data cleaning
- Exploratory data analysis
- Building interactive dashboards with Streamlit

## Features
- Interactive job title and category selection
- Date range filtering
- Salary analysis with proper formatting
- Key metrics (total jobs, average salary, growth insights)
- Interactive charts using Plotly
- Clean and user-friendly interface

## Technologies Used
- Python
- Streamlit
- Pandas
- Plotly Express

## Dataset Information
The dataset was downloaded from Kaggle and contains information about future job roles, including:
- Job Title
- Job Category
- Salary (USD)
- Posting Date
- Industry
- Location

**File:** `future_jobs_dataset.csv`

## Installation
```bash
git clone https://github.com/Kabirat-Bello/Future-job.git
cd Future-job
pip install -r requirements.txt
streamlit run app.py
├── app.py                     # Main Streamlit app
├── future_jobs_dataset.csv    # Dataset
├── requirements.txt           # Dependencies
└── README.md                  # This file

LimitationsDataset is static (no real-time data)
Limited to the size and scope of the Kaggle dataset
Insights may not reflect the current global job market

Future ImprovementsAdd more filters (location, industry)
Improve the UI design
Deploy the app online (e.g., Streamlit Community Cloud)
Add job growth predictions

AuthorKabirat Omolola
GitHub: Kabirat-BelloAcknowledgementsKaggle for providing the dataset
Streamlit and the open-source Python community

Thank you for viewing my project! 


