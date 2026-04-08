import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile
import os

# 1. Page Configuration
st.set_page_config(page_title="RetreatOS | Lookbook Creator", page_icon="🌿", layout="wide")

# Custom CSS for the Luxury Editor UI (Ensures the app itself looks clean)
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    .stTextArea textarea, .stTextInput input { border-radius: 0px; border: 1px solid #d4af37; }
    .preview-box { border: 1px solid #eee; padding: 50px; min-height: 800px; }
    </style>
""", unsafe_allow_html=True)

# 2. Split-Screen Layout
col_edit, col_prev = st.columns([1, 1], gap="large")

with col_edit:
    st.title("🌿 RetreatOS Lookbook")
    
    with st.expander("🎨 Aesthetic & Theme", expanded=True):
        bg_style = st.selectbox("Background Theme", ["Midnight Slate", "Luxury Cream", "Pure White"])
        accent_color = st.color_picker("Accent Color", "#D4AF37")
        gallery_images = st.file_uploader("Upload Experience Gallery (Multiple)", type=["jpg", "png"], accept_multiple_files=True)
    
    with st.expander("📖 Partnership Details", expanded=True):
        retreat_name = st.text_input("Retreat Name", "The Winelands Reset")
        target_lodge = st.text_input("Target Venue", "Aquila Private Game Reserve")
        host_name = st.text_input("Curator/Agency", "Junaid Gany Luxury")
        vision = st.text_area("The Vision", "A 3-day immersive longevity experience focusing on restoration.")
        instagram = st.text_input("Instagram Handle", "@yourbrand")
        website = st.text_input("Website URL", "www.yourbrand.com")
    
    resilience_check = st.checkbox("Include Resilience Badge", value=True)

# Map background and text colors based on theme
bg_map = {"Pure White": "#FFFFFF", "Luxury Cream": "#F9F6F0", "Midnight Slate": "#1A1A1A"}
text_map = {"Pure White": "#1A1A1A", "Luxury Cream": "#2D2926", "Midnight Slate": "#FFFFFF"}
current_bg = bg_map[bg_style]
current_text = text_map[bg_style]

with col_prev:
    st.title("📝 Lookbook Preview")
    
    # ---------------------------------------------------------
    # CRITICAL: THIS HTML BLOCK MUST BE RENDERED WITH THE FLAG
    # ---------------------------------------------------------
    html_preview = f"""
    <div style='background-color: {current_bg}; color: {current_text}; padding: 50px; border: 1px solid #eee; min-height: 800px; font-family: serif;'>
        <div style='border-top: 15px solid {accent_color}; margin: -50px -50px 30px -50px;'></div>
        <p style='letter-spacing: 5px; opacity: 0.6; font-size: 10px; font-family: sans-serif;'>B2B PARTNERSHIP PROPOSAL</p>
        <h1 style='font-size: 52px; margin: 0; line-height: 0.9;'>{retreat_name.upper()}</h1>
        <p style='font-size: 18px; font-style: italic; color: {accent_color}; margin-top: 10px;'>At {target_lodge}</p>
        
        <div style='margin: 30px 0; border-bottom: 1px solid {accent_color}; opacity: 0.3;'></div>
        
        <h4 style='color: {accent_color}; font-family: sans-serif;'>EXECUTIVE VISION</h4>
        <p style='font-size: 15px; font-weight: 300; line-height: 1.6; font-family: sans-serif;'>{vision}</p>
        
        <div style='display: flex; gap: 10px; margin-top: 25px;'>
            {f"<div style='width: 80px; height: 80px; background: #333; display: flex; align-items: center; justify-content: center; font-size: 9px; color: #666;'>IMAGE 1</div>" if gallery_images else ""}
            {f"<div style='width: 80px; height: 80px; background: #333; display: flex; align-items: center; justify-content: center; font-size: 9px; color: #666;'>IMAGE 2</div>" if len(gallery_images) > 1 else ""}
        </div>
        
        <div style='margin-top: 40px; padding: 20px; border: 1px solid {accent_color}; font-family: sans-serif;'>
            <p style='margin: 0; font-size: 10px; font-weight: bold; color: {accent_color};'>SOCIAL & CONNECT</p>
            <p style='margin: 0; font-size: 14px;'>{instagram} | {website}</p>
        </div>
        
        {f"<div style='margin-top: 20px; background: #2d5a27; color: white; padding: 10px; text-align: center; font-size: 11px; font-family: sans-serif;'>RESILIENCE VERIFIED</div>" if resilience_check else ""}
    </div>
    """
    
    # This is the command that prevents the "Raw HTML" error
    st.markdown(html_preview, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 3. PDF Export Logic
    if st.button("✨ Export High-End PDF", use_container_width=True):
        pdf = FPDF()
        pdf.add_page()
        
        # Theme Colors
        r_bg, g_bg, b_bg = int(current_bg[1:3], 16), int(current_bg[3:5], 16), int(current_bg[5:7], 16)
        r_acc, g_acc, b_acc = int(accent_color[1:3], 16), int(accent_color[3:5], 16), int(accent_color[5:7], 16)
        r_txt, g_txt, b_txt = int(current_text[1:3], 16), int(current_text[3:5], 16), int(current_text[5:7], 16)

        # Set Full Background
        pdf.set_fill_color(r_bg, g_bg, b_bg)
        pdf.rect(0, 0, 210, 297, 'F')
        
        # Header Accent
        pdf.set_fill_color(r_acc, g_acc, b_acc)
        pdf.rect(0, 0, 210, 10, 'F')
        
        # Text
        pdf.set_text_color(r_txt, g_txt, b_txt)
        pdf.set_y(25)
        pdf.set_font("Helvetica", 'B', 36)
        pdf.multi_cell(0, 15, retreat_name.upper())
        
        # Images Grid (PDF Version)
        if gallery_images:
            y_pos = pdf.get_y() + 5
            for i, img_file in enumerate(gallery_images[:3]): 
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                    img = Image.open(img_file).convert("RGB")
                    img.save(tmp.name)
                    pdf.image(tmp.name, x=10 + (i*65), y=y_pos, w=60)
                    os.unlink(tmp.name)
            pdf.set_y(y_pos + 50)

        pdf.ln(10)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 10, "EXECUTIVE VISION", ln=True)
        pdf.set_font("Helvetica", '', 11)
        pdf.multi_cell(0, 7, vision)
        
        # Footer
        pdf.set_y(-40)
        pdf.set_draw_color(r_acc, g_acc, b_acc)
        pdf.rect(10, pdf.get_y(), 190, 20)
        pdf.set_y(pdf.get_y() + 5)
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(0, 5, f"INSTAGRAM: {instagram}  |  WEB: {website}", align='C', ln=True)

        st.download_button("📥 Download Final Lookbook", data=bytes(pdf.output()), file_name=f"{retreat_name}_Proposal.pdf", mime="application/pdf", use_container_width=True)

st.divider()
st.caption("RetreatOS v1.7.2 | Luxury B2B Edition")
