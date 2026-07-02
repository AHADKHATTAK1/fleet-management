from __future__ import annotations

from datetime import date
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()



st.set_page_config(page_title="HAJI BARKAT KHAN JADOON GOODS TRANSPORT", layout="wide", initial_sidebar_state="expanded")


SHIPMENTS = [
    {"id": "WB-48213", "client": "Northbridge Foods", "origin": "Long Beach, CA", "dest": "Reno, NV", "status": "in transit", "eta": "2:40 PM", "progress": 0.62, "driver": "Maria Okafor", "vehicle": "TRK-0731"},
    {"id": "WB-48190", "client": "Calder Steel Co.", "origin": "Gary, IN", "dest": "Detroit, MI", "status": "delayed", "eta": "11:15 AM", "progress": 0.41, "driver": "Ricardo Vasquez", "vehicle": "TRK-0559"},
    {"id": "WB-48177", "client": "Verde Pharma", "origin": "Memphis, TN", "dest": "Atlanta, GA", "status": "delivered", "eta": "Delivered 8:52 AM", "progress": 1.0, "driver": "Sungmin Park", "vehicle": "TRK-0416"},
    {"id": "WB-48241", "client": "Hallstrom Furniture", "origin": "High Point, NC", "dest": "Columbus, OH", "status": "scheduled", "eta": "6:05 PM", "progress": 0.0, "driver": "Jamal Bell", "vehicle": "TRK-0820"},
]

STOCK = [
    {"sku": "PLT-1180", "item": "Standard pallets (48x40)", "warehouse": "Reno DC", "qty": 412, "reorder": 150, "unit": "pcs"},
    {"sku": "FUEL-DSL", "item": "Diesel reserve", "warehouse": "Detroit Yard 3", "qty": 88, "reorder": 200, "unit": "gal"},
    {"sku": "PKG-STR1", "item": "Strapping rolls", "warehouse": "Reno DC", "qty": 36, "reorder": 50, "unit": "rolls"},
    {"sku": "TIRE-22R", "item": "Tires 22.5R (drive axle)", "warehouse": "Columbus Hub", "qty": 14, "reorder": 12, "unit": "pcs"},
    {"sku": "COLD-GEL", "item": "Cold-chain gel packs", "warehouse": "Atlanta Hub", "qty": 540, "reorder": 300, "unit": "pcs"},
    {"sku": "PPE-GLV", "item": "Loading gloves (L)", "warehouse": "Reno DC", "qty": 22, "reorder": 40, "unit": "pairs"},
]

RECEIVING = [
    {"id": "GRN-3081", "supplier": "Premier Pallet Supply", "date": "Jun 28", "status": "received", "items": 3, "value": 4120},
    {"id": "GRN-3082", "supplier": "Continental Tire Distributors", "date": "Jun 29", "status": "partial", "items": 5, "value": 9860},
    {"id": "GRN-3083", "supplier": "ColdPack Industries", "date": "Jun 30", "status": "pending", "items": 2, "value": 2310},
    {"id": "GRN-3079", "supplier": "FuelCo Bulk Services", "date": "Jun 26", "status": "received", "items": 1, "value": 18450},
]

RECEIVING_LINES = {
    "GRN-3081": [
        {"name": "Standard pallets (48x40)", "ordered": 500, "received": 500},
        {"name": "Strapping rolls", "ordered": 60, "received": 60},
        {"name": "Corner protectors", "ordered": 1000, "received": 1000},
    ],
    "GRN-3082": [
        {"name": "Tires 22.5R (drive axle)", "ordered": 20, "received": 12},
        {"name": "Wheel balancing weights", "ordered": 200, "received": 200},
    ],
    "GRN-3083": [
        {"name": "Cold-chain gel packs", "ordered": 800, "received": 0},
        {"name": "Insulated liners", "ordered": 150, "received": 0},
    ],
    "GRN-3079": [{"name": "Diesel reserve", "ordered": 2000, "received": 2000}],
}

TRANSACTIONS = [
    {"id": "TXN-9001", "type": "income", "desc": "Freight payment - Northbridge Foods", "date": "Jun 30", "amount": 6200, "category": "Client payment", "owner": "finance@waybill.local"},
    {"id": "TXN-9002", "type": "expense", "desc": "Diesel refuel - TRK-0731", "date": "Jun 30", "amount": 410, "category": "Fuel", "owner": "maria@waybill.local"},
    {"id": "TXN-9003", "type": "expense", "desc": "Toll - I-80 corridor", "date": "Jun 30", "amount": 38, "category": "Toll", "owner": "maria@waybill.local"},
    {"id": "TXN-9004", "type": "expense", "desc": "Driver payout - M. Okafor", "date": "Jun 29", "amount": 980, "category": "Payroll", "owner": "finance@waybill.local"},
    {"id": "TXN-9005", "type": "income", "desc": "Freight payment - Verde Pharma", "date": "Jun 29", "amount": 4750, "category": "Client payment", "owner": "finance@waybill.local"},
    {"id": "TXN-9006", "type": "expense", "desc": "Tire replacement - Columbus Hub", "date": "Jun 28", "amount": 1240, "category": "Maintenance", "owner": "ricardo@waybill.local"},
    {"id": "TXN-9007", "type": "expense", "desc": "Warehouse lease - Reno DC", "date": "Jun 27", "amount": 5200, "category": "Facilities", "owner": "finance@waybill.local"},
]

