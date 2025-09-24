from pathlib import Path
from typing import List

import streamlit as st
import streamlit.components.v1 as components
import base64

# -----------------------
# Page & Theme Settings
# -----------------------
st.set_page_config(
    page_title="Abhiroop Bhattacharyya | Portfolio",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
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
        html, body {
            height: 100%;
            overflow-y: auto !important;
            scroll-behavior: smooth;
        }
        [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"], .block-container {
            overflow-y: auto !important;
            overflow-x: visible !important;
        }

        /* Ensure anchored sections have some top margin when scrolled to */
        #home, #about, #projects, #skills, #contact {
            scroll-margin-top: 80px;
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
    # st.divider()


def insert_anchor(anchor_id: str):
    st.markdown(f'<div id="{anchor_id}"></div>', unsafe_allow_html=True)


def matches_query(text: str, query: str) -> bool:
    if not query:
        return True
    return query.lower() in text.lower()


def render_card(title, desc, tags, links, image=None, impact=None):
    # Card display with image, tags, links, and impact
    with st.container(border=True):
        if image:
            st.image(image, use_container_width=True)
        st.markdown(f"**{title}**")
        st.write(desc)
        tag_str = " ".join([
            f"<span style='background:#21ba45;color:#fff;border-radius:6px;padding:2px 8px; margin-right:4px;'>{t}</span>"
            for t in tags
        ])
        st.markdown(tag_str, unsafe_allow_html=True)
        link_cols = st.columns(len(links))
        for idx, (label, url) in enumerate(links):
            with link_cols[idx]:
                st.link_button(label, url)
        if impact:
            st.markdown(f"<b>Impact:</b> {impact}", unsafe_allow_html=True)



# -----------------------
# Global CSS + Top Navigation
# -----------------------
inject_global_css()

# Resume (used in header and Home)
resume_path = Path("assets/resume/Abhiroop_Bhattacharyya_DataScience_Resume.pdf")
resume_bytes = load_file_bytes(resume_path)

# Simple header menu
if "nav" not in st.session_state:
    st.session_state["nav"] = "Home"

section_from_query = None
try:
    section_from_query = (st.query_params.get("section") or "").strip().lower()
except Exception:
    section_from_query = None

map_to_title = {
    "home": "Home",
    "about": "About",
    "projects": "Projects",
    "skills": "Skills",
    "contact": "Contact",
}
if section_from_query in map_to_title:
    st.session_state["nav"] = map_to_title[section_from_query]

def set_nav(target_title: str):
    st.session_state["nav"] = target_title
    try:
        st.query_params["section"] = target_title.lower()
    except Exception:
        pass

menu_cols = st.columns([1, 1, 1, 1, 1])
if menu_cols[0].button("Home", use_container_width=True):
    set_nav("Home")
if menu_cols[1].button("About", use_container_width=True):
    set_nav("About")
if menu_cols[2].button("Projects", use_container_width=True):
    set_nav("Projects")
if menu_cols[3].button("Skills", use_container_width=True):
    set_nav("Skills")
if menu_cols[4].button("Contact", use_container_width=True):
    set_nav("Contact")

nav = st.session_state["nav"]
global_query = ""


# Navigation helpers for CTA buttons
def go_projects():
    try:
        st.query_params["section"] = "projects"
    except Exception:
        pass
    st.session_state["nav"] = "Projects"


def go_contact():
    try:
        st.query_params["section"] = "contact"
    except Exception:
        pass
    st.session_state["nav"] = "Contact"


# -----------------------
# Content Sections
# -----------------------

def section_home():
    section_header("Home")
    hero = st.container(border=True)
    with hero:
        col_img, col_text = st.columns([1, 2], gap="large")

        with col_img:
            profile_img_path = Path("assets/images/profile_picture.png")
            if profile_img_path.exists():
                with open(profile_img_path, "rb") as image_file:
                    encoded = base64.b64encode(image_file.read()).decode()
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; justify-content: center; height: 100%;">
                        <img src="data:image/png;base64,{encoded}"
                        style='width:100%; max-width: 280px; aspect-ratio:1/1; border-radius:50%; box-shadow:0 4px 24px rgba(0,0,0,.18); margin:40px auto;' />
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with col_text:
            st.markdown(
                """
                ## Abhiroop Bhattacharyya  
                *Backend Developer → Applied ML & Data Science*
                """
            )
            st.write(
                "I craft robust backend systems and build data-driven features powered by ML. I enjoy shipping reliable APIs, optimizing data flows, and applying AI pragmatically to real problems."
            )
            st.markdown(
                """
                #### Key Highlights  
                - 🚀 Reduced API latency by 30% migrating Node.js → Django REST  
                - 🗄️ Built RBAC, PostgreSQL/Mongo integrations, and S3-backed data workflows  
                - 🤖 Exploring LLM apps, ML pipelines, and generative workflows
                """
            )
            st.caption("**Core Technologies:**")
            st.markdown(
                """
                <span style="background-color:#e5e5e5;padding:3px 10px;border-radius:6px;">Python</span>
                <span style="background-color:#e5e5e5;padding:3px 10px;border-radius:6px;">Django</span>
                <span style="background-color:#e5e5e5;padding:3px 10px;border-radius:6px;">REST APIs</span>
                <span style="background-color:#e5e5e5;padding:3px 10px;border-radius:6px;">PostgreSQL</span>
                <span style="background-color:#e5e5e5;padding:3px 10px;border-radius:6px;">Scikit-learn</span>
                <span style="background-color:#e5e5e5;padding:3px 10px;border-radius:6px;">ETL</span>
                """,
                unsafe_allow_html=True,
            )
            cta1, cta2 = st.columns([1, 1])
            with cta1:
                st.button("📂 View Projects", use_container_width=True, on_click=go_projects)
            with cta2:
                st.button("📬 Get in Touch", use_container_width=True, on_click=go_contact)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("👨‍💻 Years Experience", "2+")
    with m2:
        st.metric("🛠️ Projects", "5+")
    with m3:
        st.metric("🎓 Certifications", "3+")


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
    section_header("About")
    # Resume download beside About
    if resume_bytes:
        top_cols = st.columns([3, 1])
        with top_cols[1]:
            st.download_button(
                label="Download Resume",
                data=resume_bytes,
                file_name=resume_path.name,
                mime="application/pdf",
                use_container_width=True,
            )
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
        "links": [("Repo", "https://github.com/TechMaverickHub/credit-risk-predictor-streamlit")],
        "image": "assets/images/credit_risk.jpg",
        "impact": "Can be used by fintech clubs, educators, and data science learners for demo or analysis."
    },
    {
        "title": "Mall Customer Segmentation",
        "desc": "K-Means clustering with interactive visualizations to explore customer groups.",
        "tags": ["K-Means", "Visualization", "Python"],
        "links": [("Repo", "https://github.com/TechMaverickHub/Mall-Customer-Segmentation-using-K-Means-Clustering")],
        "image": "assets/images/mall_customer.jpg",
        "impact": "Can be used by marketing teams and students to visualize or analyze customer segments."
    },
    {
        "title": "100x-LLM-Week2 PDF Chatbot Frontend",
        "desc": "Streamlit frontend for an interactive PDF chatbot powered by FastAPI backend.",
        "tags": ["Streamlit", "FastAPI", "LLM"],
        "links": [("Repo", "https://github.com/TechMaverickHub/100x-LLM-week2-pdf-chatbot-ui")],
        "image": "assets/images/pdf_chatbot.jpg",
        "impact": "Can be used by product teams, students, or info workers needing fast PDF Q&A."
    }
    ]


    # Filter by search query
    filtered = [
        p for p in projects if matches_query(" ".join([p["title"], p["desc"], " ".join(p["tags"])]), query)
    ]
    if not filtered:
        return

    section_header("Projects", "Interactive showcases")

    # Responsive grid: 3 -> 2 -> 1
    # Responsive grid: 3 -> 2 -> 1
    num_cols = 3
    cols = st.columns(num_cols)
    for idx, proj in enumerate(filtered):
        with cols[idx % num_cols]:
            render_card(
                proj["title"], proj["desc"], proj["tags"], proj["links"], proj.get("image"), proj.get("impact")
            )


