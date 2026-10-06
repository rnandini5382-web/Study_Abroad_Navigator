import streamlit as st

st.set_page_config(
    page_title="Study Abroad Navigator",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Study Abroad Navigator")
st.write("AI-powered study abroad research assistant")

country = st.text_input("Which country do you want to study in?")
course = st.text_input("What course do you want to study?")
budget = st.number_input(
    "Maximum annual budget (USD)",
    min_value=0,
    value=20000
)

if st.button("🔎 Find Universities"):
    if country and course:
        st.success("Your search request is ready!")
        st.write("Country:", country)
        st.write("Course:", course)
        st.write("Budget:", budget)
    else:
        st.warning("Please enter the country and course.")