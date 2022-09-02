import random
import time
import altair as alt
import pandas as pd
import psycopg2
import streamlit as st
import paho.mqtt.client as mqtt
import json
from sqlalchemy import create_engine, types
from datetime import datetime


# 建立一個全域變數，讓函數內可以使用該變數
data = pd.DataFrame()


def init():
    st.markdown("### 戰情看版初始頁面")


def on_connect(client, userdata, flags, rc):
    # 連接程序得到響應時所做的動作(印出回應碼rc)
    st.write("Connected with result code " + str(rc))

    # 訂閱/再訂閱
    client.subscribe(st.secrets["mqtt"]["topic"])


def on_message(client, userdata, msg):
    global data

    # data = pd.DataFrame.from_records(json.loads(msg.payload.decode("utf-8")), index=[0])
    data_ = pd.DataFrame(json.loads(msg.payload.decode("utf-8")))
    data_ = pd.DataFrame(data_.mean(numeric_only=True)).transpose()
    data_ = data_.drop(columns=["pie"])
    data_.insert(0, "timestamp", datetime.now())
    data = data_.copy()


def test():
    # mqtt連線設定
    client = mqtt.Client(transport=st.secrets["mqtt"]["transport"])
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(st.secrets["mqtt"]["username"], st.secrets["mqtt"]["password"])

    # mqtt連線迴圈起始
    client.loop_start()

    # mqtt連線
    client.connect(st.secrets["mqtt"]["url"], st.secrets["mqtt"]["port"], 5)

    # 建立一個存放mqtt即時數據的變數，以下稱df
    df = pd.DataFrame(columns=["timestamp", "ingot", "discharge", "mould", "oil_pressure", "bucket"])

    # 建立一個可更新內容的容器
    placeholder = st.empty()

    # 顯示更新頻率(秒)
    display_freqency = 1

    display_data_length = 5

    while True:

        # 建立容器，該容器內的內容會持續更新，需用time.sleep(s)設定更新頻率
        with placeholder.container():

            global data

            # 未從mqtt收到任何資料時，處於待機狀態，避免報錯
            if len(data) == 0:
                continue

            if not df.empty:
                df = pd.concat([df, data], ignore_index=True)
            else:
                df = data
            df = df.tail(display_data_length)

            st.markdown("# Df:")
            st.write(df)

            try:
                st.write(df.iloc[-1:])
            except Exception as e:
                st.error("Error!")

        # 即時數據圖更新頻率(秒)
        time.sleep(display_freqency)

    # 迴圈結束後清空(重置)該容器
    placeholder.empty()

    # mqtt連線迴圈結束
    client.loop_stop()


def insert_data_to_postgres(df, engine, sql_types):
    try:
        df.to_sql('realtime', engine, index=False, dtype=sql_types)
    except ValueError as e:
        df.to_sql('realtime', engine, if_exists="append", index=False, dtype=sql_types)


def get_qualities_and_reasons(n):
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    conn = engine.connect()
    query = """
        select "quality", "reason" from public.quality order by timestamp desc limit {}
    """.format(n)
    query_ = conn.execute(query)
    df = pd.DataFrame([dict(i) for i in query_])

    return df
