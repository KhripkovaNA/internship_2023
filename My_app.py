import streamlit as st

st.title('Welcome to my app!')
st.subheader('This is my first app using :red[_Streamlit_]. Enjoy :smile:')
link_button = st.button('Click on me \N{winking face}')
if link_button:
    st.info('Feel free to connect with me via [linked-in](https://www.linkedin.com/in/natalia-khripkova-76680b43/?locale=en_US)'
            , icon="ℹ")

st.caption('Innomatics Research Labs Internship - February 2023')