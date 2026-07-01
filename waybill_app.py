from __future__ import annotations

from datetime import date

import streamlit as st


st.set_page_config(page_title="Waybill", layout="wide", initial_sidebar_state="expanded")


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
    return f'<span class="badge" style="color:{color};background:{bg}">{label}</span>'


def css() -> None:
    st.markdown(
        """
        <style>
        :root {
          --bg: #07111f;
          --panel: rgba(13, 21, 38, 0.88);
          --panel-strong: rgba(17, 27, 47, 0.95);
          --line: rgba(142, 160, 201, 0.16);
          --text: #edf2ff;
          --muted: #97a3c4;
          --accent: #ff8a3d;
        }
        .stApp {
          background:
            radial-gradient(circle at top left, rgba(255, 138, 61, 0.16), transparent 28%),
            radial-gradient(circle at top right, rgba(61, 220, 151, 0.12), transparent 24%),
            linear-gradient(180deg, #07111f 0%, #0b1324 46%, #070d17 100%);
          color: var(--text);
        }
        section[data-testid="stSidebar"] {
          background: linear-gradient(180deg, rgba(9,14,26,0.98), rgba(5,9,16,0.98));
          border-right: 1px solid rgba(140,160,210,0.14);
        }
        .waybill-card {
          border: 1px solid var(--line);
          background: var(--panel-strong);
          border-radius: 24px;
          padding: 1rem 1.1rem;
          margin-bottom: 1rem;
        }
        .waybill-kpi {
          border: 1px solid var(--line);
          background: var(--panel);
          border-radius: 20px;
          padding: 1rem;
          min-height: 120px;
        }
        .waybill-title {
          margin: 0 0 0.3rem;
          font-size: 2.5rem;
          line-height: 0.98;
        }
        .waybill-muted { color: var(--muted); }
        .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
        .badge {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          padding: 0.35rem 0.72rem;
          border-radius: 999px;
          font-size: 0.78rem;
          font-weight: 700;
        }
        .thin { color: var(--muted); font-size: 0.92rem; }
        .section-heading { margin: 0.5rem 0 0.75rem; text-transform: uppercase; letter-spacing: 0.12em; color: var(--muted); font-size: 0.82rem; }
        .top-row { display:flex; justify-content:space-between; gap:1rem; align-items:flex-end; flex-wrap:wrap; }
        .right-pill {
          border: 1px solid var(--line);
          background: rgba(255,255,255,0.03);
          border-radius: 16px;
          padding: 0.8rem 1rem;
        }
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
        </style>
        """,
        unsafe_allow_html=True,
    )


def seed_state() -> None:
    st.session_state.setdefault("authenticated", False)
    st.session_state.setdefault("role", "Admin")
    st.session_state.setdefault("email", "")
    st.session_state.setdefault("display_name", "")
    st.session_state.setdefault("section", "Dashboard")
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
              <div class="login-badge">WAYBILL // prototype auth</div>
              <h1 class="waybill-title">Logistics control for freight ops</h1>
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
        email = st.text_input("Email", placeholder="name@company.com")
        password = st.text_input("Password", type="password", placeholder="Anything signs you in")
        role = st.radio("Role", ["Admin", "Staff"], horizontal=True)
        submitted = st.form_submit_button("Enter Waybill", use_container_width=True)
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
    st.session_state.section = "Dashboard"
    st.rerun()


def sidebar() -> list[str]:
    nav = ["Dashboard", "Shipments", "Stock", "Receiving slips", "Payments & expenses"]
    if st.session_state.role == "Admin":
        nav.append("Staff management")

    st.sidebar.markdown('<div class="login-badge">WB</div>', unsafe_allow_html=True)
    st.sidebar.markdown("### Waybill")
    st.sidebar.markdown('<div class="waybill-muted">Industrial logistics control</div>', unsafe_allow_html=True)
    choice = st.sidebar.radio("Navigation", nav, index=nav.index(st.session_state.section) if st.session_state.section in nav else 0)
    st.session_state.section = choice
    st.sidebar.divider()
    st.sidebar.caption("Session role")
    st.session_state.role = st.sidebar.radio("", ["Admin", "Staff"], horizontal=True, label_visibility="collapsed")
    if st.sidebar.button("Sign out", use_container_width=True):
        sign_out()
    return nav


def topbar(title: str) -> None:
    left, right = st.columns([2.2, 1.2])
    with left:
        st.markdown(f"## {title}")
        st.caption(f"Signed in as {st.session_state.display_name} • {st.session_state.role}")
    with right:
        st.text_input("Search", placeholder="Search shipments, stock, GRNs, staff", key="search_query")


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

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Active shipments", active_shipments)
    k2.metric("Low-stock alerts", low_stock)
    k3.metric("Pending receiving slips", pending_grn)
    k4.metric("Net this week" if st.session_state.role == "Admin" else "Staff on shift", money(income - expense) if st.session_state.role == "Admin" else staff_on_shift)

    left, right = st.columns(2)
    with left:
        st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Shipments in motion</div>', unsafe_allow_html=True)
        for shipment in SHIPMENTS:
            if shipment["status"] == "delivered":
                continue
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(f"**{shipment['client']}**")
                st.caption(f"{shipment['origin']} - {shipment['dest']}")
            with c2:
                st.markdown(badge(shipment["status"]), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">Stock needing attention</div>', unsafe_allow_html=True)
        for item in st.session_state.stock:
            if item["qty"] < item["reorder"]:
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**{item['item']}**")
                    st.caption(f"{item['warehouse']} - {item['qty']} {item['unit']} on hand")
                with c2:
                    st.markdown(badge("pending"), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


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
        st.markdown('<div class="waybill-card">', unsafe_allow_html=True)
        st.markdown(f"#### {selected['id']}")
        st.write(selected["client"])
        st.progress(selected["progress"])
        st.markdown(f"**Route:** {selected['origin']} -> {selected['dest']}")
        st.markdown(f"**ETA:** {selected['eta']}")
        st.markdown(f"**Driver:** {selected['driver']}")
        st.markdown(f"**Vehicle:** {selected['vehicle']}")
        st.markdown(badge(selected["status"]), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


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
            submitted = st.form_submit_button("Add item")
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
            submitted = st.form_submit_button("Create slip")
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
        a, b, c = st.columns(3)
        a.metric("Income", money(income))
        b.metric("Expenses", money(expense))
        c.metric("Net", money(income - expense))

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
            submitted = st.form_submit_button("Save")
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
            submitted = st.form_submit_button("Invite")
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
    if section == "Dashboard":
        dashboard()
    elif section == "Shipments":
        shipments_view()
    elif section == "Stock":
        stock_view()
    elif section == "Receiving slips":
        receiving_view()
    elif section == "Payments & expenses":
        payments_view()
    elif section == "Staff management" and st.session_state.role == "Admin":
        staff_view()


if __name__ == "__main__":
    main()