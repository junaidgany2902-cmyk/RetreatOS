import streamlit as st
from fpdf import FPDF
from PIL import Image
import tempfile
import base64
import io

# 1. Page Configuration
st.set_page_config(page_title="RetreatOS | Premium Marketplace", page_icon="🌿", layout="wide")

# Custom UI for Branded Profile Cards
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [aria-selected="true"] { color: #D4AF37 !important; border-bottom-color: #D4AF37 !important; }
    
    .branded-card {
        position: relative;
        height: 280px;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 25px;
        color: white;
        background-size: cover;
        background-position: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    .card-overlay {
        position: absolute;
        bottom: 0; left: 0; right: 0; top: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.9) 20%, rgba(0,0,0,0.2) 100%);
        padding: 30px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
    }
    .rating-stars { color: #FFD700; font-size: 18px; margin-bottom: 5px; }
    .badge-premium { background: #D4AF37; padding: 4px 10px; border-radius: 4px; font-size: 10px; font-weight: bold; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

# Helper function to convert image to base64 for background-image
def get_image_base64(image_file):
    if image_file:
        encoded = base64.b64encode(image_file.getvalue()).decode()
        return f"data:image/png;base64,{encoded}"
    return "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&q=80&w=800"

# --- DATA INITIALIZATION ---
if 'network_data' not in st.session_state:
    st.session_state.network_data = [
        {"Name": "Espire Global", "Type": "Company", "Niche": "Luxury Travel", "Location": "Riyadh", "Social": "@espire_global", "Rating": 5, "Img": None, "Bio": "Curating high-end bespoke travel experiences for international HNWIs."},
        {"Name": "Zehra Allibhai", "Type": "Influencer", "Niche": "Wellness", "Location": "Canada", "Social": "@zehraallibhai", "Rating": 5, "Img": None, "Bio": "Global health educator specializing in longevity retreats."},
        {"Name": "Aquila Private Reserve", "Type": "Venue", "Niche": "Safari", "Location": "South Africa", "Social": "@aquilasafari", "Rating": 4.8, "Img": None, "Bio": "Resilience-verified luxury lodge with full solar and water backup."}
    ]

tab_market, tab_join, tab_designer = st.tabs(["🤝 Marketplace", "📝 Join Network", "✨ Pitch Designer"])

# --- TAB 1: THE MARKETPLACE ---
with tab_market:
    st.title("The Global Partnership Hub")
    col_s, col_f = st.columns([2, 1])
    with col_s: search = st.text_input("🔍 Search partners by niche or location...", placeholder="e.g. Wellness, South Africa")
    with col_f: role_filter = st.multiselect("Role Type", ["Influencer", "Venue", "Company"], default=["Influencer", "Venue", "Company"])

    st.divider()

    for p in st.session_state.network_data:
        if (search.lower() in p['Niche'].lower() or search.lower() in p['Location'].lower()) and p['Type'] in role_filter:
            bg_img = get_image_base64(p['Img']) if p['Img'] else "https://images.unsplash.com/photo-1582719478237-af16419af0c2?auto=format&fit=crop&q=80&w=800"
            stars = "★" * int(p['Rating']) + ("½" if p['Rating'] % 1 != 0 else "")
            
            st.markdown(f"""
            <div class="branded-card" style="background-image: url('{bg_img}');">
                <div class="card-overlay">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <span class="badge-premium">{p['Type'].upper()}</span>
                        <div class="rating-stars">{stars} <span style="font-size: 12px; color: white;">({p['Rating']})</span></div>
                    </div>
                    <h2 style="margin: 10px 0 0 0; font-family: serif; letter-spacing: 1px;">{p['Name'].upper()}</h2>
                    <p style="margin: 0; opacity: 0.8; font-size: 14px;">📍 {p['Location']} | 🏷️ {p['Niche']}</p>
                    <p style="margin: 10px 0; font-size: 14px; line-height: 1.4; opacity: 0.9;">{p['Bio']}</p>
                    <div style="font-weight: bold; color: #D4AF37; font-size: 14px;">Connect: {p['Social']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Send Proposal to {p['Name']}", key=p['Name']):
                st.success(f"High-end proposal notification sent to {p['Name']}!")

# --- TAB 2: JOIN NETWORK ---
with tab_join:
    st.title("Register Your Premium Profile")
    st.write("Join the elite network of wellness and luxury travel professionals.")
    
    with st.form("join_premium"):
        col_1, col_2 = st.columns(2)
        with col_1:
            name = st.text_input("Full Business/Public Name")
            role = st.selectbox("I identify as a...", ["Influencer", "Venue", "Company"])
            social = st.text_input("Social Media Handle (Instagram/LinkedIn)")
        with col_2:
            niche = st.text_input("Niche (e.g. Biohacking, Safari, Yoga)")
            location = st.text_input("Base Location")
            brand_img = st.file_uploader("Upload Brand/Profile Background Image", type=["jpg", "png"])
        
        bio = st.text_area("Professional Bio (Keep it editorial and concise)")
        
        if st.form_submit_button("List My Profile"):
            new_member = {
                "Name": name, "Type": role, "Niche": niche, 
                "Location": location, "Social": social, "Bio": bio, 
                "Img": brand_img, "Rating": 5.0 # New users start with 5.0
            }
            st.session_state.network_data.append(new_member)
            st.balloons()
            st.success("Your branded profile is now live!")

# --- TAB 3: PITCH DESIGNER ---
with tab_designer:
    st.info("The pitch generator will pull your profile rating and social links into the finalized PDF to ensure trust with partners.")
    # (Existing PDF generation logic with added rating/social integration)
