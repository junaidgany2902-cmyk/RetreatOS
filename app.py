import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile
import os

# 1. Page Configuration
st.set_page_config(page_title="RetreatOS | Luxury B2B", page_icon="🌿", layout="wide")

# 2. Sidebar Inputs
with st.sidebar:
    st.title("🌿 RetreatOS")
    st.header("Visuals")
    # Image uploader for the cover
    uploaded_image = st.file_uploader("Upload Cover Image (Lodge or Hero Shot)", type=["jpg", "jpeg", "png"])
    
    st.header("Proposal Content")
    retreat_name = st.text_input("Retreat Name", "The Winelands Reset")
    host_name = st.text_input("Host/Agency Name", "Junaid Gany Luxury")
    target_lodge = st.text_input("Target Lodge", "Aquila Private Game Reserve")
    vision_statement = st.text_area("The Vision", "A 3-day immersive longevity experience.")
    target_audience = st.text_input("Target Audience", "HNWI Professionals (35-55)")
    marketing_plan = st.text_area("Marketing Reach", "Email list of 5,000 targeted clients.")
    schedule_summary = st.text_area("Schedule Highlights", "Day 1: Arrival; Day 2: Cold Plunge; Day 3: Integration.")
    resilience_check = st.checkbox("Include Resilience Badge", value=True)

# 3. Enhanced Design Logic with Image Handling
def create_luxury_pdf(retreat, host, lodge, vision, audience, marketing, schedule, resilience, image_file):
    pdf = FPDF()
    pdf.add_page()
    
    # --- DESIGN ELEMENT: GOLD TOP BAR ---
    pdf.set_fill_color(212, 175, 55) 
    pdf.rect(0, 0, 210, 10, 'F')
    
    pdf.ln(15)
    
    # --- HERO IMAGE ---
    if image_file is not None:
        # Save uploaded file to a temporary location for FPDF to read
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            img = Image.open(image_file)
            # Convert to RGB to avoid transparency issues in PDF
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(tmp.name)
            # Place image: centered, 160mm wide
            pdf.image(tmp.name, x=25, y=25, w=160)
            pdf.ln(95) # Move cursor below image
            os.unlink(tmp.name) # Clean up temp file
    else:
        pdf.ln(20)

    # --- HEADER ---
    pdf.set_font("Helvetica", 'B', 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, f"B2B PARTNERSHIP PROPOSAL", ln=True)
    
    pdf.set_font("Helvetica", 'B', 32)
    pdf.set_text_color(26, 26, 26)
    pdf.multi_cell(0, 14, retreat.upper())
    
    pdf.set_draw_color(212, 175, 55)
    pdf.line(10, pdf.get_y() + 2, 100, pdf.get_y() + 2)
    pdf.ln(10)
    
    pdf.set_font("Helvetica", 'I', 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, f"Proposed Venue: {lodge}", ln=True)
    pdf.cell(0, 8, f"Curated by {host}", ln=True)
    
    pdf.ln(10)

    # --- CONTENT SECTIONS ---
    def add_section(title, content):
        pdf.set_font("Helvetica", 'B', 10)
        pdf.set_text_color(212, 175, 55)
        pdf.cell(0, 8, title, ln=True)
        pdf.set_font("Helvetica", '', 10)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(0, 6, content)
        pdf.ln(5)

    add_section("1. EXECUTIVE VISION", vision)
    add_section("2. AUDIENCE & REACH", f"Target: {audience}\nStrategy: {marketing}")
    add_section("3. PROGRAMMING", schedule)
    
    # --- RESILIENCE BLOCK ---
    if resilience:
        pdf.set_fill_color(248, 248, 248)
        pdf.set_draw_color(212, 175, 55)
        pdf.rect(10, pdf.get_y(), 190, 15, 'DF')
        pdf.set_y(pdf.get_y() + 3)
        pdf.set_font("Helvetica", 'B', 9)
        pdf.set_text_color(26, 26, 26)
        pdf.cell(0, 10, "  RESILIENCE COMPLIANT: FULL SOLAR & WATER INFRASTRUCTURE  ", align='C')

    return bytes(pdf.output())

# 4. App Interface
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Partnership Preview")
    if uploaded_image:
        st.image(uploaded_image, caption="Selected Hero Shot", width=400)
    st.write(f"**Target:** {target_lodge}")
    st.info(vision_statement)

with col2:
    st.markdown("### 🚀 Export")
    if st.button("Generate Image-Rich Proposal"):
        pdf_bytes = create_luxury_pdf(
            str(retreat_name), str(host_name), str(target_lodge), 
            str(vision_statement), str(target_audience), 
            str(marketing_plan), str(schedule_summary), 
            resilience_check, uploaded_image
        )
        st.download_button(
            label="📥 Download Luxury Proposal",
            data=pdf_bytes,
            file_name=f"{retreat_name.replace(' ', '_')}_Proposal.pdf",
            mime="application/pdf"
        )
