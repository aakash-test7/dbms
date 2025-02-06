# Bank Database Management Application

This is a Streamlit-based web application for managing a bank database. It allows users to connect to a MySQL database, create tables, and perform CRUD operations such as adding, modifying, and displaying customer records. It also supports operations like displaying customer passbooks, branch passbooks, and more.

## Features

- **Connect to MySQL Database**: Users can connect to a MySQL database and create a new one if it doesn't exist.
- **Create Tables**: Ability to create new tables with predefined structures.
- **Add Customer Records**: Users can add customer information including applicant number, name, IFSC code, credit, debit, balance, city, and branch code.
- **Display Records**: View all records, or search for specific records by applicant number.
- **Modify Records**: Modify existing customer records, such as changing the name, city, or branch.
- **Delete Records**: Option to delete all records or delete specific records.
- **Display Passbook**: Display passbook information for all customers, a specific branch, or a specific customer.

## Requirements

- Python 3.8 or higher
- Streamlit
- pymysql

To install the required dependencies, run the following:

```bash
pip install -r requirements.txt
