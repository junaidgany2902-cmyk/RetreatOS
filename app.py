import streamlit as st
from weasyprint import HTML

# 1. Luxury App Header
st.set_page_config(page_title="RetreatOS | Pitch Generator", page_icon="🌿")
st.title("🌿 RetreatOS")
st.subheader("Luxury B2B Pitch Generator")

# 2. Sidebar Inputs (The Fields we generated)
with st.sidebar:
    st.header("Retreat Details")
    retreat_name = st.text_input("Retreat Name", "The Winelands Reset")
    host_name = st.text_input("Host Name", "Junaid Gany")
    vibe = st.selectbox("Editorial Vibe", ["Minimalist Zen", "Rugged Luxury", "Urban Chic"])
    resilience = st.checkbox("Include Resilience Badge (Solar/Water Backup)")

# 3. The "Editorial" Template Logic
# This is where your luxury eye comes in. We use HTML for the layout.
html_template = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital@1&family=Inter:wght@300&display=swap');
    body {{ font-family: 'Inter', sans-serif; padding: 50px; color: #333; }}
    h1 {{ font-family: 'Playfair Display', serif; font-size: 48px; border-bottom: 1px solid #ccc; }}
    .badge {{ color: green; font-weight: bold; border: 1px solid green; padding: 5px; }}
</style>
<body>
    <p>B2B PROPOSAL</p>
    <h1>{retreat_name}</h1>
    <p>Hosted by: {host_name}</p>
    <hr>
    <h3>The Vision</h3>
    <p>A high-end wellness experience designed for the South African market.</p>
    {"<div class='badge'>✓ RESILIENCE CERTIFIED (SOLAR + BOREHOLE)</div>" if resilience else ""}
</body>
"""

# 4. Action Button
if st.button("Generate Luxury Pitch"):
    with st.spinner("Crafting your editorial lookbook..."):
        HTML(string=html_template).write_pdf("pitch.pdf")
        with open("pitch.pdf", "rb") as file:
            st.download_button("Download Your Pitch (PDF)", file, "Luxury_Pitch.pdf")
        st.success("Pitch generated successfully!")
