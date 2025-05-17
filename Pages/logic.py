import pymysql
import streamlit as st
import pandas as pd

def is_valid_identifier(name):
    """
    Validates a database or table name for SQL safety
    Returns (is_valid, message)
    """
    import re
    
    # Check for empty string
    if not name or name.strip() == "":
        return False, "Name cannot be empty"
    
    # Check that it consists only of allowed characters
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
        return False, "Name can only contain letters, numbers, and underscores, and must start with a letter or underscore"
    
    # List of common SQL keywords to avoid
    sql_keywords = ["SELECT", "FROM", "WHERE", "INSERT", "DELETE", "UPDATE", "DROP", "CREATE", "TABLE", 
                   "DATABASE", "ALTER", "INDEX", "VIEW"]
    
    # Check it's not a SQL keyword
    if name.upper() in sql_keywords:
        return False, "Name cannot be a SQL keyword"
    
    return True, "Valid identifier"

def logic():
    # Initialize session state variables
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
    if 'connection_initiated' not in st.session_state:
        st.session_state.connection_initiated = False
    if 'current_database' not in st.session_state:
        st.session_state.current_database = None
    
    # Function to check if connection is still alive and reconnect if needed
    def ensure_connection():
        if st.session_state.db_connected and st.session_state.mydb:
            try:
                # Test if connection is alive
                st.session_state.mycursor.execute("SELECT 1")
                return True
            except:
                # Connection lost, try to reconnect
                try:
                    mysql_config = st.secrets["mysql"]
                    host = mysql_config["host"]
                    user = mysql_config["user"]
                    password = mysql_config["password"]
                    port = mysql_config["port"]
                    
                    st.session_state.mydb = pymysql.connect(
                        host=host, 
                        user=user, 
                        password=password, 
                        port=port, 
                        ssl={'ssl': {}}
                    )
                    
                    if st.session_state.current_database:
                        st.session_state.mydb.select_db(st.session_state.current_database)
                        
                    st.session_state.mycursor = st.session_state.mydb.cursor()
                    return True
                except Exception as e:
                    st.error(f"Lost connection and failed to reconnect: {e}")
                    st.session_state.db_connected = False
                    st.session_state.mydb = None
                    st.session_state.mycursor = None
                    return False
        return st.session_state.db_connected

    st.title("Start Operations")
    con=st.container(border=True)
    with con:
        db = st.text_input("Enter name of your database:", value="testing1")
        con1,con2,con3=st.columns([2,2,2])
        with con2:
            connect_button = st.button("Connect to Database", use_container_width=True)
            mysql_config = st.secrets["mysql"]
            host = mysql_config["host"]
            user = mysql_config["user"]
            password = mysql_config["password"]
            port = mysql_config["port"]
            
            # Only attempt connection if explicitly requested or not initiated
            if connect_button:
                if db:
                    is_valid, message = is_valid_identifier(db)
                    if is_valid:
                        try:
                            # Close any existing connection
                            if st.session_state.mydb:
                                try:
                                    st.session_state.mydb.close()
                                except:
                                    pass
                                
                            # Create new connection
                            st.session_state.mydb = pymysql.connect(
                                host=host, 
                                user=user, 
                                password=password, 
                                port=port, 
                                ssl={'ssl': {}}
                            )
                            
                            st.session_state.mycursor = st.session_state.mydb.cursor()
                            
                            # Use format for database name - safe now that we've validated
                            st.session_state.mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
                            st.session_state.mydb.commit()
                            st.session_state.mycursor.execute(f"USE {db}")
                            
                            # Store the current database name
                            st.session_state.current_database = db
                            st.session_state.db_connected = True
                            st.session_state.connection_initiated = True
                            
                            st.success(f"Database '{db}' created and connected successfully.")
                        except Exception as e:
                            st.error(f"Error connecting to the database: {e}")
                    else:
                        st.error(f"Invalid database name: {message}")
                else:
                    st.warning("Please enter a database name.")

    # Display database status
    if st.session_state.db_connected:
        st.sidebar.success(f"✅ Connected to database: {st.session_state.current_database}")
    else:
        st.sidebar.warning("❌ Not connected to any database")

    # Ensure connection is active before operations
    if st.session_state.db_connected:
        active_connection = ensure_connection()
        
        # Rest of your logic continues here, but only if connection is active
        if active_connection:
            # Default table name
            default_table = "try"
            if 'tablename' not in st.session_state:
                st.session_state.tablename = default_table

            # Create Table if not exists
            try:
                query1 = """
                CREATE TABLE IF NOT EXISTS {} (
                    Applicant_no INTEGER PRIMARY KEY,
                    Name CHAR(15),
                    IFSC FLOAT,
                    Credit FLOAT DEFAULT 0.0,
                    Debit FLOAT DEFAULT 0.0,
                    Balance FLOAT DEFAULT 0.0,
                    City CHAR(10),
                    Branch INTEGER
                )
                """.format(st.session_state.tablename)
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
                        ano = st.number_input("Enter application number:", min_value=1, step=1)
                    name = st.text_input("Enter name:")
                    ifsc = st.number_input("Enter IFSC code:", min_value=0.0)
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
                    if con2.button("Add Record", use_container_width=True):
                        if not name.strip() or not city.strip():
                            st.warning("Name and City fields cannot be empty.")
                        else:
                            try:
                                # Convert to appropriate types
                                ano_val = int(ano)
                                branch_val = int(branch)
                                ifsc_val = float(ifsc)
                                c_val = float(c)
                                d_val = float(d)
                                b_val = float(b)
                                
                                # Prepare record with proper data types
                                rec = (ano_val, name.strip(), ifsc_val, c_val, d_val, b_val, city.strip(), branch_val)
                                
                                # Ensure connection is still alive before executing
                                if ensure_connection():
                                    query3 = 'INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'.format(st.session_state.tablename)
                                    st.session_state.mycursor.execute(query3, rec)
                                    st.session_state.mydb.commit()
                                    
                                    # Display formatted SQL for reference
                                    display_query = f'''
                                    INSERT INTO {st.session_state.tablename} VALUES
                                    ({ano_val}, '{name.strip()}', {ifsc_val}, {c_val}, {d_val}, {b_val}, '{city.strip()}', {branch_val})
                                    '''
                                    st.code(display_query, language="sql")
                                    st.success("Record added successfully!")
                                else:
                                    st.error("Database connection lost. Please reconnect.")
                            except pymysql.err.IntegrityError as e:
                                if "Duplicate entry" in str(e):
                                    st.error(f"Applicant number {ano} already exists.")
                                else:
                                    st.error(f"Database integrity error: {e}")
                            except Exception as e:
                                st.error(f"Error adding record: {e}")

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

            # Display Specific Record - With parameterized query
            elif st.session_state.selected_option == 'Display Specific Record':
                con = st.container(border=True)
                with con:
                    en = st.text_input("Enter applicant no. of the record to be displayed:")
                    con1,con2,con3=st.columns([2,2,2])
                    if en and con2.button("Show Specific Record",use_container_width=True):
                        try:
                            # Parameterized query
                            query5 = "SELECT * FROM {} WHERE Applicant_no=%s".format(st.session_state.tablename)
                            st.session_state.mycursor.execute(query5, (en,))
                            columns = [desc[0] for desc in st.session_state.mycursor.description]
                            record = st.session_state.mycursor.fetchone()
                            if record:
                                df = pd.DataFrame([record], columns=columns)
                                st.write(f"Record of Applicant no. {en}:")
                                st.dataframe(df, use_container_width=True)
                                st.code(f"SELECT * FROM {st.session_state.tablename} WHERE Applicant_no={en}", language="sql")
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

            # Modify Record - With parameterized query
            elif st.session_state.selected_option == 'Modify Record':
                con = st.container(border=True)
                with con:
                    en = st.text_input("Enter applicant no. of the record to be modified:")
                    con1,con2,con3=st.columns([2,2,2])
                    if en and con2.button("Modify Record",use_container_width=True):
                        try:
                            # Parameterized query
                            query7 = "SELECT * FROM {} WHERE Applicant_no=%s".format(st.session_state.tablename)
                            st.session_state.mycursor.execute(query7, (en,))
                            myrecord = st.session_state.mycursor.fetchone()
                            st.code(f"SELECT * FROM {st.session_state.tablename} WHERE Applicant_no={en}", language="sql")
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
                                        # Parameterized query for update
                                        query8 = "UPDATE {} SET Name=%s, City=%s, Branch=%s WHERE Applicant_no=%s".format(st.session_state.tablename)
                                        st.session_state.mycursor.execute(query8, (name, city, branch, en))
                                        st.session_state.mydb.commit()
                                        st.code(f"UPDATE {st.session_state.tablename} SET Name='{name}', City='{city}', Branch='{branch}' WHERE Applicant_no={en}", language="sql")
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

            # Customer Passbook - With parameterized query
            elif st.session_state.selected_option == 'Display Customer Passbook':
                con = st.container(border=True)
                with con:
                    en = st.text_input("Enter applicant no. of the record to display passbook:")
                    con1,con2,con3=st.columns([2,2,2])
                    if en and con2.button(f"Show Passbook for Applicant no. {en}",use_container_width=True):
                        try:
                            # Parameterized query
                            query11 = "SELECT * FROM {} WHERE Applicant_no=%s".format(st.session_state.tablename)
                            st.session_state.mycursor.execute(query11, (en,))
                            columns = [desc[0] for desc in st.session_state.mycursor.description]
                            data = st.session_state.mycursor.fetchone()
                            if data:
                                df = pd.DataFrame([data], columns=columns)
                                st.write(f"Passbook for Applicant no. {en}")
                                st.code(f"SELECT * FROM {st.session_state.tablename} WHERE Applicant_no={en}", language="sql")
                                st.write(df)
                            else:
                                st.warning("No record found for the provided applicant number")
                        except Exception as e:
                            st.error(f"Error fetching customer passbook: {e}")

    # Add connection close button in case user wants to manually close
    if st.session_state.db_connected:
        if st.sidebar.button("Close Database Connection"):
            try:
                st.session_state.mydb.close()
            except:
                pass
            st.session_state.db_connected = False
            st.session_state.mydb = None
            st.session_state.mycursor = None
            st.session_state.connection_initiated = False
            st.sidebar.success("Database connection closed manually")
    
    return

# Add function to force connection closing when exiting the app
def on_shutdown():
    if 'mydb' in st.session_state and st.session_state.mydb:
        st.session_state.mydb.close()
        st.session_state.db_connected = False
        
if __name__=="__main__":
    logic()