STAFF = [
    {"name": "Maria Okafor", "email": "maria@waybill.local", "role": "Driver", "access": "Staff", "status": "active", "initials": "MO"},
    {"name": "Ricardo Vasquez", "email": "ricardo@waybill.local", "role": "Driver", "access": "Staff", "status": "active", "initials": "RV"},
    {"name": "Sungmin Park", "email": "sungmin@waybill.local", "role": "Driver", "access": "Staff", "status": "active", "initials": "SP"},
    {"name": "Jamal Bell", "email": "jamal@waybill.local", "role": "Dispatcher", "access": "Staff", "status": "active", "initials": "JB"},
    {"name": "Elena Cho", "email": "elena@waybill.local", "role": "Warehouse Lead", "access": "Staff", "status": "suspended", "initials": "EC"},
    {"name": "David Reyes", "email": "david@waybill.local", "role": "Operations Manager", "access": "Admin", "status": "active", "initials": "DR"},
]

STATUS_META = {
    "in transit": ("In transit", "#FF8A3D", "rgba(255,138,61,0.12)"),
    "delayed": ("Delayed", "#FF5C5C", "rgba(255,92,92,0.12)"),
    "delivered": ("Delivered", "#3DDC97", "rgba(61,220,151,0.12)"),
    "scheduled": ("Scheduled", "#8B93A7", "rgba(139,147,167,0.12)"),
    "received": ("Received", "#3DDC97", "rgba(61,220,151,0.12)"),
    "partial": ("Partial", "#FF8A3D", "rgba(255,138,61,0.12)"),
    "pending": ("Pending", "#8B93A7", "rgba(139,147,167,0.12)"),
    "active": ("Active", "#3DDC97", "rgba(61,220,151,0.12)"),
    "suspended": ("Suspended", "#FF5C5C", "rgba(255,92,92,0.12)"),
}


def money(value: int | float) -> str:
    return f"${value:,.0f}"


def badge(status: str) -> str:
    label, color, bg = STATUS_META.get(status, STATUS_META["pending"])
    dot_html = ""
    if status == "in transit":
        dot_html = '<span class="status-dot dot-transit"></span>'
    elif status == "delayed":
        dot_html = '<span class="status-dot dot-delayed"></span>'
    elif status == "pending" or status == "partial":
        dot_html = '<span class="status-dot dot-pending"></span>'
    elif status in ("delivered", "received", "active"):
        dot_html = '<span class="status-dot dot-active"></span>'
    return f'<span class="badge" style="color:{color} !important;background:{bg} !important;display:inline-flex;align-items:center;gap:6px;">{dot_html}{label}</span>'


