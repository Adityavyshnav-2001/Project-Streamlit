import streamlit as st
import uuid
from datetime import date, timedelta

# ─────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Intl PA/DM Automation",
    page_icon="🟦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# DARK MODE CORPORATE CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* ── FONTS ── */
    @import url('https://fonts.googleapis.com/css2?family=Helvetica+Neue:wght@400;600;700&display=swap');

    /* ── REMOVE TOP WHITESPACE ── */
    .block-container {
        padding-top: 1rem !important; /* Force content up */
        padding-bottom: 5rem !important;
    }
    header {
        visibility: hidden; /* Hides the default Streamlit header hamburger menu for cleaner look */
    }

    /* ── GLOBAL DARK THEME ── */
    .stApp {
        background-color: #0E1117; /* Very Dark Background */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #FAFAFA;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 700;
    }
    
    p, div, label, span {
        color: #E0E0E0; /* Light Grey Text */
    }

    /* ── HEADER ── */
    .main-header {
        background: linear-gradient(90deg, #00175A 0%, #00338D 100%); /* Amex Blue Gradient */
        padding: 1.5rem 2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border: 1px solid #334E68;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .main-header h1 {
        font-size: 1.8rem;
        margin-bottom: 0.2rem;
    }
    .main-header p {
        color: #B3C5E6 !important;
        font-size: 0.9rem;
    }

    /* ── CARDS ── */
    .card {
        background-color: #181B21; /* Dark Slate Card */
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #2D3139;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
    }
    .card-header {
        color: #4299E1 !important; /* Bright Blue Title */
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
        border-bottom: 1px solid #2D3139;
        padding-bottom: 0.8rem;
    }

    /* ── INPUT FIELDS (Dark Mode) ── */
    /* Target text inputs, selects, date pickers, text areas */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div, .stNumberInput input, .stDateInput input, .stTextArea textarea {
        background-color: #0E1117 !important;
        border: 1px solid #2D3139 !important;
        color: #FFFFFF !important;
        border-radius: 4px;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #4299E1 !important;
        box-shadow: 0 0 0 1px #4299E1 !important;
    }
    /* Selectbox dropdown menu text color */
    div[data-baseweb="popover"] {
        background-color: #181B21;
    }
    div[data-baseweb="menu"] {
        background-color: #181B21;
    }
    div[role="option"] {
        color: white;
    }

    /* ── BUTTONS ── */
    .stButton > button {
        background-color: #006FCF; /* Bright Blue */
        color: white !important;
        border: none;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        border-radius: 4px;
    }
    .stButton > button:hover {
        background-color: #0056a3;
    }
    /* Secondary Button Override */
    button[kind="secondary"] {
        background-color: transparent !important;
        border: 1px solid #4A5568 !important;
        color: #E2E8F0 !important;
    }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #181B21;
        border: 1px solid #2D3139;
        border-bottom: none;
        color: #A0AEC0;
        padding: 10px 20px;
        border-radius: 6px 6px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #006FCF !important;
        color: white !important;
        border-color: #006FCF;
    }

    /* ── CHIPS / BADGES ── */
    .offer-chip {
        display: inline-block;
        background-color: #2C5282;
        color: #EBF8FF !important;
        border: 1px solid #2B6CB0;
        padding: 5px 12px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    .segment-chip {
        display: inline-block;
        background-color: #2D3748;
        color: #CBD5E0 !important;
        border: 1px solid #4A5568;
        padding: 3px 10px;
        border-radius: 4px;
        font-size: 0.8rem;
        margin-right: 6px;
    }

    /* ── INFO BOX ── */
    .info-box {
        background-color: #1A202C;
        border-left: 4px solid #4299E1;
        color: #E2E8F0;
        padding: 1rem;
        border-radius: 4px;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    /* ── FOOTER ── */
    .footer {
        text-align: center;
        color: #718096;
        font-size: 0.75rem;
        padding-top: 2rem;
        margin-top: 2rem;
        border-top: 1px solid #2D3139;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE MANAGEMENT
# ─────────────────────────────────────────────
if "offers" not in st.session_state:
    st.session_state.offers = []
if "active_offer_idx" not in st.session_state:
    st.session_state.active_offer_idx = None

def add_offer():
    offer_id = f"OFR-{str(uuid.uuid4())[:8].upper()}"
    st.session_state.offers.append({
        "offer_id": offer_id,
        "segments": [f"SEG-{str(uuid.uuid4())[:6].upper()}"],
        "offer_name": "",
        "offer_end_type": "Static",
        "offer_end_date": date.today() + timedelta(days=90),
        "rolling_days": 30,
    })

def add_segment(offer_idx):
    seg_id = f"SEG-{str(uuid.uuid4())[:6].upper()}"
    st.session_state.offers[offer_idx]["segments"].append(seg_id)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>International PA/DM Automation</h1>
    <p>Campaign Management & Audience Targeting System</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# NAVIGATION
# ─────────────────────────────────────────────
main_tabs = st.tabs([
    "Campaign Details",
    "Offers & Segments",
    "Targeting Rules",
    "Exclusions",
    "Delivery"
])

# ─────────────────────────────────────────────
# TAB 1: CAMPAIGN DETAILS
# ─────────────────────────────────────────────
with main_tabs[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">📋 Campaign Overview</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        business_group = st.selectbox("Business Group", ["-- Select --", "GCS", "GNS", "Consumer", "Commercial"], index=0)
        request_our = st.text_input("Requestor ID (OUR)", placeholder="e.g. 12345678")
    with col2:
        market = st.selectbox("Market Region", ["-- Select --", "United Kingdom (LICC)", "Australia (AAP)", "Mexico (Maya)", "Canada"])
        campaign_name = st.text_input("Campaign Name", placeholder="e.g. 2024 Q1 Platinum Acquisition")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        owner_email = st.text_input("Campaign Owner Email", placeholder="first.last@aexp.com")
    with col4:
        cost_center = st.text_input("Cost Center / Billing Code", placeholder="e.g. 9988-7766")

    st.markdown("<br>", unsafe_allow_html=True)
    campaign_description = st.text_area("Campaign Objective & Description", height=100, placeholder="Define the primary goal of this campaign...")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB 2: OFFERS & SEGMENTS
# ─────────────────────────────────────────────
with main_tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">🎯 Offer Configuration</div>', unsafe_allow_html=True)
    
    col_top_1, col_top_2 = st.columns([4, 1])
    with col_top_1:
        st.markdown("Configure specific offers and attach segments. Multiple offers can be associated with a single campaign.")
    with col_top_2:
        st.button("＋ New Offer", on_click=add_offer, use_container_width=True)

    if st.session_state.offers:
        st.write("---")
        chips_html = ""
        for o in st.session_state.offers:
            chips_html += f'<span class="offer-chip">{o["offer_id"]}</span>'
        st.markdown(chips_html, unsafe_allow_html=True)
        
        offer_options = [f"{o['offer_id']} - {o.get('offer_name', 'Untitled')}" for o in st.session_state.offers]
        selected_offer_str = st.selectbox("Select Offer to Edit", offer_options)
        oidx = offer_options.index(selected_offer_str)
        offer = st.session_state.offers[oidx]

        st.markdown("<br>", unsafe_allow_html=True)
        otabs = st.tabs(["Details", "Card Product", "Timeline"])
        
        with otabs[0]:
            c1, c2 = st.columns(2)
            with c1:
                offer["offer_name"] = st.text_input("Offer Name", value=offer["offer_name"], key=f"on_{oidx}")
                st.selectbox("Offer Objective", ["Acquisition", "Loyalty", "Cross-Sell", "Upgrade"], key=f"obj_{oidx}")
            with c2:
                st.selectbox("Channel", ["Direct Mail", "Email", "Telemarketing", "Digital"], key=f"ch_{oidx}")
                st.text_input("Creative Code", key=f"cc_{oidx}")

            st.markdown("#### Associated Segments")
            seg_display = ""
            for s in offer["segments"]:
                seg_display += f'<span class="segment-chip">{s}</span>'
            st.markdown(seg_display, unsafe_allow_html=True)
            st.button(f"Add Segment", on_click=add_segment, args=(oidx,), key=f"btn_seg_{oidx}")

        with otabs[1]:
            c1, c2 = st.columns(2)
            with c1:
                st.multiselect("Consumer Cards", ["Platinum", "Gold", "Green", "Blue Cash"], key=f"pc_{oidx}")
            with c2:
                st.multiselect("Corporate Cards", ["Business Platinum", "Business Gold", "Corp Green"], key=f"pb_{oidx}")

        with otabs[2]:
            c1, c2 = st.columns(2)
            with c1:
                offer["offer_end_type"] = st.radio("Expiration Logic", ["Fixed Date", "Rolling Window"], horizontal=True, key=f"exp_{oidx}")
            with c2:
                if offer["offer_end_type"] == "Fixed Date":
                    st.date_input("Expiration Date", value=offer["offer_end_date"], key=f"date_{oidx}")
                else:
                    st.number_input("Rolling Days", value=offer["rolling_days"], key=f"roll_{oidx}")

    else:
        st.markdown('<div class="info-box">No offers created yet. Click <b>+ New Offer</b> to begin.</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB 3: TARGETING
# ─────────────────────────────────────────────
with main_tabs[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">🏷️ Audience Targeting</div>', unsafe_allow_html=True)
    
    t_tabs = st.tabs(["Demographics", "Spend Behavior", "Hierarchy"])
    
    with t_tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            st.multiselect("Cardholder Status", ["Active", "Cancelled", "Suspended"], default=["Active"])
            st.multiselect("Tenure", ["< 1 Year", "1-5 Years", "5+ Years"])
        with c2:
            st.text_area("Postal Code Inclusion", placeholder="Enter postcodes...", height=100)
    
    with t_tabs[1]:
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox("Spend Activity (Last 12m)", ["All", "Active Spenders", "Inactive"])
        with c2:
            st.selectbox("Industry (SIC)", ["All", "Travel", "Retail", "Services"])
    
    with t_tabs[2]:
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Corporate ID (CID) List", placeholder="e.g. 0000123456")
        with c2:
            st.multiselect("Hierarchy Level", ["BCA", "ICA", "MCA"])

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB 4: EXCLUSIONS
# ─────────────────────────────────────────────
with main_tabs[3]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">🚫 Exclusion Rules</div>', unsafe_allow_html=True)
    
    st.markdown("##### Mandatory Suppressions")
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.checkbox("Deceased", value=True, disabled=True)
    with col_m2:
        st.checkbox("Fraud / Collections", value=True, disabled=True)
    with col_m3:
        st.checkbox("Regulatory / DNC", value=True, disabled=True)
    
    st.divider()
    
    st.markdown("##### Optional Suppressions")
    col_o1, col_o2, col_o3 = st.columns(3)
    with col_o1:
        st.checkbox("Recent Contact (<30 days)")
    with col_o2:
        st.checkbox("Low Engagement Score")
    with col_o3:
        st.checkbox("Cross-border Restricted")
        
    st.text_area("Custom Exclusion List (IDs)", placeholder="Paste specific account numbers to exclude...", height=80)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAB 5: DELIVERY
# ─────────────────────────────────────────────
with main_tabs[4]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">📦 Data Delivery</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("Delivery Method", ["SFTP", "S3 Bucket", "Email", "API"])
        st.selectbox("File Format", ["CSV", "Fixed Width", "JSON", "Excel"])
    with c2:
        st.date_input("Scheduled Extraction")
        st.text_input("Notification Emails", placeholder="email@aexp.com")
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER / ACTIONS
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

col_actions_1, col_actions_2, col_actions_3 = st.columns([3, 1, 1])

with col_actions_1:
    st.markdown("""
    <div style="font-size: 0.8rem; color: #718096; margin-top: 10px;">
    <b>Note:</b> "Generate Counts" triggers an async query. Results will be emailed.
    </div>
    """, unsafe_allow_html=True)

with col_actions_2:
    st.button("Save Draft", use_container_width=True)

with col_actions_3:
    if st.button("Generate Counts", type="primary", use_container_width=True):
        st.toast("Query submitted! Job ID: JB-998822", icon="✅")

st.markdown("""
<div class="footer">
    International PA/DM Automation Platform • Internal Use Only
</div>
""", unsafe_allow_html=True)