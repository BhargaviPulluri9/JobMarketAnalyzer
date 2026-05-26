import streamlit as st
from analyzer import extract_skills, analyze_gap

try:
    key = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success(f"✅ Key found! Length: {len(key)}")
except Exception as e:
    st.sidebar.error(f"❌ Secret error: {str(e)}")

st.set_page_config(
    page_title="Job Market Analyzer",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Job Market Analyzer")
st.markdown("Paste a job description and your resume — get instant skill gap analysis powered by AI.")

# Sidebar
with st.sidebar:
    st.header("How it works")
    st.info("1. Paste the job description\n2. Paste your resume text\n3. Click Analyze\n4. Get skill gaps + suggestions")
    st.markdown("**Built with:**")
    st.markdown("- Google Gemini 2.0 Flash")
    st.markdown("- Python + Streamlit")
    st.markdown("- Custom NLP prompts")

# Two column input
col1, col2 = st.columns(2)

with col1:
    st.subheader("Job Description")
    job_desc = st.text_area(
        "Paste the full job posting here",
        height=300,
        placeholder="Copy and paste any job description..."
    )

with col2:
    st.subheader("Your Resume")
    resume = st.text_area(
        "Paste your resume text here",
        height=300,
        placeholder="Copy and paste your resume as plain text..."
    )

# Analyze button
if st.button("🔍 Analyze My Fit", type="primary", use_container_width=True):
    if not job_desc or not resume:
        st.error("Please fill in both fields before analyzing.")
    else:
        with st.spinner("Analyzing with AI..."):
            skills_data = extract_skills(job_desc)
            gap_data = analyze_gap(job_desc, resume)

        st.success("Analysis complete!")
        st.divider()

        # Extract score from wherever Gemini put it
        score_val = "?/10"
        for items in gap_data.values():
            for item in items:
                if "RESUME_SCORE" in str(item):
                    score_val = str(item).replace("RESUME_SCORE:", "").strip()
                    break

        # Extract level from wherever Gemini put it
        level_val = "Unknown"
        for items in skills_data.values():
            for item in items:
                if "EXPERIENCE_LEVEL" in str(item):
                    level_val = str(item).replace("EXPERIENCE_LEVEL:", "").strip()
                    break

        # Clean missing skills — remove score line
        missing_clean = [
            s for s in gap_data.get("MISSING_SKILLS", [])
            if "RESUME_SCORE" not in str(s)
        ]

        # Results in 3 columns
        r1, r2, r3 = st.columns(3)

        with r1:
            st.subheader("✅ Your Matching Skills")
            matches = gap_data.get("MATCHING_SKILLS", [])
            if matches:
                for s in matches:
                    st.markdown(f"- {s}")
            else:
                st.write("No direct matches found")

        with r2:
            st.subheader("❌ Missing Skills")
            if missing_clean:
                for s in missing_clean:
                    st.markdown(f"- {s}")
            else:
                st.write("Great — no major gaps!")

        with r3:
            st.subheader("📊 Resume Score")
            st.metric("Match Score", score_val)
            st.metric("Role Level", level_val)

        st.divider()

        st.subheader("🚀 Top 3 Actionable Suggestions")
        suggestions = gap_data.get("TOP_3_SUGGESTIONS", [])
        for i, s in enumerate(suggestions[:3], 1):
            st.info(f"**{i}.** {s}")

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("💡 Interview Tips")
            tips = gap_data.get("INTERVIEW_TIPS", [])
            for t in tips:
                st.markdown(f"- {t}")

        with col_b:
            st.subheader("📝 Verdict")
            verdict = gap_data.get("OVERALL_VERDICT", [""])
            st.write(" ".join(verdict))

        with st.expander("See full job requirements breakdown"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Required Skills**")
                for s in skills_data.get("REQUIRED_SKILLS", []):
                    st.markdown(f"- {s}")
            with c2:
                st.markdown("**Nice to Have**")
                nice = [
                    s for s in skills_data.get("NICE_TO_HAVE", [])
                    if "EXPERIENCE_LEVEL" not in str(s)
                ]
                for s in nice:
                    st.markdown(f"- {s}")