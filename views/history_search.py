import pandas as pd
import streamlit as st
import psycopg2
import random
import numpy as np
from datetime import datetime, timedelta, time


def init():
    st.markdown("### 我是分頁1")


def search():
    # nowtime = datetime.now()
    # datetime_slider = st.slider(
    #     "選擇您的查詢時間範圍：",
    #     min_value=nowtime - timedelta(weeks=1),
    #     max_value=nowtime,
    #     value=(nowtime - timedelta(days=1), nowtime),
    #     format="Y/M/D-HH:MM"
    # )
    # st.write("時間：", datetime_slider)

    col1, col2, col3, col4 = st.columns(4)
    nowtime = datetime.now()
    shift = timedelta(days=1)

    start_date = col1.date_input(
        "選擇起始日期",
        nowtime - shift)
    start_time = col2.time_input(
        "選擇起始時間",
        time(0, 0)
    )
    start = datetime(start_date.year, start_date.month, start_date.day, start_time.hour, start_time.minute)

    end_date = col3.date_input(
        "選擇結束時間",
        nowtime)
    end_time = col4.time_input(
        "選擇結束時間",
        time(0, 0)
    )
    end = datetime(end_date.year, end_date.month, end_date.day, end_time.hour, end_time.minute)

    col1, col2 = st.columns([3, 1])

    col1.markdown(f"## 選擇的時間範圍：{start} ~ {end}")
    submit = col2.button("查詢")
    query = """
        select * from public.vibration 
        where timestamp > '{}'
        and timestamp < '{}'
    """.format(start, end)
    # st.write(query)
    if submit:
        df = query_postgres(query)
        st.write(df)
        st.download_button("檔案下載", df.to_csv(), "data_{}_to_{}.csv".format(start, end))


def query_postgres(query):
    # Initialize connection.
    # Uses st.experimental_singleton to only run once.
    # @st.experimental_singleton
    def init_connection():
        return psycopg2.connect(**st.secrets["postgres"])

    # Perform query.
    # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    @st.experimental_memo(ttl=600)
    def run_query(q):
        with conn.cursor() as cur:
            cur.execute(q)
            return cur.fetchall(), cur.description

    conn = init_connection()

    rows, desc = run_query(query)
    df = pd.DataFrame(rows)
    df.columns = [col.name for col in desc]

    return df

