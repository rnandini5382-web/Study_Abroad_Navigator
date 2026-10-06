import streamlit as st
import requests
import anthropic

st.set_page_config(
    page_title="Study Abroad Navigator",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Study Abroad Navigator")
st.write("AI-powered study abroad research assistant")

# Get API keys from Streamlit Secrets
SERPAPI_API_KEY = st.secrets["SERPAPI_API_KEY"]
ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]

# Create Claude client
client = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY
)

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

if st.button("🔎 Find Universities"):

    if not country or not course:
        st.warning("Please enter the country and course.")

    else:

        # -----------------------------
        # SERPAPI SEARCH
        # -----------------------------

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

            results = data.get("organic_results", [])

        # -----------------------------
        # SHOW SEARCH RESULTS
        # -----------------------------

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
                    st.write(result["link"])

        else:
            st.warning("No search results found.")

        # -----------------------------
        # CLAUDE ANALYSIS
        # -----------------------------

        with st.spinner("🤖 Claude is analyzing the results..."):

            research_text = "\n\n".join(
                [
                    f"Title: {r.get('title', '')}\n"
                    f"Snippet: {r.get('snippet', '')}\n"
                    f"Link: {r.get('link', '')}"
                    for r in results[:8]
                ]
            )

            prompt = f"""
You are an AI Study Abroad Advisor.

Student information:

Country: {country}
Course: {course}
Maximum annual budget: ${budget}
CGPA: {cgpa}

Web research results:

{research_text}

Analyze the information and provide:

1. Best universities found
2. Tuition information
3. Admission requirements
4. Scholarship opportunities
5. Universities suitable for the student's budget
6. A simple recommendation
7. Important information the student should verify from official university websites

Do not invent information.
Clearly mention when information is unavailable.
"""

            message = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1500,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            answer = message.content[0].text

        # -----------------------------
        # FINAL RESULT
        # -----------------------------

        st.header("🤖 AI Recommendation")

        st.markdown(answer)