# import pandas as pd
import streamlit as st
# # import psycopg2
# from datetime import datetime, timedelta, time
#
#
def init():
    st.markdown("### 歷史查詢初始頁面")
#
#
# def search():
#
#     # 時間格式
#     ISOTIMEFORMAT = "%Y-%m-%d %H:%M:%S"
#
#     # 第一個row，分別表示起始日期、起始時間、結束日期與結束時間
#     col1, col2, col3, col4 = st.columns(4)
#
#     # 取得當前時間，並設定預設的起始與結束時間差
#     nowtime = datetime.now()
#     shift = timedelta(hours=1)
#
#     # 設定起始日期與時間
#     start = nowtime - shift
#     start_date = col1.date_input(
#         "選擇起始日期",
#         start)
#     start_time = col2.time_input(
#         "選擇起始時間",
#         time(start.hour, start.minute)
#     )
#
#     # 將起始時間格式化
#     start = start.strftime(ISOTIMEFORMAT)
#
#     # 設定結束日期與時間
#     end = nowtime
#     end_date = col3.date_input(
#         "選擇結束時間",
#         end)
#     end_time = col4.time_input(
#         "選擇結束時間",
#         time(end.hour, end.minute)
#     )
#
#     # 將結束時間格式化
#     end = end.strftime(ISOTIMEFORMAT)
#
#     # 第二個row，分別表示起始至結束的時間範圍與查詢按鈕，前後者比例為3:1
#     col1, col2 = st.columns([3, 1])
#
#     # 顯示欲查詢的時間範圍與查詢按鈕
#     col1.markdown("### 選擇的時間範圍：{} ~ {}".format(start, end))
#     submit = col2.button("查詢")
#
#     # 設定查詢所需的query
#     query = """
#         select * from public.test
#         where timestamp > '{}'
#         and timestamp < '{}'
#     """.format(start, end)
#
#     # 當按鈕被按下，則進行query動作
#     if submit:
#
#         # 獲取所查詢的資料(dataframe格式)
#         df = query_postgres(query)
#         st.success("查詢成功，資料顯示如下，若需要下載該資料，請按下資料下方的「檔案下載」按鈕！")
#         st.write(df)
#
#         # 按下下載檔案的按鈕後，輸出csv檔
#         st.download_button("檔案下載", df.to_csv(index=False), "data_{}_to_{}.csv".format(start, end))
#
#
# def query_postgres(query):
#
#     # 初始化資料庫連線
#     # 若使用st.experimental_singleton讓該函數只執行一次的話，會導致第二次歷史查詢時報錯
#     def init_connection():
#         return psycopg2.connect(**st.secrets["postgres"])
#
#     # 運行query，並使用st.experimental_memo，當query有變動或數秒鐘後才再執行一次
#     @st.experimental_memo(ttl=600)
#     def run_query(q):
#         with conn.cursor() as cur:
#             cur.execute(q)
#             return cur.fetchall(), cur.description
#
#     # 初始化資料庫連線
#     conn = init_connection()
#
#     # 運行query
#     rows, desc = run_query(query)
#
#     # 將所得資料轉換成dataframe
#     df = pd.DataFrame(rows)
#     df.columns = [col.name for col in desc]
#
#     return df
#
