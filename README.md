# Bank Database Management System (DBMS)

🔗 **Live Demo:** [View WeatherWill](https://aakash-dbms.streamlit.app/)  

[![DBMS Demo Video](https://img.youtube.com/vi/tRqVCMsXjeU/hqdefault.jpg)](https://youtu.be/tRqVCMsXjeU)

## Overview
This Bank Database Management System (DBMS) allows users to manage customer records, create tables, insert records, modify data, and interact with a MySQL database via a user-friendly interface.

### Key Features
- **Database Creation and Connection**: Create and connect to a database.
- **Table Operations**: Create, add, modify, and delete records in a table.
- **Passbook Management**: Display passbook information for all customers, specific branches, or individual customers.

---

## Pages

### 1. **Introduction** (`intro.py`)
The introductory page explains the features and usage of the Bank DBMS. It provides an overview of operations such as:
- **Database and Table Operations**: Creating databases and tables for customer records.
- **Record Management**: Adding, deleting, and modifying records in the database.
- **Passbook Operations**: Viewing passbooks for all customers, specific branches, or individuals.

It also includes a visual representation (`MarkMap`) of the database schema for better understanding.

### 2. **Task** (`logic.py`)
The "Task" page allows users to perform operations like:
- **Database Connection**: Establishing a connection to a MySQL database.
- **Table Creation**: Creating tables to store customer data with attributes like `Applicant_no`, `Name`, `Credit`, `Debit`, etc.
- **Record Operations**: Add, modify, delete, or view customer records.
- **Passbook Display**: View all customer records, records for a specific branch, or a specific applicant.

#### Available Options:
- **Create Table**: Create a table with predefined columns for customer records.
- **Add Customer Records**: Insert customer details into the database.
- **Display All Records**: Show all records stored in the table.
- **Modify Record**: Update customer details for a specific applicant.
- **Delete Records**: Delete all or specific records from the table.
- **Display Passbooks**: Display passbook details for all customers or by branch/applicant.

### 3. **SQL Queries** (`direct_sql_code.py`)
This page displays SQL code snippets for performing common database operations:
- **Create Table**: SQL query to create a customer records table.
- **Insert Record**: SQL query to insert a new customer record.
- **Select All Records**: SQL query to fetch all records.
- **Select Specific Record**: SQL query to fetch a record by `Applicant_no`.
- **Delete All Records**: SQL query to remove all records from the table.
- **Update Record**: SQL query to modify a customer’s details.
- **Display Passbook Queries**: SQL queries for displaying passbooks for all customers, by branch, or by individual applicants.

### 4. **Source Code** (`src_code.py`)
This page presents the source code for the entire application, with explanations on database creation, table structure, and various operations like connecting to MySQL and handling form submissions.

---

## Workflow
1. **Introduction**: The user gets an overview of the system, its features, and how to use it.
2. **Logic**: User can perform database operations such as connecting to the database, creating tables, inserting records, modifying records, and viewing passbooks.
3. **SQL Queries**: The system displays the SQL queries used for each operation in the background.
4. **Source Code**: The user can inspect the full source code and understand how each feature is implemented.

---

## Instructions
1. **Connect to the Database**: Enter a database name and click to connect.
2. **Create a Table**: Define the structure of the table to store customer records.
3. **Perform Operations**: Add, modify, delete, or display customer data using the dropdown menu.
4. **View Passbooks**: Display passbook information for all customers, specific branches, or individual applicants.

---

## Technologies Used
- **Streamlit**: Web framework for creating the interactive app.
- **MySQL**: Relational database to store customer records.
- **Python**: Backend programming language for database interaction and form handling.

---

## Conclusion
This Bank DBMS provides a comprehensive solution for managing customer records and interacting with a MySQL database through a simple web interface built with Streamlit.
