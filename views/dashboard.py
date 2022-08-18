import time
import streamlit as st
import paho.mqtt.client as mqtt
import json


# data = {}
ingot_data = []
discharge_data = []
oil_pressure_data = []
mould_data = []
bucket_data = []


def on_connect(client, userdata, flags, rc):
    # 連接程序得到響應時所做的動作(印出回應碼rc)
    st.write("Connected with result code " + str(rc))

    # 訂閱/再訂閱
    client.subscribe(st.secrets["mqtt"]["topic"])


def on_message(client, userdata, msg):
    global ingot_data
    global discharge_data
    global oil_pressure_data
    global mould_data
    global bucket_data
    # global data
    # 印出收到的消息
    # st.write(msg.topic + " " + msg.payload.decode("utf-8"))

    data = json.loads(msg.payload.decode("utf-8"))
    ingot_data.append(data["ingot"])
    discharge_data.append(data["discharge"])
    oil_pressure_data.append(data["oil_pressure"])
    mould_data.append(data["mould"])
    bucket_data.append(data["bucket"])

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
    st.markdown("MQTT LOOP START")
    client.connect(st.secrets["mqtt"]["url"], st.secrets["mqtt"]["port"], 5)

    global ingot_data
    global discharge_data
    global oil_pressure_data
    global mould_data
    global bucket_data

    # 可視化
    placeholder = st.empty()
    refresh = 0
    while True:
        with placeholder.container():

            ingot, discharge = st.columns(2)

            ingot.subheader("ingot")
            ingot.line_chart(ingot_data)

            discharge.subheader("discharge")
            discharge.line_chart(discharge_data)

            oil_pressure, mould, bucket = st.columns(3)

            oil_pressure.subheader("oil_pressure")
            oil_pressure.line_chart(oil_pressure_data)

            mould.subheader("mould")
            mould.line_chart(mould_data)

            bucket.subheader("bucket")
            bucket.line_chart(bucket_data)

            refresh = refresh + 1
            if refresh > 20:
                ingot_data = []
                discharge_data = []
                oil_pressure_data = []
                mould_data = []
                bucket_data = []
                refresh = 0
                time.sleep(3)
                # break
        time.sleep(1)
    placeholder.empty()

    # while True:
    #     st.write(f"ingot:{ingot_data}")
    #     time.sleep(1)

    client.loop_stop()
    # client.loop_forever()
    st.markdown("MQTT LOOP END")

