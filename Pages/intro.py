import streamlit as st
import streamlit.components.v1 as components

def introduction():
    with st.container():
        st.markdown("# Welcome to the Bank Database Management System")
        st.markdown("""
        ## Introduction
        This system allows you to perform various operations related to bank customer records management. It supports:
        
        - **Database Management**: Create and connect to your database.
        - **Table Operations**: Create tables for customer records, add, delete, modify, and display customer data.
        - **Passbook Management**: Display passbooks for all customers, specific branches, or individual customers.
        - **User-Friendly Interface**: Select options from a dropdown menu to perform the desired actions.
        
        ## Features
        - **Create a Database**: Easily create a database for storing customer records.
        - **Create Tables**: Define the structure of customer records with columns like Applicant Number, Name, Credit, Debit, etc.
        - **Add Customer Records**: Add customer details including their credit, debit, and balance.
        - **Display and Modify Records**: View and update customer data as needed.
        - **Delete Records**: Option to delete records either specifically or all at once.
        - **Display Passbooks**: View detailed passbooks for customers and branches.
        
        ## Instructions
        - **Step 1**: Connect to the database by entering the database name.
        - **Step 2**: Create a table to store customer records.
        - **Step 3**: Add, modify, display, or delete records as per your requirements.
        - **Step 4**: View passbooks for customers or branches.
        """)
        st.image("Images/er.001.jpeg",use_container_width=True)

        with open("Pages/markmap.html", "r") as f:
            html_content = f.read()
        iframe_code = f'<iframe srcdoc="{html_content}" width="100%" height="600" frameborder="0"></iframe>'
        components.html(iframe_code, height=600)
        return

if __name__=="__page__":
    introduction()
