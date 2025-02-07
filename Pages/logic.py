import pymysql
import streamlit as st
import pandas as pd

def logic():
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

    st.title("Start Operations")
    con=st.container(border=True)
    with con:
        db = st.text_input("Enter name of your database:", value="testing1")
        con1,con2,con3=st.columns([2,2,2])
        with con2:
            connect_button = st.button("Connect to Database",use_container_width=True)
            mysql_config = st.secrets["mysql"]
            host = mysql_config["host"]
            user = mysql_config["user"]
            password = mysql_config["password"]
            port = mysql_config["port"]
            
            if connect_button:
                if db:
                    try:
                        st.session_state.mydb = pymysql.connect(host=host, user=user, password=password, port=port, ssl={'ssl': {}})
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
            query1 = f"""
            CREATE TABLE IF NOT EXISTS {st.session_state.tablename} (
                Applicant_no INTEGER PRIMARY KEY,
                Name CHAR(15),
                IFSC FLOAT,
                Credit FLOAT DEFAULT 0.0,
                Debit FLOAT DEFAULT 0.0,
                Balance FLOAT DEFAULT 0.0,
                City CHAR(10),
                Branch INTEGER
            )
            """
            st.session_state.mycursor.execute(query1)
            st.session_state.mydb.commit()
            st.session_state.table_created = True
            con=st.container(border=True)
            with con:
                st.code(query1, language="sql")

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
            con=st.container(border=True)
            with con:
                tablename = st.text_input("Enter name of the table to be created:", value=default_table)
                con1,con2,con3=st.columns([2,2,2])
                if tablename and con2.button(f"Create Table '{tablename}'",use_container_width=True):
                    try:
                        query2 = f"""
                        CREATE TABLE IF NOT EXISTS {tablename} (
                            Applicant_no INTEGER PRIMARY KEY,
                            Name CHAR(15),
                            IFSC FLOAT,
                            Credit FLOAT DEFAULT 0.0,
                            Debit FLOAT DEFAULT 0.0,
                            Balance FLOAT DEFAULT 0.0,
                            City CHAR(10),
                            Branch INTEGER
                        )
                        """
                        st.session_state.mycursor.execute(query2)
                        st.session_state.mydb.commit()
                        st.session_state.tablename = tablename
                        st.session_state.table_created = True
                        st.code(query2, language="sql")
                        st.success(f"Table '{tablename}' created successfully.")
                    except Exception as e:
                        st.error(f"Error creating table: {e}")

        # Add Customer Records
        elif st.session_state.selected_option == 'Add Customer Records':
            con = st.container(border=True)
            with con:
                st.subheader("Enter Customer Information")
                con1, con2, con3 = st.columns([1, 3, 1])
                with con2:
                    ano = st.number_input("Enter application number:", min_value=1)
                name = st.text_input("Enter name:")
                ifsc = st.number_input("Enter IFSC code:")
                con1, con2 = st.columns(2)
                with con1:
                    c = st.number_input("Enter amount credited:", min_value=0.0, format="%.2f")
                with con2:
                    d = st.number_input("Enter amount debited:", min_value=0.0, format="%.2f")
                con1, con2, con3 = st.columns([1, 3, 1])
                with con2:
                    b = st.number_input("Enter account balance:", min_value=0.0, format="%.2f")
                con1, con2 = st.columns(2)
                with con1:
                    city = st.text_input("Enter city name:")
                with con2:
                    branch = st.number_input("Enter branch code:", min_value=1)
                con1,con2,con3=st.columns([1,1,1])
                if con2.button("Add Record",use_container_width=True):
                        try:
                            rec = (ano, name, ifsc, c, d, b, city, branch)
                            query3 = 'INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'.format(st.session_state.tablename)
                            st.session_state.mycursor.execute(query3, rec)
                            st.session_state.mydb.commit()
                            st.code(query3, language="sql")
                            st.success("Record added successfully!")
                        except Exception as e:
                            st.error(f"Something went wrong: {e}")

        # Display All Records
        elif st.session_state.selected_option == 'Display All Records':
            con = st.container(border=True)
            with con:
                con1,con2,con3=st.columns([2,2,2])
                if con2.button("Show All Records",use_container_width=True):
                    try:
                        query4 = f'SELECT * FROM {st.session_state.tablename}'
                        st.session_state.mycursor.execute(query4)
                        columns = [desc[0] for desc in st.session_state.mycursor.description]
                        records = st.session_state.mycursor.fetchall()
                        df = pd.DataFrame(records, columns=columns)
                        st.dataframe(df, use_container_width=True)
                        st.code(query4, language="sql")
                    except Exception as e:
                        st.error(f"Error fetching records: {e}")

        # Display Specific Record
        elif st.session_state.selected_option == 'Display Specific Record':
            con = st.container(border=True)
            with con:
                en = st.text_input("Enter applicant no. of the record to be displayed:")
                con1,con2,con3=st.columns([2,2,2])
                if en and con2.button("Show Specific Record",use_container_width=True):
                    try:
                        query5 = f'SELECT * FROM {st.session_state.tablename} WHERE Applicant_no={en}'
                        st.session_state.mycursor.execute(query5)
                        columns = [desc[0] for desc in st.session_state.mycursor.description]
                        record = st.session_state.mycursor.fetchone()
                        df = pd.DataFrame([record], columns=columns)
                        if record:
                            st.write(f"Record of Applicant no. {en}:")
                            st.dataframe(df, use_container_width=True)
                            st.code(query5, language="sql")
                        else:
                            st.warning("No record found")
                    except Exception as e:
                        st.error(f"Error fetching record: {e}")

        # Delete All Records
        elif st.session_state.selected_option == 'Delete All Records':
            con = st.container(border=True)
            with con:
                with st.form(key='delete_form'):
                    ch = st.selectbox("Do you want to delete all records?", ['No', 'Yes'])
                    con1,con2,con3=st.columns([2,2,2])
                    submit_button = con2.form_submit_button("Submit",use_container_width=True)

                if submit_button:
                    if ch == 'Yes':
                        try:
                            query6 = f'DELETE FROM {st.session_state.tablename}'
                            st.session_state.mycursor.execute(query6)
                            st.session_state.mydb.commit()
                            st.session_state.deleted = True
                            st.success("All records deleted.")
                            st.code(query6, language="sql")

                        except Exception as e:
                            st.error(f"Error deleting records: {e}")

        # Modify Record
        elif st.session_state.selected_option == 'Modify Record':
            con = st.container(border=True)
            with con:
                en = st.text_input("Enter applicant no. of the record to be modified:")
                con1,con2,con3=st.columns([2,2,2])
                if en and con2.button("Modify Record",use_container_width=True):
                    try:
                        query7 = f'SELECT * FROM {st.session_state.tablename} WHERE Applicant_no={en}'
                        st.session_state.mycursor.execute(query7)
                        myrecord = st.session_state.mycursor.fetchone()
                        st.code(query7, language="sql")
                        columns = [desc[0] for desc in st.session_state.mycursor.description]

                        if myrecord:
                            if len(myrecord) < len(columns):
                                myrecord = myrecord + (None,) * (len(columns) - len(myrecord))

                            df = pd.DataFrame([myrecord], columns=columns)
                            st.write(f"Current details for Applicant no. {en}:")
                            st.dataframe(df, use_container_width=True)

                            # Use a form for modification
                            with st.form(key='modify_form'):
                                # Modify fields (pre-filled with current record values)
                                name = st.text_input("Modify Name:", value=myrecord[1] if myrecord[1] else "")
                                city = st.text_input("Modify City:", value=myrecord[6] if myrecord[6] else "")
                                branch = st.text_input("Modify Branch:", value=myrecord[7] if myrecord[7] else "")

                                # Submit button inside the form
                                con1,con2,con3=st.columns([2,2,2])
                                submit_button = con2.form_submit_button("Save Changes",use_container_width=True)

                                if submit_button:
                                    # Only save changes if the form is submitted
                                    query8 = f"UPDATE {st.session_state.tablename} SET Name='{name}', City='{city}', Branch='{branch}' WHERE Applicant_no={en}"
                                    st.session_state.mycursor.execute(query8)
                                    st.session_state.mydb.commit()
                                    st.code(query8, language="sql")
                                    st.success("Record modified successfully")
                        else:
                            st.warning("No record found for the provided applicant number")
                    except Exception as e:
                            st.error(f"Error modifying record: {e}")


        # Display Passbook for All Customers
        elif st.session_state.selected_option == 'Display Passbook':
            con = st.container(border=True)
            with con:
                con1,con2,con3=st.columns([2,2,2])
                if con2.button("Show Passbook for All Customers",use_container_width=True):
                    try:
                        query9 = f'SELECT * FROM {st.session_state.tablename}'
                        st.session_state.mycursor.execute(query9)
                        columns = [desc[0] for desc in st.session_state.mycursor.description]
                        records = st.session_state.mycursor.fetchall()
                        df = pd.DataFrame(records, columns=columns)
                        st.write("Passbook for All Customers")
                        st.code(query9, language="sql")
                        st.dataframe(df, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error fetching passbook: {e}")

        # Display Branch Passbook
        elif st.session_state.selected_option == 'Display Branch Passbook':
            con = st.container(border=True)
            with con:
                a = st.text_input("Enter branch code:")
                con1,con2,con3=st.columns([2,2,2])
                if a and con2.button(f"Show Passbook for Branch {a}",use_container_width=True):
                    try:
                        query10 = "SELECT * FROM {} WHERE Branch = %s".format(st.session_state.tablename)
                        st.session_state.mycursor.execute(query10, (a,))
                        columns = [desc[0] for desc in st.session_state.mycursor.description]
                        data = st.session_state.mycursor.fetchall()
                        df = pd.DataFrame(data, columns=columns)
                        st.write(f"Passbook for Branch {a}")
                        st.dataframe(df, use_container_width=True)
                        st.code(query10, language="sql")
                    except Exception as e:
                        st.error(f"Error fetching branch passbook: {e}")

        # Display Customer Passbook
        elif st.session_state.selected_option == 'Display Customer Passbook':
            con = st.container(border=True)
            with con:
                en = st.text_input("Enter applicant no. of the record to display passbook:")
                con1,con2,con3=st.columns([2,2,2])
                if en and con2.button(f"Show Passbook for Applicant no. {en}",use_container_width=True):
                    try:
                        query11 = f'SELECT * FROM {st.session_state.tablename} WHERE Applicant_no={en}'
                        st.session_state.mycursor.execute(query11)
                        columns = [desc[0] for desc in st.session_state.mycursor.description]
                        data = st.session_state.mycursor.fetchone()
                        if data:
                            df = pd.DataFrame([data], columns=columns)
                            st.write(f"Passbook for Applicant no. {en}")
                            st.code(query11, language="sql")
                            st.write(df)
                        else:
                            st.warning("No record found for the provided applicant number")
                    except Exception as e:
                        st.error(f"Error fetching customer passbook: {e}")
    return

if __name__=="__page__":
    logic()