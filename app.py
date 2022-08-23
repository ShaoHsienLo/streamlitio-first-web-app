import streamlit as st
# from streamlit_option_menu import option_menu
from views import history_search, page2, page3, dashboard

st.set_page_config(layout="wide", page_title="Dashboard")

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Add all pages in views folder

# 多頁面測邊欄設置
# menu = ["主頁面", "戰情看版", "歷史查詢"]
# with st.sidebar:
#     selected = option_menu(
#         menu_title="頁面總攬",
#         options=menu,
#         icons=None,
#         menu_icon="menu-down",
#         default_index=1
#     )
#
# if selected == "主頁面":
#     home.create_page()
# elif selected == "戰情看版":
#     dashboard.create_page()
# elif selected == "歷史查詢":
#     history.create_page()


# 多頁面導航欄設置
tab0, tab1, tab2 = st.tabs(["戰情看板", "歷史查詢", "其他測試[開發中]"])

with tab0:
    dashboard.init()

with tab1:
    history_search.search()

with tab2:
    page2.init()

# with tab3:
#     page3.init()
