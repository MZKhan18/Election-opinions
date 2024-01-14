import streamlit as st
i = 0
st.header("testing")
while True:

    if st.button('presss'):
        i = i + 1
    st.write(i)