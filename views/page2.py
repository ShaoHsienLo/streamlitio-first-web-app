import altair as alt
import numpy as np
import streamlit as st
import pandas as pd
import json


def init():
    st.markdown("### 我是分頁1")


def create_page():
    df = pd.DataFrame.from_records(json.loads('{"a": 1, "b": 2, "c": 3}'), index=[0])
    st.write(df)

    # chart_row = st.empty()
    #
    # for i in range(10):
    #     df = pd.DataFrame(
    #         np.random.randn(100, 3),
    #         columns=['a', 'b', 'c'])
    #
    #     c = alt.Chart(df).mark_circle().encode(
    #         x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
    #
    #     chart_row.altair_chart(c, use_container_width=True)

    # df = pd.DataFrame(
    #     np.random.randn(200, 3),
    #     columns=['a', 'b', 'c'])
    # df["index"] = df.index
    # st.write(df)
    # st.write(len(df))
    # chart = alt.Chart(data=df, autosize="pad").mark_line().encode(
    #     x="index",
    #     y=alt.Y("a", scale=alt.Scale(domain=[-5, 5]))
    # )
    # st.altair_chart(chart)

    # df = pd.DataFrame(
    #     np.random.randn(200, 3),
    #     columns=['a', 'b', 'c'])
    # st.vega_lite_chart(df, {
    #     'mark': {'type': 'circle', 'tooltip': True},
    #     'encoding': {
    #         'x': {'field': 'a', 'type': 'quantitative'},
    #         'y': {'field': 'b', 'type': 'quantitative'},
    #         'size': {'field': 'c', 'type': 'quantitative'},
    #         'color': {'field': 'c', 'type': 'quantitative'},
    #     },
    # })
