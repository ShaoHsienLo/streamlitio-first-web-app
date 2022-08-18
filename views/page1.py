import pandas as pd
import streamlit as st
import psycopg2
import random
import numpy as np
import time
from datetime import datetime


def init():
    st.markdown("### 我是分頁1")


def test():
    left, right = st.columns(2)

    with left:
        st.markdown("# LEFT")
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c']
        )
        st.write(chart_data)
        st.line_chart(chart_data)

    with right:
        st.markdown("# RIGHT")
        et = st.empty()
        while True:
            with et.container():
                chart_data = pd.DataFrame(
                    np.random.randn(20, 3),
                    columns=['a', 'b', 'c']
                )
                st.write(chart_data)
                st.line_chart(chart_data)
                time.sleep(1)


def create_page():
    st.markdown("我是主頁面。")

    # Initialize connection.
    # Uses st.experimental_singleton to only run once.
    @st.experimental_singleton
    def init_connection():
        return psycopg2.connect(**st.secrets["postgres"])

    # Perform query.
    # Uses st.experimental_memo to only rerun when the query changes or after 10 min.
    @st.experimental_memo(ttl=600)
    def run_query(query):
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall(), cur.description

    conn = init_connection()

    rows, desc = run_query("select * from public.vibration order by timestamp desc limit 20")
    df = pd.DataFrame(rows)
    df.columns = [col.name for col in desc]

    st.write(df)

    time.sleep(2)

    # col1, col2, col3 = st.columns(3)
    # col1.write("擠錠溫度")
    # col1.metric("Temperature", "70 °F", "1.2 °F")
    # col2.metric("Wind", "9 mph", "-8%")
    # col3.metric("Humidity", "86%", "4%")

    # Row B
    # b1, b2, b3, b4 = st.columns(4)
    # b1.metric("Temperature", "70 °F", "1.2 °F")
    # b2.metric("Wind", "9 mph", "-8%")
    # b3.metric("Humidity", "86%", "4%")
    # b4.metric("Humidity", "86%", "4%")



