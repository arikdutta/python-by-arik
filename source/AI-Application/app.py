import streamlit as st

st.title("Student information App")

# if st.button("Click Me"):
#    st.write(
#        "Button Clicked"
#    )
input_name = st.text_input("Enter the Name of the Student")
input_course = st.text_input("Enter the Course of the Student")
button_clicked = st.button("Submit")
if button_clicked:
     st.write("You entered:", input_name)
     st.write("You entered:", input_course)
# # user_input = st.slider("Select a value", 1, 100)
# st.write("You selected:", input_text)