import streamlit as st
import requests
from google import genai

st.set_page_config(
    page_title="Study Abroad Navigator",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Study Abroad Navigator")
st.write("AI-powered study abroad research assistant")

# --------------------------------
# API KEYS
# --------------------------------

SERPAPI_API_KEY = st.secrets["SERPAPI_API_KEY"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY
)

# --------------------------------
# USER INPUT
# --------------------------------

st.header("🎓 Tell us about your study plans")

country = st.text_input(
    "🌍 Preferred Country",
    placeholder="Example: Germany"
)

course = st.text_input(
    "📚 Course / Degree",
    placeholder="Example: MS in Data Science"
)

budget = st.number_input(
    "💰 Maximum Annual Budget (USD)",
    min_value=0,
    value=20000
)

cgpa = st.number_input(
    "📊 CGPA",
    min_value=0.0,
    max_value=10.0,
    value=8.0,
    step=0.1
)

# --------------------------------
# SEARCH
# --------------------------------

if st.button("🔎 Find Universities"):

    if not country or not course:

        st.warning(
            "Please enter your country and course."
        )

    else:

        # --------------------------------
        # SERPAPI
        # --------------------------------

        with st.spinner("🔍 Searching the web..."):

            query = (
                f"{course} universities in {country} "
                f"tuition fees admission requirements scholarships"
            )

            response = requests.get(
                "https://serpapi.com/search.json",
                params={
                    "engine": "google",
                    "q": query,
                    "api_key": SERPAPI_API_KEY
                },
                timeout=30
            )

            if response.status_code != 200:

                st.error("SerpApi search failed.")

                st.stop()

            data = response.json()

            results = data.get(
                "organic_results",
                []
            )

        # --------------------------------
        # SEARCH RESULTS
        # --------------------------------

        st.header("🔎 Web Research")

        if results:

            for result in results[:5]:

                st.markdown(
                    f"### {result.get('title', 'Unknown')}"
                )

                st.write(
                    result.get(
                        "snippet",
                        "No description available."
                    )
                )

                if result.get("link"):

                    st.write(
                        result["link"]
                    )

        else:

            st.warning(
                "No search results found."
            )

        # --------------------------------
        # PREPARE RESEARCH
        # --------------------------------

        research_text = "\n\n".join(
            [
                f"Title: {r.get('title', '')}\n"
                f"Snippet: {r.get('snippet', '')}\n"
                f"Link: {r.get('link', '')}"
                for r in results[:8]
            ]
        )

        # --------------------------------
        # GEMINI
        # --------------------------------

        with st.spinner(
            "🤖 Gemini is analyzing the results..."
        ):

            prompt = f"""
You are an AI Study Abroad Advisor.

Student information:

Country: {country}
Course: {course}
Maximum annual budget: ${budget}
CGPA: {cgpa}

Web research collected using SerpApi:

{research_text}

Analyze these search results.

Provide:

1. Best universities found
2. Tuition information
3. Admission requirements
4. Scholarship opportunities
5. Universities suitable for the student's budget
6. A simple recommendation
7. Important information the student should verify
   from official university websites

Do not invent information.

If information is unavailable, clearly say so.

Use a clear and student-friendly format.
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            answer = response.text

        # --------------------------------
        # FINAL RESULT
        # --------------------------------

        st.header("🤖 AI Recommendation")

        st.markdown(answer)