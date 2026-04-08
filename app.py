import streamlit as st
from fpdf import FPDF

# 1. Page Configuration
st.set_page_config(page_title="RetreatOS | Luxury B2B", page_icon="🌿", layout="wide")

# 2. Sidebar: Inputs & Monetization
with st.sidebar:
    st.title("🌿 RetreatOS")
    st.info("Build high-end B2B pitches in seconds.")
    
    st.header("Step 1: The Basics")
    retreat_name = st.text_input("Retreat Name", "The Winelands Reset")
    host_name = st.text_input("Host/Agency Name", "Junaid Gany Luxury")
    target_lodge = st.text_input("Target Lodge", "Aquila Private Game Reserve")
    
    st.header("Step 2: The Business Case")
    vision_statement = st.text_area("The Vision", "A 3-day immersive longevity experience focusing on cellular health.")
    target_audience = st.text_input("Target Audience", "HNWI Professionals (35-55)")
    marketing_plan = st.text_area("Marketing Reach", "Email list of 5,000 targeted clients.")
    
    st.header("Step 3: Logistics")
    schedule_summary = st.text_area("Schedule Highlights", "Day 1: Arrival; Day 2: Cold Plunge; Day 3: Integration.")
    resilience_check = st.checkbox("Include Resilience Badge", value=True)

# 3. PDF Generation Logic (Fixed for Unicode/Emojis)
def create_pdf(retreat, host, lodge, vision, audience, marketing, schedule, resilience):
    pdf = FPDF()
    pdf.add_page()
    
    # --- COVER SECTION ---
    pdf.set_font("Helvetica", 'B', 14)
    pdf.set_text_color(212, 175, 55) # Gold
    pdf.cell(0, 10, f"PARTNERSHIP PROPOSAL: {lodge.upper()}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 30)
    pdf.set_text_color(26, 26, 26) 
    pdf.multi_cell(0, 12, retreat)
    
    pdf.set_font("Helvetica", '', 14)
    pdf.cell(0, 10, f"Curated by {host}", ln=True)
    pdf.ln(15)

    # --- SECTION: THE VISION ---
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "1. THE VISION", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 8, vision)
    pdf.ln(5)

    # --- SECTION: AUDIENCE ---
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "2. AUDIENCE & MARKETING", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 8, f"Target: {audience}\nMarketing: {marketing}")
    pdf.ln(5)

    # --- SECTION: SCHEDULE ---
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "3. PRELIMINARY SCHEDULE", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 8, schedule)
    
    # --- RESILIENCE FOOTER (Emoji Removed to avoid Error) ---
    if resilience:
        pdf.ln(15)
        pdf.set_fill_color(244, 251, 244)
        pdf.set_draw_color(45, 90, 39)
        pdf.set_text_color(45, 90, 39)
        pdf.set_font("Helvetica", 'B', 10)
        # Using [ ] instead of Emojis prevents the Encoding Error
        pdf.cell(0, 12, "  [ RESILIENCE VERIFIED: 100% SOLAR & WATER BACKUP COMPLIANT ]  ", border=1, ln=True, fill=True)

    return bytes(pdf.output())

# 4. App Interface
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Partnership Highlights")
    st.write(f"**Host:** {host_name}")
    st.write(f"**Demographic:** {target_audience}")
    with st.expander("View Full Vision"):
        st.write(vision_statement)

with col2:
    st.markdown("### 🚀 Export Pitch")
    if st.button("Generate Final PDF"):
        # Force conversion to standard strings to avoid encoding issues
        pdf_bytes = create_pdf(
            str(retreat_name), 
            str(host_name), 
            str(target_lodge), 
            str(vision_statement), 
            str(target_audience), 
            str(marketing_plan), 
            str(schedule_summary), 
            resilience_check
        )
        st.download_button(
            label="📥 Download Luxury Pitch",
            data=pdf_bytes,
            file_name=f"{retreat_name.replace(' ', '_')}_Pitch.pdf",
            mime="application/pdf"
        )
        st.success("Pitch Ready for Lodge Review!")

st.divider()
st.caption("RetreatOS Luxury v1.3")
