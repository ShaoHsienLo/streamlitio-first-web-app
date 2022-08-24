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
    # st.write("Connected with result code " + str(rc))

    # 訂閱/再訂閱
    client.subscribe(st.secrets["mqtt"]["topic"])


def on_message(client, userdata, msg):
    global data

    data = pd.DataFrame.from_records(json.loads(msg.payload.decode("utf-8")), index=[0])


def mqtt_sub():
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
    df = pd.DataFrame(columns=["timestamp", "ingot", "discharge", "oil_pressure", "mould", "bucket"])

    # 建立一個可更新內容的容器
    placeholder = st.empty()

    # [開發階段] 設定初始化圖像的閥值
    # [上線階段] 依照所設定的閥值更新圖像
    refresh = -1
    refresh_threshold = 10

    # 時間格式
    ISOTIMEFORMAT = "%Y-%m-%d %H:%M:%S"

    while True:

        # 建立容器，該容器內的內容會持續更新，需用time.sleep(s)設定更新頻率
        with placeholder.container():

            global data
            refresh = refresh + 1

            # 未從mqtt收到任何資料時，處於待機狀態，避免報錯
            if len(data) == 0:
                continue

            # 當超過所設定的閥值時，清空df，並新增一筆參數平均值給df當作初始化的值，避免圖像顯示出問題
            # 並將refresh歸0，待機數秒，供使用者觀察波形
            if refresh > refresh_threshold:
                st.success("鋁錠擠製完畢!")
                postgres(df)
                # st.success("資料儲存完畢！")
                init_data = [[datetime.now().strftime(ISOTIMEFORMAT), df["ingot"].max(),
                              df["discharge"].max(), df["oil_pressure"].max(), df["mould"].max(),
                              df["bucket"].max()]]
                df = pd.DataFrame(data=init_data, columns=["timestamp", "ingot", "discharge", "oil_pressure",
                                                           "mould", "bucket"], index=[0])
                refresh = 0
                time.sleep(4)
            else:
                st.info("鋁錠擠製中...")
                df = pd.concat([df, data], ignore_index=True)

            # 加入時間軸，因為繪製圖像時不能使用df的index當作x軸資料
            df_have_index = df.copy()
            df_have_index["time(s)"] = df.index

            # 第一個row，擠錠溫度與出料溫度
            ingot, discharge = st.columns(2)

            # 繪製擠錠溫度圖像，透過altait chart可自定義y軸上下限(原生line chart不支援)
            with ingot:
                st.subheader("擠錠溫度")
                ingot_chart = alt.Chart(data=df_have_index, autosize="pad").mark_line().encode(
                    x="time(s)",
                    y=alt.Y("ingot", scale=alt.Scale(domain=[470, 540]))
                )
                st.altair_chart(ingot_chart, use_container_width=True)

            # 繪製出料溫度圖像，透過altait chart可自定義y軸上下限(原生line chart不支援)
            with discharge:
                st.subheader("出料溫度")
                discharge_chart = alt.Chart(data=df_have_index, autosize="pad").mark_line().encode(
                    x="time(s)",
                    y=alt.Y("discharge", scale=alt.Scale(domain=[500, 540]))
                )
                st.altair_chart(discharge_chart, use_container_width=True)

            # 第二個row，油缸壓力、模具溫度與盛錠筒溫度
            oil_pressure, mould, bucket = st.columns(3)

            # 繪製油缸壓力圖像，透過altait chart可自定義y軸上下限(原生line chart不支援)
            with oil_pressure:
                st.subheader("油缸壓力")
                oil_pressure_chart = alt.Chart(data=df_have_index, autosize="pad").mark_line().encode(
                    x="time(s)",
                    y=alt.Y("oil_pressure", scale=alt.Scale(domain=[10, 300]))
                )
                st.altair_chart(oil_pressure_chart, use_container_width=True)

            # 繪製模具溫度圖像，透過altait chart可自定義y軸上下限(原生line chart不支援)
            with mould:
                st.subheader("模具溫度")
                mould_chart = alt.Chart(data=df_have_index, autosize="pad").mark_line().encode(
                    x="time(s)",
                    y=alt.Y("mould", scale=alt.Scale(domain=[450, 550]))
                )
                st.altair_chart(mould_chart, use_container_width=True)

            # 繪製盛錠筒溫度圖像，透過altait chart可自定義y軸上下限(原生line chart不支援)
            with bucket:
                st.subheader("盛錠筒溫度")
                bucket_chart = alt.Chart(data=df_have_index, autosize="pad").mark_line().encode(
                    x="time(s)",
                    y=alt.Y("bucket", scale=alt.Scale(domain=[380, 430]))
                )
                st.altair_chart(bucket_chart, use_container_width=True)

        # 即時數據圖更新頻率(秒)
        time.sleep(1)

    # 迴圈結束後清空(重置)該容器
    placeholder.empty()

    # mqtt連線迴圈結束
    client.loop_stop()


def postgres(df):
    sql_types = {
        "timestamp": types.DateTime, "ingot": types.FLOAT, "discharge": types.FLOAT, "oil_pressure": types.FLOAT,
        "mould": types.FLOAT, "bucket": types.FLOAT
    }
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    try:
        df.to_sql('test', engine, index=False, dtype=sql_types)
    except ValueError as e:
        df.to_sql('test', engine, if_exists="append", index=False, dtype=sql_types)
