import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile
import os

# 1. Page Configuration: Wide mode allows for the Split-Screen Editor
st.set_page_config(page_title="RetreatOS | Luxury Editor", page_icon="🌿", layout="wide")

# Custom CSS to give the "App" a high-end, editorial feel
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    .stTextArea textarea, .stTextInput input { border-radius: 0px; border: 1px solid #d4af37; }
    h1, h2, h3 { font-family: 'serif'; color: #1a1a1a; }
    .preview-box { 
        border: 1px solid #eee; 
        padding: 50px; 
        background: white; 
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        min-height: 800px;
    }
    .luxury-line { border-top: 2px solid #d4af37; width: 60px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 2. Split-Screen Layout: 1 Part Editor, 1 Part Live Preview
col_edit, col_prev = st.columns([1, 1], gap="large")

with col_edit:
    st.title("🌿 RetreatOS Editor")
    st.caption("Craft your bespoke B2B partnership proposal.")
    
    with st.expander("🎨 Visual Identity & Branding", expanded=True):
        uploaded_image = st.file_uploader("Hero Image (Lodge or Aesthetic)", type=["jpg", "jpeg", "png"])
        accent_color = st.color_picker("Brand Accent Color", "#D4AF37") # Default to Gold
    
    with st.expander("📖 Content & Strategy", expanded=True):
        retreat_name = st.text_input("Retreat Name", "The Winelands Reset")
        target_lodge = st.text_input("Target Venue", "Aquila Private Game Reserve")
        host_name = st.text_input("Curator/Agency", "Junaid Gany Luxury")
        vision_statement = st.text_area("The Vision", "A 3-day immersive longevity experience focusing on restoration.")
        schedule = st.text_area("Program Highlights", "Day 1: Arrival & Breathwork; Day 2: Cold Plunge & Safari; Day 3: Integration.")
    
    resilience_check = st.checkbox("Apply [Resilience Verified] Certification", value=True)

with col_prev:
    st.title("📝 Live Document Preview")
    
    # This HTML-based Preview simulates the final PDF look in real-time
    with st.container():
        st.markdown(f"""
        <div class='preview-box'>
            <div style='border-top: 12px solid {accent_color}; margin-top: -50px; margin-left: -50px; margin-right: -50px;'></div>
            <p style='letter-spacing: 4px; color: #888; font-size: 11px; margin-top: 30px;'>B2B PARTNERSHIP PROPOSAL</p>
            <h1 style='font-family: serif; font-size: 52px; margin-top: 10px; line-height: 1;'>{retreat_name.upper()}</h1>
            <div class='luxury-line' style='border-top-color: {accent_color};'></div>
            
            <p style='font-style: italic; font-size: 18px; color: #555;'>Exclusive Residency at {target_lodge}</p>
            <p style='font-size: 14px; color: {accent_color}; font-weight: bold;'>Curated by {host_name}</p>
            
            <div style='margin-top: 30px; border-bottom: 1px solid #eee;'></div>
            
            <h4 style='color: {accent_color}; margin-top: 25px;'>EXECUTIVE VISION</h4>
            <p style='font-size: 15px; color: #444; line-height: 1.6;'>{vision_statement}</p>
            
            <h4 style='color: {accent_color}; margin-top: 25px;'>THE PROGRAM</h4>
            <p style='font-size: 15px; color: #444; line-height: 1.6;'>{schedule}</p>
            
            <br><br>
            {f"<div style='background: #f4fbf4; border: 1px solid #2d5a27; padding: 15px; color: #2d5a27; text-align: center; font-weight: bold; font-size: 12px;'>🛡 RESILIENCE VERIFIED: 100% SOLAR & WATER BACKUP COMPLIANT</div>" if resilience_check else ""}
            
            <p style='margin-top: 60px; font-size: 10px; color: #ccc; text-align: center;'>CONFIDENTIAL DOCUMENT | © 2026 {host_name.upper()}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # --- PDF EXPORT LOGIC ---
        if st.button("✨ Finalize & Export Official PDF", use_container_width=True):
            pdf = FPDF()
            pdf.add_page()
            
            # Convert HEX color to RGB for FPDF
            r = int(accent_color[1:3], 16)
            g = int(accent_color[3:5], 16)
            b = int(accent_color[5:7], 16)
            
            # Gold Header Bar
            pdf.set_fill_color(r, g, b)
            pdf.rect(0, 0, 210, 10, 'F')
            
            pdf.ln(20)
            
            # Image Support
            if uploaded_image:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                    img = Image.open(uploaded_image).convert("RGB")
                    img.save(tmp.name)
                    pdf.image(tmp.name, x=25, y=25, w=160)
                    pdf.ln(100) # Jump below image
                    os.unlink(tmp.name)

            # Text Layout
            pdf.set_font("Helvetica", 'B', 32)
            pdf.set_text_color(26, 26, 26)
            pdf.multi_cell(0, 14, retreat_name.upper())
            
            pdf.set_draw_color(r, g, b)
            pdf.line(10, pdf.get_y()+2, 100, pdf.get_y()+2)
            pdf.ln(10)
            
            # Content Blocks
            def add_pdf_section(title, content):
                pdf.set_font("Helvetica", 'B', 10)
                pdf.set_text_color(r, g, b)
                pdf.cell(0, 10, title, ln=True)
                pdf.set_font("Helvetica", '', 10)
                pdf.set_text_color(40, 40, 40)
                pdf.multi_cell(0, 6, str(content))
                pdf.ln(5)

            add_pdf_section("1. EXECUTIVE VISION", vision_statement)
            add_pdf_section("2. THE PROGRAM", schedule)
            
            if resilience_check:
                pdf.set_fill_color(248, 248, 248)
                pdf.set_draw_color(r, g, b)
                pdf.rect(10, pdf.get_y(), 190, 15, 'DF')
                pdf.set_y(pdf.get_y() + 3)
                pdf.set_font("Helvetica", 'B', 9)
                pdf.set_text_color(26, 26, 26)
                pdf.cell(0, 10, "  RESILIENCE COMPLIANT: FULL SOLAR & WATER INFRASTRUCTURE  ", align='C')

            pdf_bytes = bytes(pdf.output())
            st.download_button("📥 Download Final B2B Proposal", data=pdf_bytes, file_name=f"{retreat_name}_Proposal.pdf", mime="application/pdf", use_container_width=True)

st.divider()
st.caption("RetreatOS Luxury v1.6 | Live Editor Mode")
