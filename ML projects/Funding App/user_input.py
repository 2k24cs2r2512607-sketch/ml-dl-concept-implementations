import streamlit as st
email=st.text_input("Enter email")
password=st.text_input("Enter Password",type="password")
btn=st.button("Login")
gender=st.selectbox("Select gender",['male','other'])
if btn:
    if email=='nistish@gmail.com' and password=='123':
        st.success("login Succes")
        st.write(gender)
        st.balloons()
    else:
        st.error("Login Failed")
 


