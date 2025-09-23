from pathlib import Path
from typing import List

import streamlit as st


# -----------------------
# Page & Theme Settings
# -----------------------
st.set_page_config(
    page_title="Abhiroop Bhattacharyya | Portfolio",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------
# Utility Functions
# -----------------------
def load_file_bytes(file_path: Path) -> bytes:
    if not file_path.exists():
        return b""
    return file_path.read_bytes()


def inject_global_css():
    """Injects global CSS to enhance visuals and fix scrolling issues."""
    st.markdown(
        """
        <style>
        /* Ensure pages are scrollable */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"], .block-container {
            overflow-y: auto !important;
        }

        /* Layout tuning */
        .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        /* Headings */
        h1, h2, h3, h4 { font-weight: 700; }
        h2 { border-bottom: 1px solid #eaecef; padding-bottom: .25rem; }

        /* Code-like tags used for skill chips */
        .markdown code {
            background: #f4f6f8;
            color: #444;
            border-radius: 14px;
            padding: 2px 8px;
            margin-right: 6px;
            display: inline-block;
        }

        /* Buttons */
        .stButton>button, .stDownloadButton>button, .stLinkButton>button {
            border-radius: 10px;
            padding: .6rem 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,.06);
        }

        /* Containers (approximate styling for st.container) */
        [data-testid="stVerticalBlock"] > div:has([data-testid="stContainer"]),
        [data-testid="stContainer"] {
            border-radius: 12px;
            box-shadow: 0 4px 14px rgba(0,0,0,.06);
            background: white;
        }

        /* Sidebar avatar */
        .sidebar-avatar {
            display: block;
            margin: 0 auto 12px auto;
            width: 120px;
            height: 120px;
            border-radius: 50%;
            object-fit: cover;
            box-shadow: 0 2px 10px rgba(0,0,0,.15);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str | None = None):
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)
    st.divider()


def matches_query(text: str, query: str) -> bool:
    if not query:
        return True
    return query.lower() in text.lower()


def render_card(title: str, body: str, tags: List[str] | None = None, links: List[tuple[str, str]] | None = None):
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.write(body)
        if tags:
            st.markdown(
                " ".join([f"`{t}`" for t in tags])
            )
        if links:
            cols = st.columns(len(links))
            for idx, (label, url) in enumerate(links):
                with cols[idx]:
                    st.link_button(label, url)


# -----------------------
# Sidebar (Navigation + Search)
# -----------------------
with st.sidebar:
    # Inject CSS once at app start
    inject_global_css()

    # Profile image in the sidebar
    profile_img_path = Path("assets/images/profile_picture.png")
    if profile_img_path.exists():
        st.image(str(profile_img_path), width=120)
    st.title("👋 Hi, I'm Abhiroop")
    st.caption("Backend Developer — Aspiring ML & Data Science Engineer")
    st.divider()

    # Global search input
    global_query = st.text_input("Search portfolio", placeholder="Search projects, skills, experience…")

    st.divider()
    st.subheader("Navigate")
    nav = st.radio(
        label="Go to",
        options=[
            "Home",
            "About Me",
            "Skills",
            "Projects",
            "Experience",
            "Certifications",
            "Contact Me",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("**Links**")
    st.link_button("GitHub", "https://github.com/")
    st.link_button("LinkedIn", "https://www.linkedin.com/")


# -----------------------
# Content Sections
# -----------------------
resume_path = Path("assets/resume/Abhiroop_Bhattacharyya_DataScience_Resume.pdf")
resume_bytes = load_file_bytes(resume_path)


def section_home():
    section_header("Home")
    left, right = st.columns([2, 1])
    with left:
        st.markdown("""
        **Abhiroop Bhattacharyya**  
        Backend Developer — Aspiring ML & Data Science Engineer
        """)
        st.write(
            "I build reliable backend systems and increasingly apply ML to create data-driven features."
        )
        if resume_bytes:
            st.download_button(
                label="Download Resume",
                data=resume_bytes,
                file_name=resume_path.name,
                mime="application/pdf",
            )
    with right:
        st.metric("Years Experience", "2+")
        st.metric("Projects", "5+")
        st.metric("Certifications", "3+")


def section_about(query: str):
    content = (
        "I'm a software developer with 3+ years of experience building robust, scalable backend systems, "
        "and I'm now looking to transition into applied data science roles. With an M.Tech in Data Science "
        "and a strong foundation in Python, Django, and REST APIs, I bring solid engineering skills to "
        "data-driven problem-solving.\n\n"
        "Recently, I've been bridging the gap between backend engineering and machine learning—deploying ML "
        "models, designing API-first ML pipelines, and experimenting with tools like LangChain, Hugging Face, "
        "and MLflow.\n\n"
        "I'm also working on diffusion models (SDXL, Flux) and generative AI workflows including text-to-image, "
        "image-to-image, and image-to-video—exploring how cutting-edge models can be applied in real-world "
        "intelligent systems.\n\n"
        "I'm especially interested in opportunities where I can apply data science and AI techniques to solve "
        "complex problems at scale while continuing to grow as an applied AI engineer."
    )
    if not matches_query(content, query):
        return
    section_header("About Me")
    st.write(content)


def render_skill_bar(skill_name: str, percentage: int, experience: str):
    """Render a skill with progress bar and experience in two columns"""
    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown(f"**{skill_name}**")
        st.caption(f"{experience}")
    with col2:
        st.progress(percentage / 100)
        st.caption(f"{percentage}%")

def section_skills(query: str):
    # Define skills with their details
    skills_data = [
        {"name": "Django", "percentage": 90, "experience": "3 years"},
        {"name": "Python", "percentage": 90, "experience": "3 years"},
        {"name": "Software Development", "percentage": 90, "experience": "3 years"},
        {"name": "PostgreSQL", "percentage": 90, "experience": "3 years"},
        {"name": "Scikit-learn", "percentage": 85, "experience": "2 years"},
        {"name": "ETL", "percentage": 85, "experience": "2 years"},
        {"name": "TensorFlow", "percentage": 70, "experience": "1 year"},
        {"name": "FastAPI", "percentage": 40, "experience": "<1 year"},
    ]

    combined_text = " ".join([skill["name"] for skill in skills_data])
    if not matches_query(combined_text, query):
        return

    section_header("Skills", "Tech I use and enjoy")
    
    # Create 2 columns for skills
    col1, col2 = st.columns(2)
    
    # Split skills into two groups
    mid_point = len(skills_data) // 2
    left_skills = skills_data[:mid_point]
    right_skills = skills_data[mid_point:]
    
    # Render left column skills
    with col1:
        for skill in left_skills:
            render_skill_bar(skill["name"], skill["percentage"], skill["experience"])
            st.write("")  # Add some spacing between skills
    
    # Render right column skills
    with col2:
        for skill in right_skills:
            render_skill_bar(skill["name"], skill["percentage"], skill["experience"])
            st.write("")  # Add some spacing between skills


def section_projects(query: str):
    projects = [
        {
            "title": "Credit Risk Predictor",
            "desc": "Streamlit app powered by XGBoost to predict credit default probability.",
            "tags": ["XGBoost", "Streamlit", "ML"],
            "links": [("Repo", "https://github.com/"), ("Live", "https://share.streamlit.io/")],
        },
        {
            "title": "Mall Customer Segmentation",
            "desc": "K-Means clustering with interactive visualizations to explore customer groups.",
            "tags": ["K-Means", "Visualization", "Python"],
            "links": [("Repo", "https://github.com/")],
        },
    ]

    # Filter by search query
    filtered = [
        p for p in projects if matches_query(" ".join([p["title"], p["desc"], " ".join(p["tags"])]), query)
    ]
    if not filtered:
        return

    section_header("Projects", "Interactive showcases")

    # Responsive grid: 3 -> 2 -> 1
    num_cols = 3
    cols = st.columns(num_cols)
    for idx, proj in enumerate(filtered):
        with cols[idx % num_cols]:
            render_card(proj["title"], proj["desc"], proj["tags"], proj["links"])


def section_experience(query: str):
    experiences = [
        {
            "role": "Backend Developer",
            "company": "Divergenic Tech Solutions",
            "period": "2023 – Present",
            "desc": "Built APIs and services, improved reliability and performance.",
        },
        {
            "role": "Backend Developer Intern",
            "company": "Yatra",
            "period": "2022 – 2023",
            "desc": "Contributed to backend modules and integrations.",
        },
    ]

    combined = " ".join([
        f"{e['role']} {e['company']} {e['period']} {e['desc']}" for e in experiences
    ])
    if not matches_query(combined, query):
        return

    section_header("Experience")
    for e in experiences:
        render_card(
            f"{e['role']} — {e['company']}",
            f"{e['period']}\n\n{e['desc']}",
        )


def section_certifications(query: str):
    certs = [
        {
            "name": "100x Applied Generative AI Cohort (Ongoing)",
            "issuer": "100x",
        },
        {
            "name": "Coursera: Python for Data Science, Methodology, Tools",
            "issuer": "Coursera",
        },
    ]

    combined = " ".join([f"{c['name']} {c['issuer']}" for c in certs])
    if not matches_query(combined, query):
        return

    section_header("Certifications")
    for c in certs:
        render_card(c["name"], f"Issuer: {c['issuer']}")


def section_contact():
    section_header("Contact Me")
    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("Your Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Send")
        if submitted:
            if not name or not email or not message:
                st.error("Please fill out all fields.")
            else:
                st.success("Thanks! Your message has been recorded.")
                st.write({"name": name, "email": email, "message": message})
    st.markdown("Connect: [LinkedIn](https://www.linkedin.com/in/abhiroop-bhattacharyya-b3761414b/) | [GitHub](https://github.com/TechMaverickHub) | [Email](mailto:abhiroop1998.dev@gmail.com)")


# -----------------------
# Router
# -----------------------
if nav == "Home":
    section_home()
    section_about(global_query)
    section_skills(global_query)
    section_projects(global_query)
    section_experience(global_query)
    section_certifications(global_query)
elif nav == "About Me":
    section_about(global_query)
elif nav == "Skills":
    section_skills(global_query)
elif nav == "Projects":
    section_projects(global_query)
elif nav == "Experience":
    section_experience(global_query)
elif nav == "Certifications":
    section_certifications(global_query)
elif nav == "Contact Me":
    section_contact()


# Footer
st.markdown("---")
st.caption("© 2025 Abhiroop Bhattacharyya. Built with Streamlit.")


