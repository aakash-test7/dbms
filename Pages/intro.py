import streamlit as st

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
        st.image("/Users/aakash27/Desktop/Project1 Passion/dbms/Images/er.001.jpeg",use_container_width=True)
        return

if __name__=="__page__":
    introduction()