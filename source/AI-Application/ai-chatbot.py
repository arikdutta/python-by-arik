import streamlit as st
st.title(
   "AI Chatbot"
)
user_input = st.text_input(
   "Ask Something: "
)
if st.button("Send"):
   st.write(
       f"AI: {user_input}"
   )