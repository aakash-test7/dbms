import streamlit as st
import streamlit.components.v1 as components
import base64

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
        with open("Pages/structure.html", "r") as f:
            html_content=f.read()
        encoded_html = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
        st.subheader("Structure")
        iframe_code = f'''
        <iframe src="data:text/html;base64,{encoded_html}" width="100%" height="500" style="border: 2px solid black;" frameborder="0"></iframe>
        '''
        components.html(iframe_code, height=600)
        with open("Pages/markmap.html", "r") as f:
            html_content2 = f.read()
        encoded_html2 = base64.b64encode(html_content2.encode('utf-8')).decode('utf-8')
        st.subheader("MarkMap")
        iframe_code2 = f'''
        <iframe src="data:text/html;base64,{encoded_html2}" width="100%" height="500" style="border: 2px solid black;" frameborder="0"></iframe>
        '''
        components.html(iframe_code2, height=600)
    return

if __name__=="__main__":
    introduction()
