import time
import altair as alt
import pandas as pd
import psycopg2
import streamlit as st
import paho.mqtt.client as mqtt
import json


def init():
    st.markdown("### 我是戰情看版")


# data = {"ingot": "", "discharge": "", "oil_pressure": "", "mould": "", "bucket": ""}
data = pd.DataFrame()
# ingot_data = []
# discharge_data = []
# oil_pressure_data = []
# mould_data = []
# bucket_data = []


def on_connect(client, userdata, flags, rc):
    # 連接程序得到響應時所做的動作(印出回應碼rc)
    st.write("Connected with result code " + str(rc))

    # 訂閱/再訂閱
    client.subscribe(st.secrets["mqtt"]["topic"])


def on_message(client, userdata, msg):
    # global ingot_data
    # global discharge_data
    # global oil_pressure_data
    # global mould_data
    # global bucket_data
    global data
    # 印出收到的消息
    # st.write(msg.topic + " " + msg.payload.decode("utf-8"))

    data = pd.DataFrame.from_records(json.loads(msg.payload.decode("utf-8")), index=[0])
    st.write(data)
    # ingot_data.append(data["ingot"])
    # discharge_data.append(data["discharge"])
    # oil_pressure_data.append(data["oil_pressure"])
    # mould_data.append(data["mould"])
    # bucket_data.append(data["bucket"])

    # st.write(f"In message:{receive_msg}")
    # visualization(msg.payload.decode("utf-8"))


# def on_log(client, userdata, level, buf):
#     st.write("log: ", buf)


def mqtt_sub():
    # mqtt連線
    client = mqtt.Client(transport=st.secrets["mqtt"]["transport"])
    client.on_connect = on_connect
    client.on_message = on_message
    # client.on_log = on_log
    client.username_pw_set(st.secrets["mqtt"]["username"], st.secrets["mqtt"]["password"])

    client.loop_start()
    client.connect(st.secrets["mqtt"]["url"], st.secrets["mqtt"]["port"], 5)

    ingot_data = []
    discharge_data = []
    oil_pressure_data = []
    mould_data = []
    bucket_data = []
    df = pd.DataFrame(columns=["ingot", "discharge", "oil_pressure", "mould", "bucket"])

    placeholder = st.empty()
    refresh = -1
    while True:
        with placeholder.container():

            global data
            refresh = refresh + 1

            if len(data) == 0:
                continue

            # st.write(f"data:{data}")
            if refresh > 20:
                st.success("鋁錠擠製完畢!")
                df = pd.DataFrame(columns=["ingot", "discharge", "oil_pressure", "mould", "bucket"])
            else:
                st.info("鋁錠擠製中...")
                df = pd.concat([df, data], ignore_index=True)

            df_have_index = df.copy()
            df_have_index["time(s)"] = df.index

            # 第一個row，擠錠溫度、出料溫度
            ingot, discharge = st.columns(2)

            ingot.subheader("擠錠溫度")
            ingot_chart = alt.Chart(data=df_have_index, autosize="pad").mark_line().encode(
                x="time(s)",
                y=alt.Y("ingot", scale=alt.Scale(domain=[470, 540]))
            )
            st.altair_chart(ingot_chart)

            # discharge.subheader("discharge")
            #
            # oil_pressure, mould, bucket = st.columns(3)
            #
            # oil_pressure.subheader("oil_pressure")
            #
            # mould.subheader("mould")
            #
            # bucket.subheader("bucket")

            if refresh > 20:
                refresh = 0
                time.sleep(4)
                # break
        time.sleep(1)
    placeholder.empty()

    # 可視化
    # placeholder = st.empty()
    # refresh = -1
    # while True:
    #     with placeholder.container():
    #
    #         global data
    #         refresh = refresh + 1
    #
    #         if refresh > 20:
    #             ingot_data = []
    #             discharge_data = []
    #             oil_pressure_data = []
    #             mould_data = []
    #             bucket_data = []
    #         else:
    #             ingot_data.append(data.get("ingot"))
    #             discharge_data.append(data.get("discharge"))
    #             oil_pressure_data.append(data.get("oil_pressure"))
    #             mould_data.append(data.get("mould"))
    #             bucket_data.append(data.get("bucket"))
    #
    #         if len(data) == 0:
    #             continue
    #
    #         # 創建altair chart
    #         ingot_alt = alt.Chart(ingot_data).mark_line().encode(
    #             alt.Y("ingot", scale=alt.Scale(zero=False)),
    #             x="生產時間(秒):Q"
    #         )
    #
    #         ingot, discharge = st.columns(2)
    #
    #         ingot.subheader("ingot")
    #         # ingot.line_chart(ingot_data)
    #         ingot.altair_chart(ingot_alt)
    #
    #         discharge.subheader("discharge")
    #         discharge.line_chart(discharge_data)
    #
    #         oil_pressure, mould, bucket = st.columns(3)
    #
    #         oil_pressure.subheader("oil_pressure")
    #         oil_pressure.line_chart(oil_pressure_data)
    #
    #         mould.subheader("mould")
    #         mould.line_chart(mould_data)
    #
    #         bucket.subheader("bucket")
    #         bucket.line_chart(bucket_data)
    #
    #         if refresh > 20:
    #             refresh = 0
    #             st.success("當前鋁錠錠生產結束!!")
    #             time.sleep(4)
    #             # break
    #     time.sleep(1)
    # placeholder.empty()

    # while True:
    #     st.write(f"ingot:{ingot_data}")
    #     time.sleep(1)

    client.loop_stop()
    # client.loop_forever()


def postgres():
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
