import streamlit as st

def directsqlcode():
    st.title("SQL Queries")
    st.subheader("SQL query to create a table")
    st.code("""
    CREATE TABLE IF NOT EXISTS {st.session_state.tablename} (
        Applicant_no INTEGER PRIMARY KEY,
        Name CHAR(15),
        IFSC FLOAT,
        Credit FLOAT DEFAULT 0.0,
        Debit FLOAT DEFAULT 0.0,
        Balance FLOAT DEFAULT 0.0,
        City CHAR(10),
        Branch INTEGER
    );
    """, language='sql')

    # Displaying the code for adding customer records
    st.subheader(" SQL query to insert a record into the table")
    st.code("""
    INSERT INTO {st.session_state.tablename} VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, language='sql')

    # Display all records SQL query
    st.subheader("SQL query to select all records from the table")
    st.code("""
    SELECT * FROM {st.session_state.tablename};
    """, language='sql')

    # SQL query to display a specific record by Applicant_no
    st.subheader("SQL query to select a specific record")
    st.code("""
    SELECT * FROM {st.session_state.tablename} WHERE Applicant_no={en};
    """, language='sql')

    # SQL query to delete all records
    st.subheader("SQL query to delete all records from the table")
    st.code("""
    DELETE FROM {st.session_state.tablename};
    """, language='sql')

    # SQL query to modify a record
    st.subheader("SQL query to update a specific record")
    st.code("""
    UPDATE {st.session_state.tablename} SET Name='{name}', City='{city}', Branch='{branch}' WHERE Applicant_no={en};
    """, language='sql')

    # Display passbook for all customers
    st.subheader("SQL query to select all records to display a passbook for all customers")
    st.code("""
    SELECT * FROM {st.session_state.tablename};
    """, language='sql')

    # Display branch passbook
    st.subheader("SQL query to select records for a specific branch")
    st.code("""
    SELECT * FROM {st.session_state.tablename} WHERE Branch = %s;
    """, language='sql')

    # Display customer passbook for a specific applicant
    st.subheader("SQL query to select a specific applicant's record for a passbook")
    st.code("""
    SELECT * FROM {st.session_state.tablename} WHERE Applicant_no={en};
    """, language='sql')
    return

if __name__=="__main__":
    directsqlcode()
