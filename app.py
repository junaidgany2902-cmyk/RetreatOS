import streamlit as st
from fpdf import FPDF

# 1. Page Configuration
st.set_page_config(page_title="RetreatOS | Luxury B2B", page_icon="🌿", layout="wide")

# 2. Sidebar: Inputs & Monetization
with st.sidebar:
    st.title("🌿 RetreatOS")
    st.info("Build high-end B2B pitches in seconds.")
    
    # --- PAYMENT SECTION ---
    st.subheader("💳 Unlock Premium Export")
    merchant_id = "10000100" 
    payfast_html = f"""
    <form action="https://www.payfast.co.za/eng/process" method="post" target="_blank">
        <input type="hidden" name="merchant_id" value="{merchant_id}">
        <input type="hidden" name="amount" value="350.00">
        <input type="hidden" name="item_name" value="Single Luxury Pitch Export">
        <input type="submit" value="Pay R350 to Export" style="width:100%; background:#000; color:#fff; border:none; padding:10px; cursor:pointer; font-weight:bold;">
    </form>
    """
    st.components.v1.html(payfast_html, height=50)
    st.divider()

    # --- INPUT FIELDS ---
    retreat_name = st.text_input("Retreat Name", "The Winelands Reset")
    host_name = st.text_input("Host/Agency Name", "Junaid Gany Luxury")
    target_lodge = st.text_input("Target Lodge", "Aquila Private Game Reserve")
    resilience_check = st.checkbox("Include Resilience Badge", value=True)
    vision_statement = st.text_area("The Vision", "A 3-day immersive longevity experience.")

# 3. The PDF Generation Logic (Corrected for Streamlit)
def create_pdf(retreat, host, lodge, vision, resilience):
    pdf = FPDF()
    pdf.add_page()
    
    # Luxury Styling
    pdf.set_font("Helvetica", 'B', 16)
    pdf.set_text_color(212, 175, 55) # Gold color
    pdf.cell(0, 10, f"PARTNERSHIP PROPOSAL FOR {lodge.upper()}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Helvetica", 'B', 30)
    pdf.set_text_color(26, 26, 26) 
    pdf.multi_cell(0, 12, retreat)
    
    pdf.ln(5)
    pdf.set_font("Helvetica", '', 14)
    pdf.cell(0, 10, f"Curated by {host}", ln=True)
    
    pdf.ln(20)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 10, "THE VISION", ln=True)
    pdf.set_font("Helvetica", '', 11)
    pdf.multi_cell(0, 8, vision)
    
    if resilience:
        pdf.ln(10)
        pdf.set_fill_color(244, 251, 244)
        pdf.set_draw_color(45, 90, 39)
        pdf.set_text_color(45, 90, 39)
        pdf.cell(0, 12, "  RESILIENCE VERIFIED: 100% SOLAR & WATER BACKUP  ", border=1, ln=True, fill=True)

    # Convert to bytes for Streamlit download
    return bytes(pdf.output())

# 4. App Interface
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### 📝 Preview: {retreat_name}")
    st.markdown(f"**Lodge:** {target_lodge}")
    st.info(vision_statement)

with col2:
    st.markdown("### 🚀 Export")
    # This generates the PDF data once the button is pressed
    if st.button("Generate Pitch File"):
        pdf_bytes = create_pdf(retreat_name, host_name, target_lodge, vision_statement, resilience_check)
        
        # Now the data is in a format Streamlit understands
        st.download_button(
            label="📥 Download Luxury Pitch",
            data=pdf_bytes,
            file_name=f"{retreat_name.replace(' ', '_')}_Pitch.pdf",
            mime="application/pdf"
        )
        st.success("Your pitch is ready!")

st.divider()
st.caption("RetreatOS Luxury v1.1 - No-Code Edition")
