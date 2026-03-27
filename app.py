import streamlit as st
import random
from data_engine import build_elite_database, simulate_agent_scan

st.set_page_config(layout="wide", page_title="Autonomous FBA Agent", page_icon="🤖")

# --- CUSTOM BEAUTIFUL CSS INJECTION ---
st.markdown("""
<style>
    /* Dark Theme Core */
    :root {
        --bg-color: #0d1117;
        --card-bg: rgba(22, 27, 34, 0.7);
        --accent-primary: #00e5ff;
        --accent-secondary: #b05bff;
        --text-primary: #c9d1d9;
        --border-color: rgba(0, 229, 255, 0.2);
    }
    
    .stApp { background-color: var(--bg-color); color: var(--text-primary); font-family: 'Inter', sans-serif; }
    
    .glass-card {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 40px rgba(176, 91, 255, 0.2);
        border-color: rgba(176, 91, 255, 0.5);
    }
    
    .card-title { font-size: 1.25rem; font-weight: 700; color: #fff; margin-bottom: 0.5rem; text-decoration: none;}
    .card-title:hover { color: var(--accent-primary); }

    .badge-container { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 15px;}
    .stBadge { padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: bold; }
    .badge-region { background: rgba(255,255,255,0.1); color: var(--text-primary); }
    .badge-source { background: rgba(176,91,255,0.2); border: 1px solid rgba(176,91,255,0.4); color: #e1bfff; }
    
    .metric-grid { display: flex; flex-wrap: wrap; gap: 8px; margin: 15px 0;}
    .metric-chip { 
        background: rgba(0,0,0,0.3); padding: 5px 12px; border-radius: 6px; 
        font-size: 0.8rem; display: flex; align-items: center; gap: 5px; border: 1px solid rgba(255,255,255,0.05);
    }
    .metric-chip .icon { font-size: 1rem; }
    
    /* Terminal Styles */
    .agent-terminal { background: #010409; border: 1px solid var(--border-color); border-radius: 8px; padding: 15px; font-family: monospace; }
    .blinking-cursor { animation: blink 1s step-end infinite; }
    @keyframes blink { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)


# --- STATE MANAGEMENT ---
if 'all_products' not in st.session_state:
    st.session_state.all_products = []
if 'shown_ids' not in st.session_state:
    st.session_state.shown_ids = set()
if 'current_view' not in st.session_state:
    st.session_state.current_view = []
if 'saved_niches' not in st.session_state:
    st.session_state.saved_niches = []
if 'ui_mode' not in st.session_state:
    st.session_state.ui_mode = "dashboard"


# --- RENDER HELPER ---
def render_product_card(prod, col_index):
    # Determine if saved
    is_saved = any(p['id'] == prod['id'] for p in st.session_state.saved_niches)
    
    html = f"""
    <div class="glass-card">
        <a href="{prod['amazonLink']}" target="_blank" class="card-title">{prod['name']}</a>
        <div class="badge-container">
            <span class="stBadge badge-region">{prod['region']}</span>
            <span class="stBadge badge-source">{prod['source']}</span>
        </div>
        <div style="margin-bottom:10px;"><strong style="color:var(--accent-primary); font-size:1.1rem;">Est. Price: {prod['estPrice']}</strong></div>
        
        <p style="font-size: 0.9rem; color: #8b949e;"><strong>Why it wins:</strong> {prod['whyWins']}</p>
        
        <div class="metric-grid">
            <div class="metric-chip"><span class="icon">📦</span> {prod['weight']}</div>
            <div class="metric-chip"><span class="icon">📈</span> {prod['trendType']}</div>
            <div class="metric-chip"><span class="icon">👑</span> {prod['monopolyRisk']}</div>
            <div class="metric-chip"><span class="icon">💲</span> {prod['priceGap']}</div>
            <div class="metric-chip"><span class="icon">✅</span> {prod['categoryRisk']}</div>
            <div class="metric-chip"><span class="icon">🚫</span> AMZ Basics: {prod['amazonBasics']}</div>
            <div class="metric-chip"><span class="icon">💰</span> {prod['netMargin']}</div>
            <div class="metric-chip"><span class="icon">⭐</span> {prod['top10Reviews']}</div>
            <div class="metric-chip"><span class="icon">🎨</span> {prod['variationRisk']}</div>
        </div>
        
        <div style="font-size: 0.85rem; margin-top:15px; display:flex; gap:10px;">
            <span style="background: rgba(255,255,255,0.05); padding: 3px 8px; border-radius: 4px;">Demand: <strong>{prod['demandSignal']}</strong></span>
            <span style="background: rgba(255,255,255,0.05); padding: 3px 8px; border-radius: 4px;">Competition: <strong>{prod['competitionSignal']}</strong></span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    
    # Render interactive save button directly below HTML
    btn_id = f"save_btn_{prod['id']}_{col_index}"
    if is_saved:
        if st.button("💔 Unsave", key=btn_id, use_container_width=True):
            st.session_state.saved_niches = [p for p in st.session_state.saved_niches if p['id'] != prod['id']]
            st.rerun()
    else:
        if st.button("❤️ Save Niche", key=btn_id, type="primary", use_container_width=True):
            st.session_state.saved_niches.append(prod)
            st.rerun()


# --- APP LAYOUT ---
st.sidebar.title("AI Agent Center")

if st.sidebar.button("📊 Dashboard"):
    st.session_state.ui_mode = "dashboard"
    st.rerun()
    
if st.sidebar.button(f"🔖 Saved Niches ({len(st.session_state.saved_niches)})"):
    st.session_state.ui_mode = "saved"
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Agent Memory Core: Active")
st.sidebar.caption("Rules Engine: Strict Overrides Engaged")


if st.session_state.ui_mode == "dashboard":
    st.title("Autonomous FBA AI Agent")
    
    if not st.session_state.current_view:
        st.markdown("""
        <div style="border: 1px solid rgba(0, 229, 255, 0.4); border-radius: 8px; padding: 15px; background: rgba(0, 229, 255, 0.05); margin-bottom:20px;">
            <p style="margin:0; font-weight:bold; color: #00e5ff;">Last Core Scan: 2 Hrs Ago | Target Region: Global Marketplace | Next Cycle: 22 Hrs</p>
        </div>
        """, unsafe_allow_html=True)
        
        agent_placeholder = st.empty()
        
        if st.button("⚙️ Boot Agent & Extract Niches", type="primary"):
            st.session_state.all_products = simulate_agent_scan(agent_placeholder)
            
            # Extract first 25
            batch = st.session_state.all_products[0:25]
            st.session_state.current_view = batch
            for p in batch: st.session_state.shown_ids.add(p['id'])
            st.rerun()
            
    else:
        # Show Current View Results
        st.subheader("Extracted Winning Niches")
        
        cols = st.columns(2)
        for i, prod in enumerate(st.session_state.current_view):
            with cols[i % 2]:
                render_product_card(prod, i)
        
        # Pagination
        st.markdown("---")
        available = [p for p in st.session_state.all_products if p['id'] not in st.session_state.shown_ids]
        
        if len(available) > 0:
            if st.button("Generate Next 25 Products", type="primary", use_container_width=True):
                batch = random.sample(available, min(25, len(available)))
                st.session_state.current_view = batch
                for p in batch: st.session_state.shown_ids.add(p['id'])
                st.rerun()
        else:
            st.error("Memory Exhausted: All 150 unique high-tier items generated. Reboot application to restart cycle.")

elif st.session_state.ui_mode == "saved":
    st.title("Your Curated Vault")
    if len(st.session_state.saved_niches) == 0:
        st.info("You haven't saved any winning products yet!")
    else:
        cols = st.columns(2)
        for i, prod in enumerate(reversed(st.session_state.saved_niches)):
            with cols[i % 2]:
                render_product_card(prod, f"saved_{i}")
