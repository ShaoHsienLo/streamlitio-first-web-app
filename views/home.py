import pandas as pd
import streamlit as st
import psycopg2


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

    # Print results.
    # for row in rows:
    #     st.write(f"{row[0]} has a :{row[1]}:")




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



