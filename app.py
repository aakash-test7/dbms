import streamlit as st

st.set_page_config("DataBaseManagementSystem App",layout="wide")
st.logo("Images/moneyrun.gif")
st.markdown("""<style>.stLogo {    width: 48px;    height: 48px;}</style>""", unsafe_allow_html=True)

pages = [
    st.Page("Pages/intro.py", title="Introduction", icon="🏠"),
    st.Page("Pages/logic.py", title="Task", icon="👨🏻‍💻"),
    st.Page("Pages/direct_sql_code.py", title="SQL queries", icon="📗"),
    st.Page("Pages/src_code.py", title="Source Code", icon="📕")
]

pg=st.navigation(pages, position="sidebar", expanded=True)
pg.run()