def section_experience(query: str):
    experiences = [
        {
            "role": "Backend Developer",
            "company": "Divergenic Tech Solutions",
            "period": "Jul 2023 – Present",
            "desc": [
                "Migrated legacy Node.js APIs to Django REST and redesigned endpoints, reducing API response times by 30% and improving client dashboards.",
                "Optimized database queries and refactored endpoints, enhancing performance and scalability.",
                "Integrated PostgreSQL and MongoDB, implemented RBAC, and configured AWS S3 storage for secure, scalable multiuser chart sharing.",
                "Designed end-to-end dashboard features with monitoring and role-based access to support production use.",
            ],
        },
        {
            "role": "Backend Developer Intern",
            "company": "Yatra",
            "period": "Jun 2022 – Jun 2023",
            "desc": [
                "Built a Spring AOP-based logging system to improve monitoring and audits.",
                "Tracked request/response data and performance metrics, reducing response analysis time by 25%.",
                "Enabled real-time method call tracking, improving debugging efficiency by 30%.",
                "Improved system reliability during peak traffic, minimizing downtime of critical services.",
            ],
        },
    ]


    def desc_to_text(desc):
        if isinstance(desc, list):
            return " ".join(desc)
        return str(desc)

    combined = " ".join([
        f"{e['role']} {e['company']} {e['period']} {desc_to_text(e['desc'])}" for e in experiences
    ])
    if not matches_query(combined, query):
        return

    section_header("Experience")
    for e in experiences:
        # Build markdown body allowing bullet points
        if isinstance(e["desc"], list):
            bullets = "\n".join([f"- {item}" for item in e["desc"]])
            body = f"{e['period']}\n\n{bullets}"
        else:
            body = f"{e['period']}\n\n{e['desc']}"

        render_card(
            f"{e['role']} — {e['company']}",
            body,
        )


