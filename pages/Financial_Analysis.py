import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("Financial Analysis")
    st.write("This is the Financial Analysis page.")

loan = pd.read_pickle('data_input/loan_clean')
loan['purpose'] = loan['purpose'].str.replace("_"," ").str.title()

st.subheader('Financial Analysis')
option = st.selectbox('Select Loan Condition', ('Good Loan', 'Bad Loan'))
loan_condition = loan[loan['loan_condition'] == option]

with st.container(border=True):
    tab_hist, tab_box = st.tabs(['Loan Amount Distribution', 'Loan Amount Distribution by Purpose'])

with tab_hist:
    loan_amount_hist = px.histogram(
        loan_condition,
        x = 'loan_amount',
        color = 'term',
        template = 'seaborn',
        nbins = 30,
        title ='Loan Amount Distribution by Term',
        labels ={
            'loan_amount': 'Loan Amount',
            'term' : 'Loan Term'
        }
    )
    st.plotly_chart(loan_amount_hist)

with tab_box:
    loan_amount_bar = px.box(
        loan_condition,
        x = 'purpose',
        y = 'loan_amount',
        color = 'term',
        template = 'seaborn',
        title = 'Loan Amount Distribution by Purpose',
        labels ={
            'loan_amount': 'Loan Amount',
            'term': 'Loan Term',
            'purpose': 'Loan Purpose'
        }
    )
    st.plotly_chart(loan_amount_bar)