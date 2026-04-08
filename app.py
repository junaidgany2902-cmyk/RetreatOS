import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile
import os
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="RetreatOS | Marketplace", page_icon="🌿", layout="wide")

# Custom UI Styling for a Luxury App Experience
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; border-bottom: 1px solid #eee; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: transparent; font-family: sans-serif; }
    .stTabs [aria-selected="true"] { color: #D4AF37 !important; border-bottom-color: #D4AF37 !important; }
    .partner-card { 
        border: 1px solid #eee; 
        padding: 25px; 
        background: white; 
        border-radius: 4px; 
        margin-bottom: 20px; 
        border-left: 5px solid #D4AF37;
    }
    .badge { padding: 4px 8px; border-radius: 3px; font-size: 10px; font-weight: bold; text-transform: uppercase; }
    .badge-inf { background-color: #E3F2FD; color: #1976D2; }
    .badge-ven { background-color: #F3E5F5; color: #7B1FA2; }
    </style>
""", unsafe_allow_html=True)

# --- DATA INITIALIZATION ---
if 'network_data' not in st.session_state:
    st.session_state.network_data = [
        {"Name": "Zehra Allibhai", "Type": "Influencer", "Niche": "Wellness/Fitness", "Location": "Canada", "Social": "@zehraallibhai", "Bio": "Global health educator specializing in women-only longevity retreats."},
        {"Name": "Aquila Safari", "Type": "Venue", "Niche": "Safari Luxury", "Location": "South Africa", "Social": "@aquilasafari", "Bio": "Award-winning safari lodge with full solar and water resilience."},
        {"Name": "Espire Global", "Type": "Company", "Niche": "Luxury Travel", "Location": "Riyadh", "Social": "@espire_global", "Bio": "Curating high-end bespoke travel experiences for international HNWIs."}
    ]

# 2. Navigation Tabs
tab_market, tab_designer, tab_join = st.tabs(["🤝 Marketplace", "✨ Lookbook Designer", "📝 Join Network"])

# --- TAB 1: MARKETPLACE ---
with tab_market:
    st.title("Global Partnership Network")
    col_s, col_f = st.columns([2, 1])
    with col_s:
        search = st.text_input("🔍 Search partners...", placeholder="Try 'Safari' or 'Wellness'")
    with col_f:
        roles = st.multiselect("Roles", ["Influencer", "Venue", "Company"], default=["Influencer", "Venue", "Company"])

    st.divider()
    
    for p in st.session_state.network_data:
        if (search.lower() in p['Name'].lower() or search.lower() in p['Niche'].lower()) and p['Type'] in roles:
            b_class = "badge-inf" if p['Type'] == "Influencer" else "badge-ven"
            st.markdown(f"""
            <div class="partner-card">
                <span class="badge {b_class}">{p['Type']}</span>
                <h3 style="margin: 10px 0 5px 0;">{p['Name']}</h3>
                <p style="color: #666; font-size: 14px;">📍 {p['Location']} | 🏷️ {p['Niche']}</p>
                <p style="font-size: 15px;">{p['Bio']}</p>
                <p style="color: #D4AF37; font-weight: bold;">{p['Social']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Propose Collaboration to {p['Name']}", key=p['Name']):
                st.success(f"Connection request sent to {p['Name']}!")

# --- TAB 2: LOOKBOOK DESIGNER ---
with tab_designer:
    col_edit, col_prev = st.columns([1, 1], gap="large")
    
    with col_edit:
        st.subheader("Design Your Pitch")
        bg_style = st.selectbox("Document Theme", ["Midnight Slate", "Luxury Cream", "Pure White"])
        accent_color = st.color_picker("Accent Color", "#D4AF37")
        gallery = st.file_uploader("Upload Experience Gallery", type=["jpg", "png"], accept_multiple_files=True)
        
        retreat_name = st.text_input("Retreat Name", "The Winelands Reset")
        target_venue = st.text_input("Target Venue", "Aquila Private Game Reserve")
        vision = st.text_area("Vision Statement", "A 3-day immersive longevity experience.")
        social_link = st.text_input("Social/Web Link", "www.espireglobal.com")
        resilience = st.checkbox("Include Resilience Badge", value=True)

    with col_prev:
        st.subheader("Live Lookbook Preview")
        bg_map = {"Pure White": "#FFFFFF", "Luxury Cream": "#F9F6F0", "Midnight Slate": "#1A1A1A"}
        txt_map = {"Pure White": "#1A1A1A", "Luxury Cream": "#2D2926", "Midnight Slate": "#FFFFFF"}
        
        html_preview = f"""
        <div style='background-color: {bg_map[bg_style]}; color: {txt_map[bg_style]}; padding: 40px; border: 1px solid #eee; min-height: 600px; font-family: serif;'>
            <div style='border-top: 10px solid {accent_color}; margin: -40px -40px 20px -40px;'></div>
            <p style='letter-spacing: 3px; opacity: 0.6; font-size: 10px; font-family: sans-serif;'>B2B PROPOSAL</p>
            <h1 style='font-size: 42px; margin: 0;'>{retreat_name.upper()}</h1>
            <p style='color: {accent_color}; font-style: italic;'>At {target_venue}</p>
            <hr style='opacity: 0.2; margin: 20px 0;'>
            <h5 style='color: {accent_color}; font-family: sans-serif;'>VISION</h5>
            <p style='font-family: sans-serif; font-size: 14px;'>{vision}</p>
            <div style='margin-top: 30px; padding: 15px; border: 1px solid {accent_color}; font-family: sans-serif; font-size: 12px;'>
                {social_link}
            </div>
        </div>
        """
        st.markdown(html_preview, unsafe_allow_html=True)
        
        if st.button("✨ Export Lookbook PDF", use_container_width=True):
            pdf = FPDF()
            pdf.add_page()
            # PDF Logic (Colors)
            r_b, g_b, b_b = int(bg_map[bg_style][1:3], 16), int(bg_map[bg_style][3:5], 16), int(bg_map[bg_style][5:7], 16)
            r_a, g_a, b_a = int(accent_color[1:3], 16), int(accent_color[3:5], 16), int(accent_color[5:7], 16)
            r_t, g_t, b_t = int(txt_map[bg_style][1:3], 16), int(txt_map[bg_style][3:5], 16), int(txt_map[bg_style][5:7], 16)
            
            pdf.set_fill_color(r_b, g_b, b_b)
            pdf.rect(0, 0, 210, 297, 'F')
            pdf.set_fill_color(r_a, g_a, b_a)
            pdf.rect(0, 0, 210, 10, 'F')
            
            pdf.set_text_color(r_t, g_t, b_t)
            pdf.set_y(25)
            pdf.set_font("Helvetica", 'B', 32)
            pdf.multi_cell(0, 15, retreat_name.upper())
            
            # PDF Gallery
            if gallery:
                y_img = pdf.get_y() + 10
                for i, img in enumerate(gallery[:3]):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                        Image.open(img).convert("RGB").save(tmp.name)
                        pdf.image(tmp.name, x=10 + (i*65), y=y_img, w=60)
                        os.unlink(tmp.name)
                pdf.set_y(y_img + 50)

            pdf.ln(10)
            pdf.set_font("Helvetica", 'B', 12)
            pdf.cell(0, 10, "EXECUTIVE VISION", ln=True)
            pdf.set_font("Helvetica", '', 11)
            pdf.multi_cell(0, 7, vision)
            
            st.download_button("📥 Download PDF", data=bytes(pdf.output()), file_name="Proposal.pdf", use_container_width=True)

# --- TAB 3: JOIN NETWORK ---
with tab_join:
    st.title("Join the Network")
    st.write("Create your profile to be found by global luxury partners.")
    with st.form("reg_form"):
        n_name = st.text_input("Business/Public Name")
        n_type = st.selectbox("Role", ["Influencer", "Venue", "Company"])
        n_niche = st.text_input("Niche")
        n_loc = st.text_input("Location")
        n_social = st.text_input("Social Handle")
        n_bio = st.text_area("Professional Bio")
        if st.form_submit_button("Create Profile"):
            st.session_state.network_data.append({"Name": n_name, "Type": n_type, "Niche": n_niche, "Location": n_loc, "Social": n_social, "Bio": n_bio})
            st.success("Profile live in Marketplace!")

st.divider()
st.caption("RetreatOS v2.1")
