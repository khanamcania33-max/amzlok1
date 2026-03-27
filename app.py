try:
    from ai_analyzer import analyze_product
except:
    def analyze_product(x):
        return "AI temporarily unavailable"
import streamlit as st
from data_engine import generate_products
from scorer import calculate_score
from ai_analyzer import analyze_product
from database import save_product, get_saved

st.set_page_config(layout="wide", page_title="Nexura AI", page_icon="🤖")

st.title("🤖 Nexura AI — Product Intelligence Engine")

# SESSION
if "products" not in st.session_state:
    st.session_state.products = []

# RUN AI
if st.button("🚀 Run AI Scan"):
    with st.spinner("Scanning & Analyzing..."):
        products = generate_products(30)

        for p in products:
            p["score"] = calculate_score(p)

        # Sort by score
        products = sorted(products, key=lambda x: x["score"], reverse=True)

        st.session_state.products = products

# DISPLAY
for p in st.session_state.products:

    with st.container():
        col1, col2 = st.columns([3,1])

        with col1:
            st.subheader(p["name"])
            st.write(f"💰 Price: ${p['price']}")
            st.write(f"[View on Amazon]({p['amazonLink']})")

        with col2:
            st.metric("Score", f"{p['score']}/100")

        # AI Analysis
        if st.button(f"Analyze {p['id']}"):
            analysis = analyze_product(p["name"])
            st.info(analysis)

        # Save
        if st.button(f"Save {p['id']}"):
            save_product(p["name"], p["score"], "Saved manually")
            st.success("Saved!")

        st.markdown("---")

# SAVED
st.sidebar.title("📊 Saved Products")

saved = get_saved()

for name, score in saved:
    st.sidebar.write(f"{name} ({score})")
