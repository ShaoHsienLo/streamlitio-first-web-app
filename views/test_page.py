import streamlit as st


def test():
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container():
            st.markdown("<h2 style='text-align: center; color: white;'>A級</h2>",
                        unsafe_allow_html=True)

    with col2:
        st.markdown("OK")

    with col3:
        st.markdown("NOT OK")