def css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

        :root {
          --bg: #07111f;
          --panel: rgba(13, 21, 38, 0.88);
          --panel-strong: rgba(17, 27, 47, 0.95);
          --line: rgba(142, 160, 201, 0.16);
          --text: #edf2ff;
          --muted: #97a3c4;
          --accent: #ff8a3d;
        }

        /* Typography overrides */
        .stApp, .stApp button, .stApp input, .stApp select, .stApp textarea, .stApp [data-testid="stMarkdownContainer"] {
          font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        .mono {
          font-family: 'JetBrains Mono', monospace !important;
        }

        .stApp {
          background:
            radial-gradient(circle at top left, rgba(255, 138, 61, 0.16), transparent 28%),
            radial-gradient(circle at top right, rgba(61, 220, 151, 0.12), transparent 24%),
            linear-gradient(180deg, #07111f 0%, #0b1324 46%, #070d17 100%);
          color: var(--text) !important;
        }

        /* Custom cards structure */
        .waybill-card {
          border: 1px solid var(--line);
          background: var(--panel-strong);
          border-radius: 24px;
          padding: 1.25rem 1.5rem;
          margin-bottom: 1rem;
          box-shadow: 0 12px 40px rgba(0, 0, 0, 0.22);
          transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .waybill-card:hover {
          border-color: rgba(142, 160, 201, 0.26);
        }

        /* Force high contrast text on Streamlit elements */
        .stApp [data-testid="stMarkdownContainer"] p, 
        .stApp [data-testid="stMarkdownContainer"] span:not(.badge),
        .stApp [data-testid="stMarkdownContainer"] li {
          color: var(--text) !important;
        }

        .stApp [data-testid="stMarkdownContainer"] .waybill-muted {
          color: var(--muted) !important;
        }

        .stApp [data-testid="stMarkdownContainer"] .thin {
          color: var(--muted) !important;
        }

        .stApp [data-testid="stMarkdownContainer"] .section-heading {
          color: var(--muted) !important;
          font-weight: 600 !important;
          letter-spacing: 0.12em;
          text-transform: uppercase;
        }

        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
          color: var(--text) !important;
          font-weight: 700 !important;
        }

        /* Sidebar styling overrides */
        section[data-testid="stSidebar"] {
          background: linear-gradient(180deg, rgba(9,14,26,0.98), rgba(5,9,16,0.98)) !important;
          border-right: 1px solid rgba(140,160,210,0.14) !important;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
        section[data-testid="stSidebar"] div[role="radiogroup"] label p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] .stCaption p {
          color: var(--text) !important;
        }

        section[data-testid="stSidebar"] .stCaption p {
          color: var(--muted) !important;
        }

        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] + div p {
          color: var(--muted) !important;
        }

        section[data-testid="stSidebar"] .waybill-muted {
          color: var(--muted) !important;
        }

        /* Captions styling */
        .stCaption, .stCaption p, [data-testid="stCaptionContainer"] {
          color: var(--muted) !important;
          font-size: 0.85rem !important;
          font-weight: 500;
        }

        /* Metric Widget Styling as gorgeous hoverable KPI cards */
        [data-testid="stMetric"] {
          border: 1px solid var(--line) !important;
          background: var(--panel) !important;
          border-radius: 20px !important;
          padding: 1.1rem 1.25rem !important;
          min-height: 110px !important;
          box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;
          transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
        }

        [data-testid="stMetric"]:hover {
          transform: translateY(-2px) !important;
          border-color: rgba(255, 138, 61, 0.35) !important;
          box-shadow: 0 12px 35px rgba(255, 138, 61, 0.08) !important;
        }

        [data-testid="stMetricLabel"] {
          color: var(--muted) !important;
          font-weight: 500 !important;
          font-size: 0.9rem !important;
        }

        [data-testid="stMetricValue"] {
          color: var(--text) !important;
          font-weight: 800 !important;
          font-size: 1.9rem !important;
          letter-spacing: -0.02em !important;
        }

        /* Badge component */
        .badge {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          padding: 0.38rem 0.75rem;
          border-radius: 999px;
          font-size: 0.78rem;
          font-weight: 700;
        }

        /* Live status dot animations */
        @keyframes pulse-dot {
          0% { transform: scale(0.85); opacity: 0.55; }
          50% { transform: scale(1.15); opacity: 1; }
          100% { transform: scale(0.85); opacity: 0.55; }
        }
        .status-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          display: inline-block;
          flex-shrink: 0;
        }
        .dot-transit {
          background-color: #FF8A3D;
          box-shadow: 0 0 8px #FF8A3D;
          animation: pulse-dot 1.8s infinite ease-in-out;
        }
        .dot-delayed {
          background-color: #FF5C5C;
          box-shadow: 0 0 8px #FF5C5C;
          animation: pulse-dot 1.2s infinite ease-in-out;
        }
        .dot-pending {
          background-color: #8B93A7;
          box-shadow: 0 0 6px #8B93A7;
          animation: pulse-dot 2.2s infinite ease-in-out;
        }
        .dot-active {
          background-color: #3DDC97;
          box-shadow: 0 0 8px #3DDC97;
          animation: pulse-dot 2.0s infinite ease-in-out;
        }

        /* Sleek input & buttons styling */
        .login-shell {
          min-height: 92vh;
          display: grid;
          place-items: center;
          padding: 2rem;
        }
        .login-card {
          width: min(980px, 100%);
          display: grid;
          grid-template-columns: 1.1fr 0.9fr;
          border: 1px solid var(--line);
          background: rgba(8,13,24,0.88);
          border-radius: 30px;
          overflow: hidden;
        }
        .login-copy, .login-form { padding: 2rem; }
        .login-form { background: rgba(14,22,41,0.96); }
        .login-badge {
          display:inline-flex; align-items:center; gap:0.6rem;
          border: 1px solid rgba(255,138,61,0.18);
          background: rgba(255,138,61,0.08);
          padding: 0.5rem 0.8rem; border-radius: 999px;
          font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
          color: #ffcfaa; font-weight: 700;
        }
        .preview-row { display:flex; justify-content:space-between; gap:1rem; padding:0.8rem 0; border-bottom:1px solid rgba(255,255,255,0.06); }
        .preview-row:last-child { border-bottom:0; }
        @media (max-width: 900px) {
          .login-card { grid-template-columns: 1fr; }
        }

        /* Custom scrollbars */
        ::-webkit-scrollbar {
          width: 6px;
          height: 6px;
        }
        ::-webkit-scrollbar-track {
          background: transparent;
        }
        ::-webkit-scrollbar-thumb {
          background: rgba(142, 160, 201, 0.2);
          border-radius: 99px;
        }
        ::-webkit-scrollbar-thumb:hover {
          background: rgba(142, 160, 201, 0.4);
        }

        /* Streamlit Alerts override */
        [data-testid="stAlert"] {
          border-radius: 14px !important;
          background-color: rgba(61, 220, 151, 0.08) !important;
          border: 1px solid rgba(61, 220, 151, 0.2) !important;
          color: #3DDC97 !important;
        }

        /* Custom Premium Radio Buttons in Sidebar */
        div[role="radiogroup"] {
          gap: 8px !important;
        }
        div[role="radiogroup"] label {
          background: rgba(255, 255, 255, 0.02) !important;
          border: 1px solid rgba(142, 160, 201, 0.1) !important;
          border-radius: 12px !important;
          padding: 10px 14px !important;
          margin: 0 !important;
          transition: all 0.18s ease-in-out !important;
          cursor: pointer !important;
          display: flex !important;
          align-items: center !important;
          width: 100% !important;
        }
        div[role="radiogroup"] label:hover {
          background: rgba(255, 255, 255, 0.05) !important;
          border-color: rgba(142, 160, 201, 0.22) !important;
        }
        div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
          margin-left: 0 !important;
        }
        div[role="radiogroup"] label > div:first-child {
          display: none !important; /* Hide radio dot */
        }
        div[role="radiogroup"] label:has(input:checked) {
          background: linear-gradient(135deg, rgba(255, 138, 61, 0.18), rgba(255, 255, 255, 0.02)) !important;
          border-color: rgba(255, 138, 61, 0.35) !important;
          box-shadow: 0 4px 15px rgba(255, 138, 61, 0.06) !important;
        }
        div[role="radiogroup"] label:has(input:checked) p {
          color: #ff8a3d !important;
          font-weight: 700 !important;
        }

        /* Brand Logo in Sidebar */
        .brand-logo {
          width: 40px;
          height: 40px;
          border-radius: 10px;
          display: grid;
          place-items: center;
          color: #ffcfaa;
          background: linear-gradient(135deg, rgba(255, 138, 61, 0.24), rgba(255, 138, 61, 0.08));
          border: 1px solid rgba(255, 138, 61, 0.2);
          font-weight: 800;
          font-size: 1.15rem;
          box-shadow: 0 8px 20px rgba(255, 138, 61, 0.12);
        }

        /* Custom KPI Card Grid and KPI Card design */
        .kpi-grid {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 16px;
          margin-bottom: 24px;
        }
        @media (max-width: 768px) {
          .kpi-grid {
            grid-template-columns: 1fr;
          }
        }
        .kpi-card-custom {
          display: flex;
          align-items: center;
          gap: 16px;
          background: var(--panel);
          border: 1px solid var(--line);
          border-radius: 20px;
          padding: 1.1rem 1.4rem;
          box-shadow: 0 10px 30px rgba(0,0,0,0.18);
          transition: all 0.2s ease-in-out;
        }
        .kpi-card-custom:hover {
          transform: translateY(-2px);
          border-color: rgba(255, 138, 61, 0.35);
          box-shadow: 0 12px 35px rgba(255, 138, 61, 0.08);
        }
        .kpi-icon-wrap {
          width: 46px;
          height: 46px;
          border-radius: 14px;
          display: grid;
          place-items: center;
          font-size: 1.25rem;
          flex-shrink: 0;
        }
        .transit-icon {
          color: #ff8a3d;
          background: rgba(255, 138, 61, 0.12);
          border: 1px solid rgba(255, 138, 61, 0.2);
        }
        .alert-icon {
          color: #ff5c5c;
          background: rgba(255, 92, 92, 0.12);
          border: 1px solid rgba(255, 92, 92, 0.2);
        }
        .pending-icon {
          color: #8b93a7;
          background: rgba(139, 147, 167, 0.12);
          border: 1px solid rgba(139, 147, 167, 0.2);
        }
        .success-icon {
          color: #3ddc97;
          background: rgba(61, 220, 151, 0.12);
          border: 1px solid rgba(61, 220, 151, 0.2);
        }
        .kpi-val {
          font-size: 1.85rem;
          font-weight: 800;
          line-height: 1.1;
          color: var(--text);
          letter-spacing: -0.02em;
        }
        .kpi-lbl {
          font-size: 0.85rem;
          color: var(--muted);
          font-weight: 500;
          margin-top: 2px;
        }

        /* Custom dashboard lists */
        .custom-list-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 12px 0;
          border-bottom: 1px solid rgba(255, 255, 255, 0.05);
          transition: all 0.15s ease;
        }
        .custom-list-row:last-child {
          border-bottom: none;
          padding-bottom: 4px;
        }

        /* Button Styling Overrides */
        div.stButton > button {
          background-color: rgba(255, 255, 255, 0.03) !important;
          color: var(--text) !important;
          border: 1px solid rgba(142, 160, 201, 0.12) !important;
          border-radius: 12px !important;
          padding: 0.6rem 1rem !important;
          font-weight: 600 !important;
          transition: all 0.15s ease-in-out !important;
        }
        div.stButton > button:hover {
          background-color: rgba(255, 255, 255, 0.06) !important;
          border-color: rgba(255, 138, 61, 0.3) !important;
          color: #ff8a3d !important;
          transform: translateY(-1px);
        }
        div.stButton > button[kind="primary"] {
          background: linear-gradient(135deg, #ffcfaa, #ff8a3d) !important;
          color: #07111f !important;
          border: none !important;
          font-weight: 700 !important;
          box-shadow: 0 4px 15px rgba(255, 138, 61, 0.2) !important;
        }
        div.stButton > button[kind="primary"]:hover {
          background: linear-gradient(135deg, #ffe2cc, #ffa366) !important;
          box-shadow: 0 6px 20px rgba(255, 138, 61, 0.3) !important;
          transform: translateY(-1px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def seed_state() -> None:
    st.session_state.setdefault("authenticated", False)
    st.session_state.setdefault("role", "Admin")
    st.session_state.setdefault("email", "")
    st.session_state.setdefault("display_name", "")
    st.session_state.setdefault("section", "📊 Dashboard")
    st.session_state.setdefault("stock", [row.copy() for row in STOCK])
    st.session_state.setdefault("receiving", [row.copy() for row in RECEIVING])
    st.session_state.setdefault("receiving_lines", {key: [row.copy() for row in rows] for key, rows in RECEIVING_LINES.items()})
    st.session_state.setdefault("transactions", [row.copy() for row in TRANSACTIONS])
    st.session_state.setdefault("staff", [row.copy() for row in STAFF])
    st.session_state.setdefault("selected_shipment", SHIPMENTS[0]["id"])
    st.session_state.setdefault("toast", "")
    st.session_state.setdefault("stock_modal", False)
    st.session_state.setdefault("receiving_modal", False)
    st.session_state.setdefault("payment_modal", False)
    st.session_state.setdefault("staff_modal", False)
    st.session_state.setdefault("new_stock", {})
    st.session_state.setdefault("new_receiving", {})
    st.session_state.setdefault("new_payment", {})
    st.session_state.setdefault("new_staff", {})


def login_screen() -> None:
    st.markdown(
        """
        <div class="login-shell">
          <div class="login-card">
            <div class="login-copy">
              <div class="login-badge">HBK JADOON // goods transport</div>
              <h1 class="waybill-title">Haji Barkat Khan Jadoon Goods Transport</h1>
              <p class="waybill-muted">
                Sign in with any email and password. Toggle Admin or Staff to change what you can see.
                Everything stays in local Streamlit state so the prototype is ready for a real API later.
              </p>
              <div class="waybill-card">
                <div class="section-heading">Included modules</div>
                <div class="preview-row"><span>Dashboard</span><span class="mono">KPI cards</span></div>
                <div class="preview-row"><span>Shipments</span><span class="mono">Route detail</span></div>
                <div class="preview-row"><span>Receiving</span><span class="mono">Expandable GRNs</span></div>
              </div>
            </div>
            <div class="login-form">
        """,
        unsafe_allow_html=True,
    )
    with st.form("login_form", clear_on_submit=False):
        default_email = os.getenv("DEFAULT_EMAIL", "")
        email = st.text_input("Email", value=default_email, placeholder="name@company.com")
        password = st.text_input("Password", type="password", placeholder="Anything signs you in")
        role = st.radio("Role", ["Admin", "Staff"], horizontal=True)
        submitted = st.form_submit_button("Enter Portal", use_container_width=True, type="primary")
        if submitted and (email or password or True):
            st.session_state.authenticated = True
            st.session_state.email = email.strip() or "demo@waybill.local"
            st.session_state.display_name = st.session_state.email.split("@")[0].replace(".", " ").title()
            st.session_state.role = role
            st.session_state.toast = f"Signed in as {role}"
            st.rerun()
    st.markdown("</div></div></div>", unsafe_allow_html=True)


def sign_out() -> None:
    st.session_state.authenticated = False
    st.session_state.email = ""
    st.session_state.display_name = ""
    st.session_state.section = "📊 Dashboard"
    st.rerun()


def sidebar() -> list[str]:
    nav = ["📊 Dashboard", "🚚 Shipments", "📦 Stock", "📄 Receiving slips", "💳 Payments & expenses"]
    if st.session_state.role == "Admin":
        nav.append("👥 Staff management")

    st.sidebar.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px; padding: 6px 0;">
          <div class="brand-logo">HBK</div>
          <div>
            <div style="font-weight: 800; font-size: 0.95rem; letter-spacing: -0.02em; line-height: 1.2; color: var(--text);">HAJI BARKAT KHAN JADOON</div>
            <div class="waybill-muted" style="font-size: 0.8rem; font-weight: 600; color: #ff8a3d !important;">GOODS TRANSPORT</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    choice = st.sidebar.radio("Navigation", nav, index=nav.index(st.session_state.section) if st.session_state.section in nav else 0)
    st.session_state.section = choice
    st.sidebar.divider()
    st.sidebar.caption("Session role")
    st.session_state.role = st.sidebar.radio("Role", ["Admin", "Staff"], horizontal=True, label_visibility="collapsed")
    if st.sidebar.button("Sign out", use_container_width=True):
        sign_out()
    return nav


def topbar(title: str) -> None:
    left, right = st.columns([2.2, 1.2])
    with left:
        st.markdown(f'<h1 style="margin: 0 0 4px 0; font-size: 2.2rem; font-weight: 800; letter-spacing: -0.03em;">{title}</h1>', unsafe_allow_html=True)
        st.markdown(f'<div class="waybill-muted" style="font-size: 0.88rem; display: flex; align-items: center; gap: 8px;">'
                    f'Signed in as <strong style="color: var(--text); font-weight: 600;">{st.session_state.display_name}</strong> • '
                    f'<span class="badge" style="color: #ff8a3d !important; background: rgba(255,138,61,0.08) !important; padding: 0.2rem 0.6rem !important; font-size: 0.72rem !important;">{st.session_state.role}</span>'
                    f'</div>', unsafe_allow_html=True)
    with right:
        col_search, col_live = st.columns([2.5, 1])
        with col_search:
            st.text_input("Search", placeholder="Search shipments, stock, GRNs, staff", key="search_query", label_visibility="collapsed")
        with col_live:
            app_env = os.getenv("APP_ENVIRONMENT", "Production")
            st.markdown(
                f'<div style="height: 38px; display: flex; align-items: center; justify-content: center; gap: 6px; background: rgba(61,220,151,0.05); border: 1px solid rgba(61,220,151,0.15); border-radius: 12px; font-size: 0.82rem; font-weight: 600; color: #3DDC97; padding: 0 12px;">'
                '<span class="status-dot dot-active"></span>'
                f'{app_env}'
                '</div>',
                unsafe_allow_html=True
            )


def toast() -> None:
    if st.session_state.toast:
        st.success(st.session_state.toast)
        st.session_state.toast = ""


def dashboard() -> None:
    income = sum(tx["amount"] for tx in st.session_state.transactions if tx["type"] == "income")
    expense = sum(tx["amount"] for tx in st.session_state.transactions if tx["type"] == "expense")
    low_stock = sum(1 for item in st.session_state.stock if item["qty"] < item["reorder"])
    pending_grn = sum(1 for slip in st.session_state.receiving if slip["status"] != "received")
    active_shipments = sum(1 for shipment in SHIPMENTS if shipment["status"] == "in transit")
    staff_on_shift = sum(1 for person in st.session_state.staff if person["status"] == "active")

    last_icon = "💰" if st.session_state.role == "Admin" else "👥"
    last_label = "Net Cashflow" if st.session_state.role == "Admin" else "Staff on Shift"
    last_val = money(income - expense) if st.session_state.role == "Admin" else staff_on_shift
    last_class = "success-icon" if st.session_state.role == "Admin" else "transit-icon"

    kpi_html = (
        f'<div class="kpi-grid">'
        f'  <div class="kpi-card-custom">'
        f'    <div class="kpi-icon-wrap transit-icon">🚚</div>'
        f'    <div>'
        f'      <div class="kpi-val">{active_shipments}</div>'
        f'      <div class="kpi-lbl">Active Shipments</div>'
        f'    </div>'
        f'  </div>'
        f'  <div class="kpi-card-custom">'
        f'    <div class="kpi-icon-wrap alert-icon">⚠️</div>'
        f'    <div>'
        f'      <div class="kpi-val">{low_stock}</div>'
        f'      <div class="kpi-lbl">Low-Stock Alerts</div>'
        f'    </div>'
        f'  </div>'
        f'  <div class="kpi-card-custom">'
        f'    <div class="kpi-icon-wrap pending-icon">📄</div>'
        f'    <div>'
        f'      <div class="kpi-val">{pending_grn}</div>'
        f'      <div class="kpi-lbl">Pending Slips</div>'
        f'    </div>'
        f'  </div>'
        f'  <div class="kpi-card-custom">'
        f'    <div class="kpi-icon-wrap {last_class}">{last_icon}</div>'
        f'    <div>'
        f'      <div class="kpi-val">{last_val}</div>'
        f'      <div class="kpi-lbl">{last_label}</div>'
        f'    </div>'
        f'  </div>'
        f'</div>'
    )
    st.markdown(kpi_html, unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        shipment_rows = []
        for shipment in SHIPMENTS:
            if shipment["status"] == "delivered":
                continue
            badge_html = badge(shipment["status"])
            shipment_rows.append(
                f'<div class="custom-list-row">'
                f'  <div>'
                f'    <div style="font-weight: 700; color: var(--text); font-size: 0.98rem;">{shipment["client"]}</div>'
                f'    <div style="font-size: 0.85rem; color: var(--muted); margin-top: 3px;">{shipment["origin"]} &rarr; {shipment["dest"]}</div>'
                f'  </div>'
                f'  <div>{badge_html}</div>'
                f'</div>'
            )
        st.markdown(
            f'<div class="waybill-card">'
            f'  <div class="section-heading" style="margin-bottom: 12px;">Shipments in motion</div>'
            f'  {"".join(shipment_rows)}'
            f'</div>',
            unsafe_allow_html=True
        )

    with right:
        stock_rows = []
        for item in st.session_state.stock:
            if item["qty"] < item["reorder"]:
                badge_html = badge("pending")
                stock_rows.append(
                    f'<div class="custom-list-row">'
                    f'  <div>'
                    f'    <div style="font-weight: 700; color: var(--text); font-size: 0.98rem;">{item["item"]}</div>'
                    f'    <div style="font-size: 0.85rem; color: var(--muted); margin-top: 3px;">{item["warehouse"]} &bull; <strong style="color: #ff5c5c;">{item["qty"]} {item["unit"]}</strong> on hand</div>'
                    f'  </div>'
                    f'  <div>{badge_html}</div>'
                    f'</div>'
                )
        st.markdown(
            f'<div class="waybill-card">'
            f'  <div class="section-heading" style="margin-bottom: 12px;">Stock needing attention</div>'
            f'  {"".join(stock_rows)}'
            f'</div>',
            unsafe_allow_html=True
        )


def shipments_view() -> None:
    query = st.session_state.get("search_query", "").strip().lower()
    filtered = [shipment for shipment in SHIPMENTS if not query or any(query in str(shipment[field]).lower() for field in ("id", "client", "origin", "dest"))]
    left, right = st.columns([1, 1.35])
    with left:
        st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
        for shipment in filtered:
            if st.button(f"{shipment['id']} — {shipment['client']}", key=f"ship_{shipment['id']}", use_container_width=True):
                st.session_state.selected_shipment = shipment["id"]
        st.markdown("</div>", unsafe_allow_html=True)
    selected = next((item for item in SHIPMENTS if item["id"] == st.session_state.selected_shipment), SHIPMENTS[0])
    with right:
        progress_pct = int(selected["progress"] * 100)
        progress_color = STATUS_META.get(selected["status"], STATUS_META["pending"])[1]
        
        detail_html = f"""
        <div class="waybill-card" style="padding: 1.5rem 1.8rem;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
            <div>
              <span class="mono badge" style="background: rgba(255,255,255,0.03); color: #dce5ff; border: 1px solid rgba(255,255,255,0.08); font-size: 0.82rem; padding: 0.25rem 0.65rem;">{selected['id']}</span>
              <h2 style="margin: 8px 0 0 0; font-size: 1.8rem; font-weight: 800; letter-spacing: -0.02em; color: var(--text);">{selected['client']}</h2>
            </div>
            {badge(selected['status'])}
          </div>
          
          <div style="margin: 24px 0 16px 0;">
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: var(--muted); margin-bottom: 8px; font-weight: 600;">
              <span>Route Progress</span>
              <span>{progress_pct}%</span>
            </div>
            <div style="height: 8px; width: 100%; background: rgba(255,255,255,0.08); border-radius: 99px; overflow: hidden; position: relative;">
              <div style="height: 100%; width: {progress_pct}%; background: {progress_color}; border-radius: 99px; transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);"></div>
            </div>
          </div>
          
          <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
            <span style="color: var(--muted); font-size: 0.9rem;">Route</span>
            <strong style="color: var(--text); font-size: 0.9rem;">{selected['origin']} &rarr; {selected['dest']}</strong>
          </div>
          <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
            <span style="color: var(--muted); font-size: 0.9rem;">ETA</span>
            <strong style="color: var(--text); font-size: 0.9rem; display: flex; align-items: center; gap: 4px;">🕒 {selected['eta']}</strong>
          </div>
          <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
            <span style="color: var(--muted); font-size: 0.9rem;">Driver</span>
            <strong style="color: var(--text); font-size: 0.9rem;">{selected['driver']}</strong>
          </div>
          <div style="display: flex; justify-content: space-between; padding: 12px 0;">
            <span style="color: var(--muted); font-size: 0.9rem;">Vehicle ID</span>
            <strong class="mono" style="color: var(--text); font-size: 0.9rem; background: rgba(255,255,255,0.04); padding: 2px 6px; border-radius: 4px;">{selected['vehicle']}</strong>
          </div>
        </div>
        """
        st.markdown(detail_html, unsafe_allow_html=True)


def stock_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<div class="section-heading">Inventory</div>', unsafe_allow_html=True)
    with c2:
        if st.button("+ New item", use_container_width=True):
            st.session_state.stock_modal = not st.session_state.stock_modal
    st.dataframe(st.session_state.stock, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.stock_modal:
        with st.form("new_stock_form"):
            sku = st.text_input("SKU")
            item = st.text_input("Item")
            warehouse = st.text_input("Warehouse")
            qty = st.number_input("Qty on hand", min_value=0, step=1)
            reorder = st.number_input("Reorder threshold", min_value=0, step=1)
            unit = st.selectbox("Unit", ["pcs", "gal", "rolls", "pairs"])
            submitted = st.form_submit_button("Add item", type="primary")
            if submitted and sku and item:
                st.session_state.stock.insert(0, {"sku": sku, "item": item, "warehouse": warehouse, "qty": int(qty), "reorder": int(reorder), "unit": unit})
                st.session_state.stock_modal = False
                st.session_state.toast = f"{sku} added to inventory"
                st.rerun()


def receiving_view() -> None:
    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    if st.button("+ New slip"):
        st.session_state.receiving_modal = not st.session_state.receiving_modal
    for slip in st.session_state.receiving:
        with st.expander(f"{slip['id']} — {slip['supplier']}", expanded=st.session_state.get("open_grn", RECEIVING[0]["id"]) == slip["id"]):
            st.write(f"Date: {slip['date']} | Line items: {slip['items']} | Value: {money(slip['value'])}")
            st.markdown(badge(slip["status"]), unsafe_allow_html=True)
            st.dataframe(st.session_state.receiving_lines.get(slip["id"], []), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.receiving_modal:
        with st.form("new_receiving_form"):
            supplier = st.text_input("Supplier")
            items = st.number_input("Line items", min_value=1, step=1)
            value = st.number_input("Estimated value ($)", min_value=0, step=10)
            submitted = st.form_submit_button("Create slip", type="primary")
            if submitted and supplier:
                new_id = f"GRN-{3084 + len(st.session_state.receiving)}"
                st.session_state.receiving.insert(0, {"id": new_id, "supplier": supplier, "date": date.today().strftime("%b %d"), "status": "pending", "items": int(items), "value": int(value)})
                st.session_state.receiving_lines[new_id] = [{"name": "Pending line item entry", "ordered": 0, "received": 0}]
                st.session_state.receiving_modal = False
                st.session_state.toast = f"{new_id} created"
                st.rerun()


def payments_view() -> None:
    role = st.session_state.role
    income = sum(tx["amount"] for tx in st.session_state.transactions if tx["type"] == "income")
    expense = sum(tx["amount"] for tx in st.session_state.transactions if tx["type"] == "expense")
    visible = st.session_state.transactions if role == "Admin" else [tx for tx in st.session_state.transactions if tx["type"] == "expense" and tx.get("owner") == st.session_state.email]

    if role == "Admin":
        st.markdown(
            f'<div class="kpi-grid" style="grid-template-columns: repeat(3, 1fr); margin-bottom: 20px;">'
            f'  <div class="kpi-card-custom">'
            f'    <div class="kpi-icon-wrap success-icon">📈</div>'
            f'    <div>'
            f'      <div class="kpi-val" style="color: #3DDC97;">{money(income)}</div>'
            f'      <div class="kpi-lbl">Income (7d)</div>'
            f'    </div>'
            f'  </div>'
            f'  <div class="kpi-card-custom">'
            f'    <div class="kpi-icon-wrap alert-icon">📉</div>'
            f'    <div>'
            f'      <div class="kpi-val" style="color: #FF5C5C;">{money(expense)}</div>'
            f'      <div class="kpi-lbl">Expenses (7d)</div>'
            f'    </div>'
            f'  </div>'
            f'  <div class="kpi-card-custom">'
            f'    <div class="kpi-icon-wrap transit-icon">💰</div>'
            f'    <div>'
            f'      <div class="kpi-val">{money(income - expense)}</div>'
            f'      <div class="kpi-lbl">Net Cashflow</div>'
            f'    </div>'
            f'  </div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    st.dataframe(visible, use_container_width=True, hide_index=True)
    if st.button("+ New entry"):
        st.session_state.payment_modal = not st.session_state.payment_modal
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.payment_modal:
        with st.form("new_payment_form"):
            desc = st.text_input("Description")
            category = st.text_input("Category")
            amount = st.number_input("Amount ($)", min_value=0, step=10)
            tx_type = st.selectbox("Type", ["expense", "income"] if role == "Admin" else ["expense"])
            submitted = st.form_submit_button("Save", type="primary")
            if submitted and desc:
                new_id = f"TXN-{9008 + len(st.session_state.transactions)}"
                st.session_state.transactions.insert(0, {"id": new_id, "type": tx_type, "desc": desc, "date": date.today().strftime("%b %d"), "amount": int(amount), "category": category or "General", "owner": st.session_state.email})
                st.session_state.payment_modal = False
                st.session_state.toast = "Transaction saved"
                st.rerun()


def staff_view() -> None:
    if st.session_state.role != "Admin":
        st.info("Staff management is hidden from Staff role.")
        return

    st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
    if st.button("+ Invite staff"):
        st.session_state.staff_modal = not st.session_state.staff_modal
    st.dataframe(st.session_state.staff, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    for idx, person in enumerate(st.session_state.staff):
        cols = st.columns([2.2, 1.2, 1, 1])
        cols[0].write(person["name"])
        cols[1].write(person["role"])
        cols[2].write(person["access"])
        updated_status = cols[3].selectbox("Status", ["active", "suspended"], index=0 if person["status"] == "active" else 1, key=f"staff_status_{idx}")
        st.session_state.staff[idx]["status"] = updated_status

    if st.session_state.staff_modal:
        with st.form("staff_invite_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            role = st.text_input("Role", value="Driver")
            access = st.selectbox("Access", ["Staff", "Admin"])
            submitted = st.form_submit_button("Invite", type="primary")
            if submitted and name:
                initials = "".join(part[0].upper() for part in name.split()[:2])
                st.session_state.staff.insert(0, {"name": name, "email": email or f"{name.replace(' ', '.').lower()}@waybill.local", "role": role, "access": access, "status": "active", "initials": initials})
                st.session_state.staff_modal = False
                st.session_state.toast = f"{name} invited"
                st.rerun()


def main() -> None:
    seed_state()
    css()

    if not st.session_state.authenticated:
        login_screen()
        return

    nav = sidebar()
    topbar(st.session_state.section)
    toast()

    section = st.session_state.section
    if "Dashboard" in section:
        dashboard()
    elif "Shipments" in section:
        shipments_view()
    elif "Stock" in section:
        stock_view()
    elif "Receiving slips" in section:
        receiving_view()
    elif "Payments & expenses" in section:
        payments_view()
    elif "Staff management" in section and st.session_state.role == "Admin":
        staff_view()


if __name__ == "__main__":
    main()