import streamlit as st
from weasyprint import HTML
import base64

# 1. Page Configuration & Aesthetic Setup
st.set_page_config(page_title="RetreatOS | Luxury B2B", page_icon="🌿", layout="wide")

# Custom CSS for the Streamlit UI (not the PDF)
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 0px; background-color: #d4af37; color: white; border: none; }
    .stButton>button:hover { background-color: #b8962e; color: white; }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar: The Monetization & Input Hub
with st.sidebar:
    st.title("🌿 RetreatOS")
    st.info("Monetize your expertise. Build high-end B2B pitches in seconds.")
    
    # --- PAYMENT SECTION ---
    st.subheader("💳 Unlock Premium Export")
    # Replace these with your real PayFast Merchant ID and Key from your dashboard
    merchant_id = "10000100" # Demo ID
    merchant_key = "46f0cd694581a" # Demo Key
    
    # PayFast HTML Button
    payfast_html = f"""
    <form action="https://www.payfast.co.za/eng/process" method="post" target="_blank">
        <input type="hidden" name="merchant_id" value="{merchant_id}">
        <input type="hidden" name="merchant_key" value="{merchant_key}">
        <input type="hidden" name="amount" value="350.00">
        <input type="hidden" name="item_name" value="Single Luxury Pitch Export">
        <input type="submit" value="Pay R350 to Export" style="width:100%; background:#000; color:#fff; border:none; padding:10px; cursor:pointer; font-weight:bold;">
    </form>
    """
    st.components.v1.html(payfast_html, height=50)
    st.caption("Once paid, the 'Generate Pitch' button below will be active.")
    st.divider()

    # --- INPUT FIELDS ---
    retreat_name = st.text_input("Retreat Name", "The Winelands Reset")
    host_name = st.text_input("Host/Agency Name", "Junaid Gany Luxury")
    target_lodge = st.text_input("Target Lodge", "e.g. Aquila Private Game Reserve")
    resilience_check = st.checkbox("Include Resilience Badge", value=True)
    vision_statement = st.text_area("The Vision", "A 3-day immersive longevity experience for high-net-worth professionals.")

# 3. The High-End Editorial HTML Template
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        @page {{ size: A4; margin: 0; }}
        body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; color: #1a1a1a; }}
        
        /* Cover Page */
        .page {{ height: 100vh; padding: 80px; box-sizing: border-box; position: relative; page-break-after: always; }}
        .gold-bar {{ width: 60px; height: 4px; background: #d4af37; margin-bottom: 20px; }}
        .subtitle {{ font-size: 14px; letter-spacing: 5px; text-transform: uppercase; color: #888; margin-bottom: 10px; }}
        h1 {{ font-family: 'Playfair Display', serif; font-size: 64px; margin: 0; line-height: 1.1; }}
        
        /* Content Sections */
        .content-section {{ margin-top: 60px; border-top: 1px solid #eee; padding-top: 40px; }}
        h2 {{ font-family: 'Playfair Display', serif; font-size: 28px; margin-bottom: 20px; }}
        p {{ font-size: 16px; line-height: 1.8; color: #444; font-weight: 300; }}
        
        /* Resilience Badge */
        .badge {{ border: 1px solid #2d5a27; color: #2d5a27; padding: 15px; font-size: 13px; font-weight: 600; display: inline-block; margin-top: 30px; letter-spacing: 1px; }}
        
        .footer {{ position: absolute; bottom: 80px; font-size: 12px; color: #aaa; }}
    </style>
</head>
<body>
    <div class="page">
        <div class="gold-bar"></div>
        <div class="subtitle">Partnership Proposal for {target_lodge}</div>
        <h1>{retreat_name}</h1>
        <p style="font-size: 20px; margin-top: 20px;">Curated by {host_name}</p>
        
        <div class="content-section">
            <h2>The Vision</h2>
            <p>{vision_statement}</p>
        </div>

        {f'<div class="badge">🛡 RESILIENCE VERIFIED: LOAD-SHEDDING & WATER SECURITY COMPLIANT</div>' if resilience_check else ''}

        <div class="footer">
            CONFIDENTIAL & PROPRIETARY | RETREATOS LUXURY NETWORK 2026
        </div>
    </div>
</body>
</html>
"""

# 4. App Main Interface
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Live Preview")
    st.write("---")
    # Displaying a simplified version of the vision in the app for preview
    st.markdown(f"**Retreat:** {retreat_name}")
    st.markdown(f"**Lodge:** {target_lodge}")
    st.info(vision_statement)

with col2:
    st.markdown("### 🚀 Export")
    if st.button("Generate & Download PDF"):
        with st.spinner("Compiling high-end assets..."):
            # Using WeasyPrint to generate the PDF from the HTML string
            pdf_file = HTML(string=html_content).write_pdf()
            
            st.download_button(
                label="📥 Download Luxury Pitch",
                data=pdf_file,
                file_name=f"{retreat_name}_Pitch.pdf",
                mime="application/pdf"
            )
            st.success("Your pitch is ready!")

st.divider()
st.caption("Developed for Junaid Gany - Wellness Retreat OS v1.0")
