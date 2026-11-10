import streamlit as st
import time
import pandas as pd
st.title("Startup Dashboard")
st.header("I am learning Streamlit")
st.subheader("And I am Loving it!")
st.write("This is a normal text")
st.markdown("""
### My favourite movies
- Race 3
- Humshakals
"""
)
st.code("""
def foo(input):
    return foo**2
x=foo(2)
""")
st.latex('x^2+y^2+10=0')
df=pd.DataFrame({
    'name':['A','B','C'],
    'marks':[2,3,4]
})
st.dataframe(df)
st.metric('Revenue','Rs 3L','3%')
st.json({
    'name':['A','B','C'],
    'marks':[2,3,4]
})
# st.image('web.jpg')
# st.video('task.m4v')
st.sidebar.title("Sidebar")
col1,col2=st.columns(2)
# with col1:
    # st.image('uname.jpg')
# with col2:
    # st.image('djfh.jgp')
st.error("Login Failed")
st.success("Login Successful")
st.info("Info")
st.warning("Warning")
# bar=st.progress(0)
# for i in range(1,101):
#     time.sleep(0.1)
#     bar.progress(i)
email=st.text_input("Enter email")
number=st.number_input("Enter age")
st.date_input("Enter Date")
file=st.file_uploader("Upload CSV")
if file is not None:
    df=pd.read_csv(file)
    st.dataframe(df.describe())
