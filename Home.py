import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Financial Insight Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("<h1 style='text-align: center;'>Financial Insights Dashboard: 📊 Loan Performance & Trends</h1>", unsafe_allow_html=True)
st.markdown("---")
st.sidebar.title("Dashboard Filters and Features")
st.sidebar.markdown(
'''
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
'''
)

loan = pd.read_pickle('data_input/loan_clean')
loan['purpose'] = loan['purpose'].str.replace("_"," ").str.title()

with st.container(border=True):
    col1, col2 = st.columns(2)
    col1.metric("Total Loans", f"{loan.shape[0]:,}")
    col1.metric("Total Loan Amount", f"$ {loan['loan_amount'].sum():,.0f}")
    col2.metric("Average Interest Rate", f"{loan['interest_rate'].mean():.2f}%")
    col2.metric("Average Loan Amount", f"$ {loan['loan_amount'].mean():,.0f}")

with st.container(border=True):
    tab1, tab2, tab3 = st.tabs(['Loan Issued Over Time', 'Loan Amount Over Time', 'Issue Data Analysis'])

with tab1:
    loan_date_count = loan.groupby('issue_date')['loan_amount'].count()
    line_count = px.line(
        loan_date_count,
        markers= True,
        title= 'Number of Loans Over Time',
        labels = {
            'issue_date': 'Issue Date',
            'value': 'Number of Loans',
            'variable' : 'Variable'
        },
        template= 'seaborn'
    ).update_layout(showlegend = False)
    st.plotly_chart(line_count)

with tab2:
    loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()
    line_sum = px.line(
        loan_date_sum,
        markers= True,
        title= 'Total Loans Amount Issued Over Time',
        labels = {
            'issue_date': 'Issue Date',
            'value': 'Number of Loans',
            'variable' : 'Variable'
        },
        template= 'seaborn'
    ).update_layout(showlegend = False)
    st.plotly_chart(line_sum)

with tab3:
    loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()
    day_count = px.bar(
        loan_day_count,
        category_orders= {
            'issue_weekday':['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        },
        title= 'Distribution of Loans by Day of The Week',
        labels = {
            'issue_weekday': 'Issue Weekday',
            'value': 'Number of Loans',
            'variable' : 'Variable'
        },
        template= 'seaborn'
    ).update_layout(showlegend = False)
    st.plotly_chart(day_count)

st.subheader('Loan Performance')
with st.expander('', expanded = True):
    loan1, loan2 = st.columns(2)

with loan1:
    loan_condition_counts = loan['loan_condition'].value_counts()
    loan_pie = px.pie(
        loan_condition_counts,
        names = loan_condition_counts.index,
        values = loan_condition_counts.values,
        hole = 0.4,
        labels={
        'loan_condition': 'Loan Condition',
        'value': 'Number of Loans'
        },
        title = 'Distribution of Loans by Condition',
        template = 'seaborn'
    ).update_traces(textinfo = 'percent + value')
    st.plotly_chart(loan_pie)

with loan2:
    grade = loan['grade'].value_counts().sort_index()
    loan_bar = px.bar(
        grade,
        labels = {
            'index': 'Grade',
            'value': 'Number of Loans',
            'variable' : 'Variable'
        },
        title = 'Distribution of Loans by Grade',
        template = 'seaborn'
    ).update_layout(showlegend = False)
    st.plotly_chart(loan_bar)

st.markdown("---")