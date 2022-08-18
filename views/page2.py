# importing required libraries

import streamlit as st

import time


def init():
    st.markdown("### 我是分頁1")


def create_page():
    # creating a simple 30 seconds countdown using st.empty

    with st.empty():
        i = 5

        while i > 0:
            st.write(f"{i} seconds left")

            time.sleep(1)

            i = i - 1

        st.write("Time's up!!")  # text to display after the countdown ends

    # creating a single element placeholder

    placeholder = st.empty()

    # adding some text into the placeholder

    placeholder.text("Initial text")

    # replacing the initial text with multi-elements

    # with placeholder.container():
    #     st.write("This is element 1")
    #
    #     st.write("This is element 2")

    # clearing all the elements

    placeholder.empty()

