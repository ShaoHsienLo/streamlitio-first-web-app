import streamlit as st
from streamlit_option_menu import option_menu
from views import home, dashboard, history

st.set_page_config(layout="wide", page_title="Dashboard")

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Add all pages in views folder

menu = ["主頁面", "戰情看版", "歷史查詢"]

with st.sidebar:
    selected = option_menu(
        menu_title="頁面總攬",
        options=menu,
        icons=None,
        menu_icon="menu-down",
        default_index=0
    )

if selected == "主頁面":
    home.create_page()
elif selected == "戰情看版":
    dashboard.create_page()
elif selected == "歷史查詢":
    history.create_page()


