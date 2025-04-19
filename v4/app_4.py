# This script is the main application for the AI Blog Generator. 
# It provides a user interface for generating, saving, and viewing blog posts using Streamlit.
import streamlit as st
from blog_generator_4 import generate_blog_post
from retriever import extract_text_from_pdf, extract_text_from_url
from utils import save_blog, list_saved_blogs, load_blog, delete_blog, export_to_pdf, export_to_markdown
from trends import get_serpapi_trends
import os

from datetime import datetime



# Page setup
st.set_page_config(page_title="AI Blog Generator", layout="centered")
st.title("🧠 AI Blog Post Generator")

# Tabs for UX
tabs = st.tabs(["📝 Generate Blog", "📂 Saved Blogs"])

# --- Generate Blog ---
with tabs[0]:
    st.header("Create a New Blog Post")

    with st.form("generate_blog_form"):
        topic = st.text_input("Enter a blog topic")
        tone = st.selectbox("Choose a tone", ["Informative", "Persuasive", "Casual", "Formal"])
        length = st.slider("Length", 0, 5000, 500, step=100)
        language = st.selectbox("Language", ["English", "Spanish", "French"])

        uploaded_pdf = st.file_uploader("Upload PDF for context (optional)", type="pdf")
        url_input = st.text_input("Paste URL for context (optional)")
        
        # Checkbox to make trending keywords optional
        include_keywords = st.checkbox("Fetch Trending Keywords", value=True)

        submitted = st.form_submit_button("Generate")

        if submitted and topic:
            keywords = []
            if include_keywords:
                st.info("🔍 Fetching trending ...")
                keywords = get_serpapi_trends(topic)
                st.success("✅ Trending Keywords fetched:")
            else:
                st.info("🔍 Skipping trends....")

            # Load context from PDF or URL
            context = ""
            if uploaded_pdf:
                st.info("📄 Reading PDF...")
                context = extract_text_from_pdf(uploaded_pdf)
                st.success("✅ PDF context added.")
            elif url_input:
                st.info("🌐 Scraping website...")
                context = extract_text_from_url(url_input)
                st.success("✅ URL context added.")

            # Generate blog
            blog = generate_blog_post(topic, tone, length, language, keywords, context=context)
            st.session_state["blog"] = blog
            st.session_state["topic"] = topic
            st.session_state["keywords"] = keywords
            st.session_state["context"] = context
            st.success("✅ Blog generated successfully!")
        
    if "blog" in st.session_state and "topic" in st.session_state:
        st.text_area("📝 Generated Blog", st.session_state["blog"], height=400)
        
        # --- Save section ---
        with st.form("save_blog_form"):
            save_button = st.form_submit_button("💾 Save Blog")
            if save_button:
                filename = save_blog(
                    st.session_state["topic"],
                    st.session_state["blog"], 
                    {
                        "tone": tone,
                        "length": length,
                        "language": language,
                        "keywords": st.session_state["keywords"],
                        "has_context": bool(st.session_state["context"])
                    },)
                st.success(f"Blog saved as: {filename}")

        # --- Export section ---
        with st.expander("📤 Export Options"):
            col1, col2, col3 = st.columns(3)
                    
            with col1:
                if st.button("⬇️ Export as PDF"):
                    # Generate PDF content in memory
                    from io import BytesIO
                    pdf_buffer = BytesIO()
                    pdf_content = export_to_pdf(st.session_state["topic"], st.session_state["blog"])
                    st.success("PDF generated successfully!")
                    st.download_button(
                        label="Download PDF",
                        data=pdf_content,
                        file_name=f"{st.session_state['topic'].replace(' ', '_').lower()}.pdf",
                        mime="application/pdf",
                    )

            with col2:
                if st.button("⬇️ Export as Markdown"):
                    # Generate Markdown content in memory
                    markdown_content = export_to_markdown(st.session_state["topic"], st.session_state["blog"])
                    st.success("Markdown generated successfully!")
                    st.download_button(
                        label="Download Markdown",
                        data=markdown_content,
                        file_name=f"{st.session_state['topic'].replace(' ', '_').lower()}.md",
                        mime="text/markdown",
                    )
            
            with col3:
                if st.button("⬇️ Export as Text"):
                    # Generate Text content in memory
                    text_content = st.session_state["blog"]
                    st.success("Text file generated successfully!")
                    st.download_button(
                        label="Download Text",
                        data=text_content,
                        file_name=f"{st.session_state['topic'].replace(' ', '_').lower()}.txt",
                        mime="text/plain",
                    )
                

# --- Saved Blogs ---
with tabs[1]:
    st.header("Saved Blogs")
    blogs = list_saved_blogs()

    if not blogs:
        st.info("No blogs saved yet.")
    else:
        selected = st.selectbox("Choose a saved blog to view", blogs)
        if selected:
            blog_data = load_blog(selected)
            st.subheader(f"📄 {blog_data['topic']}")
            st.markdown(blog_data["content"])
            st.caption(f"🕒 Saved on {blog_data['timestamp']}")

            if st.button("🗑 Delete Blog"):
                delete_blog(selected)
                st.warning(f"{selected} deleted. Refresh to update.")