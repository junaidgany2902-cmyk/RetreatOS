import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile
import os

# 1. Page Configuration
st.set_page_config(page_title="RetreatOS | Lookbook Creator", page_icon="🌿", layout="wide")

# Custom CSS for the Luxury Editor
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    .stTextArea textarea, .stTextInput input { border-radius: 0px; border: 1px solid #d4af37; }
    .preview-box { border: 1px solid #eee; padding: 50px; min-height: 800px; transition: all 0.3s; }
    </style>
""", unsafe_allow_html=True)

# 2. Split-Screen Layout
col_edit, col_prev = st.columns([1, 1], gap="large")

with col_edit:
    st.title("🌿 RetreatOS Lookbook")
    
    with st.expander("🎨 Aesthetic & Theme", expanded=True):
        bg_style = st.selectbox("Background Theme", ["Pure White", "Luxury Cream", "Midnight Slate"])
        accent_color = st.color_picker("Accent Color", "#D4AF37")
        # Support for multiple images
        gallery_images = st.file_uploader("Upload Experience Gallery (Multiple)", type=["jpg", "png"], accept_multiple_files=True)
    
    with st.expander("📖 Partnership Details", expanded=True):
        retreat_name = st.text_input("Retreat Name", "The Winelands Reset")
        target_lodge = st.text_input("Target Venue", "Aquila Private Game Reserve")
        vision = st.text_area("The Vision", "A bespoke longevity residency.")
        instagram = st.text_input("Instagram Handle", "@yourbrand")
        website = st.text_input("Website URL", "www.yourbrand.com")
    
    resilience_check = st.checkbox("Include Resilience Badge", value=True)

# Map background colors
bg_map = {"Pure White": "#FFFFFF", "Luxury Cream": "#F9F6F0", "Midnight Slate": "#1A1A1A"}
text_map = {"Pure White": "#1A1A1A", "Luxury Cream": "#2D2926", "Midnight Slate": "#FFFFFF"}
current_bg = bg_map[bg_style]
current_text = text_map[bg_style]

with col_prev:
    st.title("📝 Lookbook Preview")
    
    with st.container():
        st.markdown(f"""
        <div class='preview-box' style='background-color: {current_bg}; color: {current_text};'>
            <div style='border-top: 15px solid {accent_color}; margin: -50px -50px 30px -50px;'></div>
            <p style='letter-spacing: 5px; opacity: 0.6; font-size: 10px;'>B2B PARTNERSHIP PROPOSAL</p>
            <h1 style='font-family: serif; font-size: 58px; margin: 0; line-height: 0.9;'>{retreat_name.upper()}</h1>
            <p style='font-size: 20px; font-style: italic; color: {accent_color}; margin-top: 10px;'>At {target_lodge}</p>
            
            <div style='margin: 40px 0; border-bottom: 1px solid {accent_color}; opacity: 0.3;'></div>
            
            <h4 style='color: {accent_color};'>EXECUTIVE VISION</h4>
            <p style='font-size: 16px; font-weight: 300; line-height: 1.8;'>{vision}</p>
            
            <div style='display: flex; gap: 10px; margin-top: 30px;'>
                {"<div style='width: 100px; height: 100px; background: #eee; border: 1px solid #ccc;'>Image 1</div>" if gallery_images else ""}
                {"<div style='width: 100px; height: 100px; background: #eee; border: 1px solid #ccc;'>Image 2</div>" if len(gallery_images) > 1 else ""}
            </div>
            
            <div style='margin-top: 50px; padding: 20px; border: 1px solid {accent_color}; opacity: 0.8;'>
                <p style='margin: 0; font-size: 12px; font-weight: bold;'>SOCIAL & CONNECT</p>
                <p style='margin: 0; font-size: 14px;'>{instagram} | {website}</p>
            </div>
            
            {f"<div style='margin-top: 20px; background: #2d5a27; color: white; padding: 10px; text-align: center; font-size: 11px;'>RESILIENCE VERIFIED</div>" if resilience_check else ""}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✨ Export High-End PDF"):
            pdf = FPDF()
            pdf.add_page()
            
            # Set Background Color
            r_bg, g_bg, b_bg = int(current_bg[1:3], 16), int(current_bg[3:5], 16), int(current_bg[5:7], 16)
            pdf.set_fill_color(r_bg, g_bg, b_bg)
            pdf.rect(0, 0, 210, 297, 'F')
            
            # Accent Header
            r_acc, g_acc, b_acc = int(accent_color[1:3], 16), int(accent_color[3:5], 16), int(accent_color[5:7], 16)
            pdf.set_fill_color(r_acc, g_acc, b_acc)
            pdf.rect(0, 0, 210, 10, 'F')
            
            # Text Coloring
            r_txt, g_txt, b_txt = int(current_text[1:3], 16), int(current_text[3:5], 16), int(current_text[5:7], 16)
            pdf.set_text_color(r_txt, g_txt, b_txt)
            
            pdf.set_y(25)
            pdf.set_font("Helvetica", 'B', 40)
            pdf.multi_cell(0, 15, retreat_name.upper())
            
            # Images Grid
            if gallery_images:
                y_pos = pdf.get_y() + 10
                for i, img_file in enumerate(gallery_images[:3]): # Cap at 3 for layout
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                        img = Image.open(img_file).convert("RGB")
                        img.save(tmp.name)
                        pdf.image(tmp.name, x=10 + (i*65), y=y_pos, w=60)
                        os.unlink(tmp.name)
                pdf.set_y(y_pos + 50)

            pdf.ln(10)
            pdf.set_font("Helvetica", 'B', 12)
            pdf.cell(0, 10, "THE VISION", ln=True)
            pdf.set_font("Helvetica", '', 11)
            pdf.multi_cell(0, 7, vision)
            
            # Footer Socials
            pdf.set_y(-40)
            pdf.set_draw_color(r_acc, g_acc, b_acc)
            pdf.rect(10, pdf.get_y(), 190, 20)
            pdf.set_y(pdf.get_y() + 5)
            pdf.set_font("Helvetica", 'B', 10)
            pdf.cell(0, 5, f"INSTAGRAM: {instagram}  |  WEB: {website}", align='C', ln=True)

            st.download_button("📥 Download Final Lookbook", data=bytes(pdf.output()), file_name="Lookbook.pdf", use_container_width=True)