def section_certifications(query: str):
    certs = [
        {
            "name": "100x Applied Generative AI Cohort (Ongoing)",
            "issuer": "100x",
        },
        {
            "name": "Python for Data Science",
            "issuer": "Coursera",
        },
        {
            "name": "Data Science Methodology",
            "issuer": "Coursera",
        },
        {
            "name": "Tools for Data Science",
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
    section_header("Contact")
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
# Single-page layout: render all sections in order
# -----------------------
insert_anchor("home")
section_home()

insert_anchor("about")
section_about(global_query)

insert_anchor("projects")
section_projects(global_query)

insert_anchor("skills")
section_skills(global_query)

insert_anchor("contact")
section_contact()

# Smooth scroll to selected section after render
target_map = {
    "Home": "home",
    "About": "about",
    "Projects": "projects",
    "Skills": "skills",
    "Contact": "contact",
}
target_id = target_map.get(nav)
if target_id:
    components.html(
        f"""
        <script>
        (function() {{
          function scrollNow() {{
            var el = window.parent ? window.parent.document.getElementById('{target_id}') : document.getElementById('{target_id}');
            if (!el) {{ el = document.getElementById('{target_id}'); }}
            if (el) {{ el.scrollIntoView({{behavior: 'smooth', block: 'start'}}); }}
          }}
          setTimeout(scrollNow, 100);
        }})();
        </script>
        """,
        height=0,
    )


# Footer
st.markdown("---")
st.caption("© 2025 Abhiroop Bhattacharyya. Built with Streamlit.")


