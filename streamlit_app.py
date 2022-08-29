import streamlit as st
from views import dashboard, history_search, wang_tsung, hourm_eng, test_page
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide", page_title="Dashboard")

# 加入css
# with open('style.css') as f:
#     st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

# 多頁面導航欄設置
# tab0, tab1, tab2 = st.tabs(["戰情看板", "歷史查詢", "其他測試[開發中]"])
#
# with tab0:
#     dashboard.init()
#
# with tab1:
#     history_search.search()
#
# with tab2:
#     page2.init()

# 多頁面測邊欄設置
menu = ["戰情看板", "歷史查詢", "旺欉戰情看版", "宏英戰情看版[開發中]", "測試網頁"]
with st.sidebar:
    selected = option_menu(
        menu_title="頁面總攬",
        options=menu,
        icons=None,
        menu_icon="menu-down",
        default_index=2
    )

if selected == "戰情看板":
    dashboard.init()
elif selected == "歷史查詢":
    history_search.init()
elif selected == "旺欉戰情看版":
    wang_tsung.mqtt_sub()
elif selected == "宏英戰情看版[開發中]":
    hourm_eng.init()
elif selected == "測試網頁":
    test_page.test()

