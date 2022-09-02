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
    data_ = data_.drop(columns=["pie"])
    data_ = pd.DataFrame(data_.mean(numeric_only=True)).transpose()
    data_.insert(0, "timestamp", datetime.now())
    data = data_.copy()

    # df = pd.DataFrame(json.loads(msg.payload.decode("utf-8")))
    # timestamp = df["Timestamp"].iloc[0]
    # df = df.drop(columns=["pie", "E_temperature", "E_humidity"])
    # df = pd.DataFrame([df.mean(axis=0)], columns=df.columns)
    # df["Timestamp"].iloc[0] = timestamp
    # data = df


def create_page():
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

    # [開發階段] 設定初始化圖像的閥值
    # [上線階段] 依照所設定的閥值更新圖像
    display_data_length = 180

    # 時間格式
    ISOTIMEFORMAT = "%Y-%m-%d %H:%M:%S"

    # 顯示更新頻率(秒)
    display_freqency = 1.5

    # 連接postgres與設定資料型態(無自定義統一當作TEXT存入資料庫)
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    sql_types = {
        "timestamp": types.DateTime, "ingot": types.FLOAT, "discharge": types.FLOAT, "oil_pressure": types.FLOAT,
        "mould": types.FLOAT, "bucket": types.FLOAT
    }

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

            insert_data_to_postgres(df.iloc[-1:], engine, sql_types)

            # 加入時間軸，因為繪製圖像時不能使用df的index當作x軸資料
            df_have_index = df.copy()
            df_have_index["time(s)"] = df.index * display_freqency

            # 第一個row，擠錠溫度與出料溫度
            ingot, discharge = st.columns(2)

            # 繪製擠錠溫度圖像，透過altait chart可自定義y軸上下限(原生line chart不支援)
            with ingot:
                st.subheader("擠錠溫度 {}".format(round(df_have_index["ingot"].iloc[-1], 2)))
                ingot_chart = alt.Chart(data=df_have_index, autosize="pad").mark_line().encode(
                    x="time(s)",
                    # y=alt.Y("ingot", scale=alt.Scale(domain=[470, 540]))
                    y=alt.Y("ingot", scale=alt.Scale(domain=[100, 650]))
                )
                st.altair_chart(ingot_chart, use_container_width=True)

            # 繪製出料溫度圖像，透過altait chart可自定義y軸上下限(原生line chart不支援)
            with discharge:
                st.subheader("出料溫度 {}".format(round(df_have_index["discharge"].iloc[-1], 2)))
                discharge_chart = alt.Chart(data=df_have_index, autosize="pad").mark_line().encode(
                    x="time(s)",
                    # y=alt.Y("discharge", scale=alt.Scale(domain=[500, 540]))
                    y=alt.Y("discharge", scale=alt.Scale(domain=[100, 650]))
                )
                st.altair_chart(discharge_chart, use_container_width=True)

            # 第二個row，油缸壓力、模具溫度與盛錠筒溫度
            oil_pressure, mould, bucket = st.columns(3)

            # 繪製油缸壓力圖像，透過altait chart可自定義y軸上下限(原生line chart不支援)
            with oil_pressure:
                st.subheader("油缸壓力 {}".format(round(df_have_index["oil_pressure"].iloc[-1], 2)))
                oil_pressure_chart = alt.Chart(data=df_have_index, autosize="pad").mark_line().encode(
                    x="time(s)",
                    # y=alt.Y("oil_pressure", scale=alt.Scale(domain=[10, 300]))
                    y=alt.Y("oil_pressure", scale=alt.Scale(domain=[0, 300]))
                )
                st.altair_chart(oil_pressure_chart, use_container_width=True)

            # 繪製模具溫度圖像，透過altait chart可自定義y軸上下限(原生line chart不支援)
            with mould:
                st.subheader("模具溫度 {}".format(round(df_have_index["mould"].iloc[-1], 2)))
                mould_chart = alt.Chart(data=df_have_index, autosize="pad").mark_line().encode(
                    x="time(s)",
                    # y=alt.Y("mould", scale=alt.Scale(domain=[450, 550]))
                    y=alt.Y("mould", scale=alt.Scale(domain=[100, 650]))
                )
                st.altair_chart(mould_chart, use_container_width=True)

            # 繪製盛錠筒溫度圖像，透過altait chart可自定義y軸上下限(原生line chart不支援)
            with bucket:
                st.subheader("盛錠筒溫度 {}".format(round(df_have_index["bucket"].iloc[-1], 2)))
                bucket_chart = alt.Chart(data=df_have_index, autosize="pad").mark_line().encode(
                    x="time(s)",
                    # y=alt.Y("bucket", scale=alt.Scale(domain=[380, 430]))
                    y=alt.Y("bucket", scale=alt.Scale(domain=[100, 650]))
                )
                st.altair_chart(bucket_chart, use_container_width=True)

            # if refresh > refresh_threshold:
            #     # 第三個row，分別表示當前鋁錠品質與前5錠鋁錠的品質(總共6錠)
            #     # 更新頻率：refresh歸0時
            #     ingots = st.columns(6)
            #
            #     #
            #     quality_text_list = ["當前鋁錠品質", "前一錠品質", "前二錠品質", "前三錠品質", "前四錠品質", "前五錠品質"]
            #
            #     #
            #     quality_df = get_qualities_and_reasons(6)
            #
            #     # with ingots[0]:
            #     #     st.markdown("##### 鋁錠品質")
            #     #     st.write("品質分級")
            #     #     st.write("異常原因")
            #
            #     i = 0
            #     while i < len(ingots):
            #         with ingots[i]:
            #             tem = round(random.randint(480, 530), 2)
            #             delta = round(random.uniform(-5, 5), 2)
            #             st.write(quality_text_list[i])
            #             st.subheader(quality_df["quality"].iloc[i])
            #             st.metric(quality_df["reason"].iloc[i], "{} °C".format(tem), "{} °C".format(delta))
            #             # st.markdown("##### {}".format(quality_text_list[i - 1]))
            #             # st.write(quality_df["quality"].iloc[i - 1])
            #             # st.write()
            #         i = i + 1
            #     i = 0

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
