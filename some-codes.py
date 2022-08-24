# import streamlit as st
# from streamlit_option_menu import option_menu
#
#
# st.set_page_config(
#     page_title="Multipage App",
#     page_icon="👋",
#     layout="wide"
# )
#
# with st.sidebar:
#     st.title("Title")
#     st.write("Sidebar Content")
#
# selected = option_menu(
#     None,
#     ["Home", "Upload", "Tasks", 'Settings'],
#     icons=['house', 'cloud-upload', "list-task", 'gear'],
#     menu_icon="cast", default_index=0, orientation="horizontal"
# )

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
