import pymysql
import streamlit as st
st.set_page_config(layout="wide")
# Initialize session state
if 'db_connected' not in st.session_state:
    st.session_state.db_connected = False
if 'table_created' not in st.session_state:
    st.session_state.table_created = False
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None
if 'mydb' not in st.session_state:
    st.session_state.mydb = None
if 'mycursor' not in st.session_state:
    st.session_state.mycursor = None

st.title("Bank Database Management")
db = st.text_input("Enter name of your database:", value="testing1")
connect_button = st.button("Connect to Database")
mysql_config = st.secrets["mysql"]
host = mysql_config["host"]
user = mysql_config["user"]
password = mysql_config["password"]
port = mysql_config["port"]
if connect_button:
    if db:
        try:
            st.session_state.mydb = pymysql.connect(host=host,user=user,password=password,port=port,ssl={'ssl': {}})
            st.session_state.mycursor = st.session_state.mydb.cursor()
            st.session_state.mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
            st.session_state.mydb.commit()
            st.session_state.mycursor.execute(f"USE {db}")
            st.session_state.db_connected = True
            st.success(f"Database '{db}' created and connected successfully.")
        except Exception as e:
            st.error(f"Error connecting to the database: {e}")
    else:
        st.warning("Please enter a database name.")

# Proceed only if the database is connected
if st.session_state.db_connected:
    # Default table name
    default_table = "try"
    if 'tablename' not in st.session_state:
        st.session_state.tablename = default_table

    # Create Table if not exists
    try:
        query = f"""
        CREATE TABLE IF NOT EXISTS {st.session_state.tablename} (
            Applicant_no INTEGER PRIMARY KEY,
            Name CHAR(15),
            IFSC INTEGER UNIQUE,
            Credit FLOAT DEFAULT 0.0,
            Debit FLOAT DEFAULT 0.0,
            Balance FLOAT DEFAULT 0.0,
            City CHAR(10),
            Branch INTEGER
        )
        """
        st.session_state.mycursor.execute(query)
        st.session_state.mydb.commit()
        st.session_state.table_created = True
    except Exception as e:
        st.error(f"Error creating table: {e}")

    # Dropdown for selecting an option
    options = [
        'Create Table', 'Add Customer Records', 'Display All Records', 'Display Specific Record',
        'Delete All Records', 'Delete Specific Record', 'Modify Record',
        'Display Passbook', 'Display Branch Passbook', 'Display Customer Passbook'
    ]
    selected_option = st.selectbox("Choose an option:", options)
    st.session_state.selected_option = selected_option

    # Create Table
    if st.session_state.selected_option == 'Create Table':
        tablename = st.text_input("Enter name of the table to be created:", value=default_table)
        if tablename and st.button(f"Create Table '{tablename}'"):
            try:
                query = f"""
                CREATE TABLE IF NOT EXISTS {tablename} (
                    Applicant_no INTEGER PRIMARY KEY,
                    Name CHAR(15),
                    IFSC INTEGER UNIQUE,
                    Credit FLOAT DEFAULT 0.0,
                    Debit FLOAT DEFAULT 0.0,
                    Balance FLOAT DEFAULT 0.0,
                    City CHAR(10),
                    Branch INTEGER
                )
                """
                st.session_state.mycursor.execute(query)
                st.session_state.mydb.commit()
                st.session_state.tablename = tablename
                st.session_state.table_created = True
                st.success(f"Table '{tablename}' created successfully.")
            except Exception as e:
                st.error(f"Error creating table: {e}")

    # Add Customer Records
    elif st.session_state.selected_option == 'Add Customer Records':
        con=st.container(border=True)
        with con:
            st.subheader("Enter Customer Information")
            con1,con2,con3=st.columns([1,3,1])
            with con2:
                ano = st.number_input("Enter application number:", min_value=1)
            name = st.text_input("Enter name:")
            ifsc = st.number_input("Enter IFSC code:")
            con1,con2=st.columns(2)
            with con1:
                c = st.number_input("Enter amount credited:", min_value=0.0, format="%.2f")
            with con2:
                d = st.number_input("Enter amount debited:", min_value=0.0, format="%.2f")
            con1,con2,con3=st.columns([1,3,1])
            with con2:
                b = st.number_input("Enter account balance:", min_value=0.0, format="%.2f")
            con1,con2=st.columns(2)
            with con1:
                city = st.text_input("Enter city name:")
            with con2:
                branch = st.number_input("Enter branch code:", min_value=1)
            if st.button("Add Record"):
                try:
                    rec = (ano, name, ifsc, c, d, b, city, branch)
                    query = f'INSERT INTO {st.session_state.tablename} VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                    st.session_state.mycursor.execute(query, rec)
                    st.session_state.mydb.commit()
                    st.success("Record added successfully!")
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    # Display All Records
    elif st.session_state.selected_option == 'Display All Records':
        con=st.container(border=True)
        with con:
            if st.button("Show All Records"):
                try:
                    query = f'SELECT * FROM {st.session_state.tablename}'
                    st.session_state.mycursor.execute(query)
                    records = st.session_state.mycursor.fetchall()
                    st.dataframe(records)
                except Exception as e:
                    st.error(f"Error fetching records: {e}")

    # Display Specific Record
    elif st.session_state.selected_option == 'Display Specific Record':
        con=st.container(border=True)
        with con:
            en = st.text_input("Enter applicant no. of the record to be displayed:")
            if en and st.button("Show Specific Record"):
                try:
                    query = f'SELECT * FROM {st.session_state.tablename} WHERE Applicant_no={en}'
                    st.session_state.mycursor.execute(query)
                    record = st.session_state.mycursor.fetchone()
                    if record:
                        st.write(f"Record of Applicant no. {en}:")
                        st.write(record)
                    else:
                        st.warning("No record found")
                except Exception as e:
                    st.error(f"Error fetching record: {e}")

    # Delete All Records
    elif st.session_state.selected_option == 'Delete All Records':
        con=st.container(border=True)
        with con:
            if st.button("Delete All Records"):
                ch = st.selectbox("Do you want to delete all records?", ['No', 'Yes'])
                if ch == 'Yes':
                    try:
                        st.session_state.mycursor.execute(f'DELETE FROM {st.session_state.tablename}')
                        st.session_state.mydb.commit()
                        st.success("All records deleted.")
                    except Exception as e:
                        st.error(f"Error deleting records: {e}")

    # Modify Record
    elif st.session_state.selected_option == 'Modify Record':
        con=st.container(border=True)
        with con:
            en = st.text_input("Enter applicant no. of the record to be modified:")
            if en and st.button("Modify Record"):
                try:
                    query = f'SELECT * FROM {st.session_state.tablename} WHERE Applicant_no={en}'
                    st.session_state.mycursor.execute(query)
                    myrecord = st.session_state.mycursor.fetchone()
                    if myrecord:
                        st.write(f"Current details for Applicant no. {en}:")
                        st.write(myrecord)
                        name = st.text_input("Modify Name:", value=myrecord[1])
                        city = st.text_input("Modify City:", value=myrecord[6])
                        branch = st.text_input("Modify Branch:", value=myrecord[7])

                        if st.button("Save Changes"):
                            query = f"UPDATE {st.session_state.tablename} SET Name='{name}', City='{city}', Branch='{branch}' WHERE Applicant_no={en}"
                            st.session_state.mycursor.execute(query)
                            st.session_state.mydb.commit()
                            st.success("Record modified successfully")
                    else:
                        st.warning("No record found for the provided applicant number")
                except Exception as e:
                    st.error(f"Error modifying record: {e}")

    # Display Passbook for All Customers
    elif st.session_state.selected_option == 'Display Passbook':
        con=st.container(border=True)
        with con:
            if st.button("Show Passbook for All Customers"):
                try:
                    query = f'SELECT * FROM {st.session_state.tablename}'
                    st.session_state.mycursor.execute(query)
                    records = st.session_state.mycursor.fetchall()
                    st.write("Passbook for All Customers")
                    st.dataframe(records)
                except Exception as e:
                    st.error(f"Error fetching passbook: {e}")

    # Display Branch Passbook
    elif st.session_state.selected_option == 'Display Branch Passbook':
        con=st.container(border=True)
        with con:
            a = st.text_input("Enter branch code:")
            if a and st.button(f"Show Passbook for Branch {a}"):
                try:
                    query = f"SELECT * FROM {st.session_state.tablename} WHERE Branch={a}"
                    st.session_state.mycursor.execute(query)
                    data = st.session_state.mycursor.fetchall()
                    st.write(f"Passbook for Branch {a}")
                    st.dataframe(data)
                except Exception as e:
                    st.error(f"Error fetching branch passbook: {e}")

    # Display Customer Passbook
    elif st.session_state.selected_option == 'Display Customer Passbook':
        con=st.container(border=True)
        with con:
            en = st.text_input("Enter applicant no. of the record to display passbook:")
            if en and st.button(f"Show Passbook for Applicant no. {en}"):
                try:
                    query = f'SELECT * FROM {st.session_state.tablename} WHERE Applicant_no={en}'
                    st.session_state.mycursor.execute(query)
                    data = st.session_state.mycursor.fetchone()
                    if data:
                        st.write(f"Passbook for Applicant no. {en}")
                        st.write(data)
                    else:
                        st.warning("No record found for the provided applicant number")
                except Exception as e:
                    st.error(f"Error fetching customer passbook: {e}")