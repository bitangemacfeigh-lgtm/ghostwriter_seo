import streamlit as st
import os
from scraper import analyze_url
from generator import generate_aeo_article
from streamlit_extras.add_vertical_space import add_vertical_space
from fpdf import FPDF

# 1. Page Configuration
st.set_page_config(page_title="Ghostwriter SEO Architect", page_icon="✍️", layout="wide")

# 2. PDF Generator Helper (FIXED)
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'SEO Architect Content Export', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(text):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    # Sanitize for latin-1 (standard PDF fonts)
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    # FIX: Ensure it returns bytes for Streamlit
    return bytes(pdf.output())

# 3. CSS Loader
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

def main():
    with st.sidebar:
        st.title("✍️ Ghostwriter v1.0")
        st.info("Strategy: Competitor Hijack Mode")
        add_vertical_space(2)
        if st.button("Reset Session"):
            st.cache_data.clear()
            st.rerun()

    st.title("SEO Content Architect")
    st.write("Target a competitor URL to generate a high-authority 'Content Hijack' cluster.")
    
    target_url = st.text_input("Competitor URL", placeholder="https://competitor.com/their-best-post")

    if st.button("Generate Architecture"):
        if not target_url:
            st.error("Please enter a URL.")
            return

        try:
            with st.status("🔍 Analyzing Competitor Gaps...", expanded=True):
                data = analyze_url(target_url)
                base_topic = data['headings'][0] if data['headings'] else "Industry Strategy"
                
                # Market-Focused Topics
                topics = [
                    f"The 10x Pillar: {base_topic} Mastery",
                    f"Why Competitors Fail at {base_topic} (Gap Analysis)",
                    f"The Future of {base_topic} in 2026"
                ]
            
            for i, topic in enumerate(topics):
                status_msg = "🔥 HIJACKING TOPIC..." if i == 0 else f"Writing Article {i+1}..."
                with st.spinner(status_msg):
                    content = generate_aeo_article(topic, data['content'])
                    
                    label = f"🚀 MASTER HIJACK: {topic}" if i == 0 else f"📖 Article {i+1}: {topic}"
                    
                    with st.expander(label, expanded=(i == 0)):
                        st.markdown(content)
                        st.divider()
                        
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.code(content, language="markdown")
                            st.caption("Copy Markdown")

                        with c2:
                            st.download_button(
                                label="Download .MD",
                                data=content,
                                file_name=f"hijack_{i+1}.md",
                                mime="text/markdown",
                                key=f"md_{i}"
                            )

                        with c3:
                            pdf_bytes = create_pdf(content)
                            st.download_button(
                                label="Download .PDF",
                                data=pdf_bytes,
                                file_name=f"hijack_{i+1}.pdf",
                                mime="application/pdf",
                                key=f"pdf_{i}"
                            )
            
            st.balloons()

        except Exception as e:
            st.error(f"Critical Error: {e}")

if __name__ == "__main__":
    main()
