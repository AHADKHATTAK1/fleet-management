import React, { useState } from "react";
import {
  Truck,
  Clock,
  CheckCircle2,
  AlertTriangle,
  ChevronDown,
  Plus,
  X,
  ArrowUpRight,
  ArrowDownRight,
  FileText,
  LayoutDashboard,
  Boxes,
  ClipboardList,
  Wallet,
  Users,
  Shield,
  Search,
  MapPin,
  Package,
} from "lucide-react";
import "./App.css";

const SHIPMENTS = [
  { id: "WB-48213", client: "Northbridge Foods", origin: "Long Beach, CA", dest: "Reno, NV", status: "in_transit", eta: "2:40 PM", progress: 0.62 },
  { id: "WB-48190", client: "Calder Steel Co.", origin: "Gary, IN", dest: "Detroit, MI", status: "delayed", eta: "11:15 AM", progress: 0.41 },
  { id: "WB-48177", client: "Verde Pharma", origin: "Memphis, TN", dest: "Atlanta, GA", status: "delivered", eta: "Delivered 8:52 AM", progress: 1 },
  { id: "WB-48241", client: "Hallstrom Furniture", origin: "High Point, NC", dest: "Columbus, OH", status: "scheduled", eta: "6:05 PM", progress: 0 },
];

const STOCK = [
  { sku: "PLT-1180", item: "Standard pallets (48x40)", warehouse: "Reno DC", qty: 412, reorder: 150, unit: "pcs" },
  { sku: "FUEL-DSL", item: "Diesel reserve", warehouse: "Detroit Yard 3", qty: 88, reorder: 200, unit: "gal" },
  { sku: "PKG-STR1", item: "Strapping rolls", warehouse: "Reno DC", qty: 36, reorder: 50, unit: "rolls" },
  { sku: "TIRE-22R", item: "Tires 22.5R (drive axle)", warehouse: "Columbus Hub", qty: 14, reorder: 12, unit: "pcs" },
  { sku: "COLD-GEL", item: "Cold-chain gel packs", warehouse: "Atlanta Hub", qty: 540, reorder: 300, unit: "pcs" },
  { sku: "PPE-GLV", item: "Loading gloves (L)", warehouse: "Reno DC", qty: 22, reorder: 40, unit: "pairs" },
];

const RECEIVING = [
  { id: "GRN-3081", supplier: "Premier Pallet Supply", date: "Jun 28", status: "received", items: 3, value: 4120 },
  { id: "GRN-3082", supplier: "Continental Tire Distributors", date: "Jun 29", status: "partial", items: 5, value: 9860 },
  { id: "GRN-3083", supplier: "ColdPack Industries", date: "Jun 30", status: "pending", items: 2, value: 2310 },
  { id: "GRN-3079", supplier: "FuelCo Bulk Services", date: "Jun 26", status: "received", items: 1, value: 18450 },
];

const RECEIVING_LINES = {
  "GRN-3081": [
    { name: "Standard pallets (48x40)", ordered: 500, received: 500 },
    { name: "Strapping rolls", ordered: 60, received: 60 },
    { name: "Corner protectors", ordered: 1000, received: 1000 },
  ],
  "GRN-3082": [
    { name: "Tires 22.5R (drive axle)", ordered: 20, received: 12 },
    { name: "Wheel balancing weights", ordered: 200, received: 200 },
  ],
  "GRN-3083": [
    { name: "Cold-chain gel packs", ordered: 800, received: 0 },
    { name: "Insulated liners", ordered: 150, received: 0 },
  ],
  "GRN-3079": [{ name: "Diesel reserve", ordered: 2000, received: 2000 }],
};

const TRANSACTIONS = [
  { id: "TXN-9001", type: "income", desc: "Freight payment - Northbridge Foods", date: "Jun 30", amount: 6200, category: "Client payment" },
  { id: "TXN-9002", type: "expense", desc: "Diesel refuel - TRK-0731", date: "Jun 30", amount: 410, category: "Fuel" },
  { id: "TXN-9003", type: "expense", desc: "Toll - I-80 corridor", date: "Jun 30", amount: 38, category: "Toll" },
  { id: "TXN-9004", type: "expense", desc: "Driver payout - M. Okafor", date: "Jun 29", amount: 980, category: "Payroll" },
  { id: "TXN-9005", type: "income", desc: "Freight payment - Verde Pharma", date: "Jun 29", amount: 4750, category: "Client payment" },
  { id: "TXN-9006", type: "expense", desc: "Tire replacement - Columbus Hub", date: "Jun 28", amount: 1240, category: "Maintenance" },
  { id: "TXN-9007", type: "expense", desc: "Warehouse lease - Reno DC", date: "Jun 27", amount: 5200, category: "Facilities" },
];

const STAFF = [
  { name: "Maria Okafor", role: "Driver", access: "Staff", status: "active", initials: "MO" },
  { name: "Ricardo Vasquez", role: "Driver", access: "Staff", status: "active", initials: "RV" },
  { name: "Sungmin Park", role: "Driver", access: "Staff", status: "active", initials: "SP" },
  { name: "Jamal Bell", role: "Dispatcher", access: "Staff", status: "active", initials: "JB" },
  { name: "Elena Cho", role: "Warehouse Lead", access: "Staff", status: "suspended", initials: "EC" },
  { name: "David Reyes", role: "Operations Manager", access: "Admin", status: "active", initials: "DR" },
];

const STATUS_META = {
  in_transit: { label: "In transit", color: "#FF8A3D", bg: "rgba(255,138,61,0.12)" },
  delayed: { label: "Delayed", color: "#FF5C5C", bg: "rgba(255,92,92,0.12)" },
  delivered: { label: "Delivered", color: "#3DDC97", bg: "rgba(61,220,151,0.12)" },
  scheduled: { label: "Scheduled", color: "#8B93A7", bg: "rgba(139,147,167,0.12)" },
  received: { label: "Received", color: "#3DDC97", bg: "rgba(61,220,151,0.12)" },
  partial: { label: "Partial", color: "#FF8A3D", bg: "rgba(255,138,61,0.12)" },
  pending: { label: "Pending", color: "#8B93A7", bg: "rgba(139,147,167,0.12)" },
  active: { label: "Active", color: "#3DDC97", bg: "rgba(61,220,151,0.12)" },
  suspended: { label: "Suspended", color: "#FF5C5C", bg: "rgba(255,92,92,0.12)" },
};

const NAV_ITEMS = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "shipments", label: "Shipments", icon: Truck },
  { id: "inventory", label: "Inventory", icon: Boxes },
  { id: "receiving", label: "Receiving", icon: ClipboardList },
  { id: "payments", label: "Payments", icon: Wallet },
  { id: "people", label: "People", icon: Users },
];

const money = (n) => `$${n.toLocaleString()}`;

const Pill = ({ status }) => {
  const meta = STATUS_META[status] || STATUS_META.pending;
  let dotClass = "";
  if (status === "in_transit") dotClass = "status-dot dot-transit";
  else if (status === "delayed") dotClass = "status-dot dot-delayed";
  else if (status === "pending" || status === "partial") dotClass = "status-dot dot-pending";
  else if (status === "received" || status === "delivered" || status === "active") dotClass = "status-dot dot-active";

  return (
    <span className="pill" style={{ color: meta.color, background: meta.bg }}>
      {dotClass && <span className={dotClass} />}
      {meta.label}
    </span>
  );
};

function flashToast(setToast, msg) {
  setToast(msg);
  if (typeof window.__toastTimer === "number") window.clearTimeout(window.__toastTimer);
  window.__toastTimer = window.setTimeout(() => setToast(""), 2400);
}

function Dashboard({ role, stock, receiving, transactions, staff }) {
  const income = transactions.filter((t) => t.type === "income").reduce((a, b) => a + b.amount, 0);
  const expense = transactions.filter((t) => t.type === "expense").reduce((a, b) => a + b.amount, 0);
  const lowStock = stock.filter((s) => s.qty < s.reorder).length;
  const pendingGRN = receiving.filter((r) => r.status !== "received").length;
  const activeShipments = SHIPMENTS.filter((s) => s.status === "in_transit").length;

  const cards = [
    { label: "Active shipments", value: activeShipments, icon: Truck, color: "#FF8A3D" },
    { label: "Low stock alerts", value: lowStock, icon: AlertTriangle, color: "#FF5C5C" },
    { label: "Pending receiving slips", value: pendingGRN, icon: ClipboardList, color: "#8B93A7" },
    role === "Admin"
      ? { label: "Net this week", value: money(income - expense), icon: Wallet, color: "#3DDC97" }
      : { label: "Staff on shift", value: staff.filter((s) => s.status === "active").length, icon: Users, color: "#3DDC97" },
  ];

  return (
    <div>
      <div className="card-grid">
        {cards.map((c, i) => (
          <div className="kpi-card" key={i}>
            <div className="kpi-icon" style={{ color: c.color, background: `${c.color}1F` }}>
              <c.icon size={17} />
            </div>
            <div>
              <div className="kpi-value">{c.value}</div>
              <div className="kpi-label">{c.label}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="two-col">
        <div className="panel">
          <div className="section-label">Shipments in motion</div>
          {SHIPMENTS.filter((s) => s.status !== "delivered").map((s) => (
            <div className="mini-row" key={s.id}>
              <div>
                <div className="mini-title">{s.client}</div>
                <div className="mini-sub">
                  {s.origin} - {s.dest}
                </div>
              </div>
              <Pill status={s.status} />
            </div>
          ))}
        </div>

        <div className="panel">
          <div className="section-label">Stock needing attention</div>
          {stock.filter((s) => s.qty < s.reorder).map((s) => (
            <div className="mini-row" key={s.sku}>
              <div>
                <div className="mini-title">{s.item}</div>
                <div className="mini-sub">
                  {s.warehouse} - {s.qty} {s.unit} on hand
                </div>
              </div>
              <span className="pill" style={{ color: "#FF5C5C", background: "rgba(255,92,92,0.12)" }}>
                Reorder
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function ShipmentsView({ shipments }) {
  const [selectedId, setSelectedId] = useState(shipments[0]?.id || SHIPMENTS[0].id);

  React.useEffect(() => {
    if (!shipments.some((s) => s.id === selectedId)) {
      setSelectedId(shipments[0]?.id || SHIPMENTS[0].id);
    }
  }, [shipments, selectedId]);

  const selected = shipments.find((s) => s.id === selectedId) || shipments[0] || SHIPMENTS[0];
  const meta = STATUS_META[selected.status] || STATUS_META.pending;

  return (
    <div className="two-col shipments-layout">
      <div className="ship-list">
        {shipments.map((s) => (
          <button key={s.id} className={`ship-card ${s.id === selectedId ? "active" : ""}`} onClick={() => setSelectedId(s.id)}>
            <div className="ship-card-top">
              <span className="mono-tag">{s.id}</span>
              <Pill status={s.status} />
            </div>
            <div className="mini-title">{s.client}</div>
            <div className="mini-sub">
              {s.origin} - {s.dest}
            </div>
          </button>
        ))}
      </div>

      <div className="panel">
        <div className="detail-top">
          <div>
            <div className="mono-tag">{selected.id}</div>
            <div className="detail-client">{selected.client}</div>
          </div>
          <Pill status={selected.status} />
        </div>
        <div className="route-track">
          <div className="route-fill" style={{ width: `${selected.progress * 100}%`, background: meta.color }} />
          <div className="route-truck" style={{ left: `calc(${selected.progress * 100}% - 9px)`, color: meta.color }}>
            <Truck size={18} />
          </div>
        </div>
        <div className="route-endpoints">
          <span>{selected.origin}</span>
          <span>{selected.dest}</span>
        </div>
        <div className="meta-item" style={{ marginTop: 22 }}>
          <span className="meta-label">ETA</span>
          <span className="meta-value">
            <Clock size={13} />
            {selected.eta}
          </span>
        </div>
      </div>
    </div>
  );
}

function Modal({ title, onClose, children, onSubmit, submitLabel }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={(e) => e.stopPropagation()}>
        <div className="modal-head">
          <div className="modal-title">{title}</div>
          <button className="modal-close" onClick={onClose}>
            <X size={16} />
          </button>
        </div>
        <div className="modal-body">{children}</div>
        <div className="modal-foot">
          <button className="btn-ghost" onClick={onClose}>
            Cancel
          </button>
          <button className="btn-primary" onClick={onSubmit}>
            {submitLabel}
          </button>
        </div>
      </div>
    </div>
  );
}

function Field({ label, children }) {
  return (
    <label className="field">
      <span className="field-label">{label}</span>
      {children}
    </label>
  );
}

function Toast({ text }) {
  return (
    <div className="toast">
      <CheckCircle2 size={15} />
      {text}
    </div>
  );
}

function StockView({ stock, setStock }) {
  const [open, setOpen] = useState(false);
  const blank = { sku: "", item: "", warehouse: "", qty: "", reorder: "", unit: "pcs" };
  const [form, setForm] = useState(blank);
  const [toast, setToast] = useState("");

  const submit = () => {
    if (!form.item || !form.sku) return;
    setStock([{ ...form, qty: Number(form.qty) || 0, reorder: Number(form.reorder) || 0 }, ...stock]);
    setForm(blank);
    setOpen(false);
    flashToast(setToast, `${form.sku} added to inventory`);
  };

  return (
    <div className="panel">
      {toast && <Toast text={toast} />}
      <div className="table-head">
        <div className="section-label" style={{ marginBottom: 0 }}>
          Inventory - {stock.length} SKUs
        </div>
        <button className="btn-primary" onClick={() => setOpen(true)}>
          <Plus size={14} />
          New item
        </button>
      </div>
      <table className="data-table">
        <thead>
          <tr>
            <th>SKU</th>
            <th>Item</th>
            <th>Warehouse</th>
            <th>On hand</th>
            <th>Reorder at</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {stock.map((s) => {
            const low = s.qty < s.reorder;
            return (
              <tr key={s.sku}>
                <td className="mono-cell">{s.sku}</td>
                <td>{s.item}</td>
                <td>{s.warehouse}</td>
                <td>
                  {s.qty} {s.unit}
                </td>
                <td>
                  {s.reorder} {s.unit}
                </td>
                <td>
                  <span className="pill" style={{ color: low ? "#FF5C5C" : "#3DDC97", background: low ? "rgba(255,92,92,0.12)" : "rgba(61,220,151,0.12)" }}>
                    {low ? "Reorder" : "In stock"}
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>

      {open && (
        <Modal title="New inventory item" onClose={() => setOpen(false)} onSubmit={submit} submitLabel="Add item">
          <Field label="SKU">
            <input value={form.sku} onChange={(e) => setForm({ ...form, sku: e.target.value })} placeholder="e.g. PLT-1190" />
          </Field>
          <Field label="Item name">
            <input value={form.item} onChange={(e) => setForm({ ...form, item: e.target.value })} placeholder="e.g. Shrink wrap rolls" />
          </Field>
          <Field label="Warehouse">
            <input value={form.warehouse} onChange={(e) => setForm({ ...form, warehouse: e.target.value })} placeholder="e.g. Reno DC" />
          </Field>
          <div className="field-row">
            <Field label="Quantity on hand">
              <input type="number" value={form.qty} onChange={(e) => setForm({ ...form, qty: e.target.value })} />
            </Field>
            <Field label="Reorder threshold">
              <input type="number" value={form.reorder} onChange={(e) => setForm({ ...form, reorder: e.target.value })} />
            </Field>
          </div>
          <Field label="Unit">
            <select value={form.unit} onChange={(e) => setForm({ ...form, unit: e.target.value })}>
              <option value="pcs">pcs</option>
              <option value="gal">gal</option>
              <option value="rolls">rolls</option>
              <option value="pairs">pairs</option>
            </select>
          </Field>
        </Modal>
      )}
    </div>
  );
}

function ReceivingView({ receiving, setReceiving, lines, setLines }) {
  const [openId, setOpenId] = useState(receiving[0]?.id || null);
  const [open, setOpen] = useState(false);
  const blank = { supplier: "", items: "", value: "" };
  const [form, setForm] = useState(blank);
  const [toast, setToast] = useState("");

  const submit = () => {
    if (!form.supplier) return;
    const id = `GRN-${3084 + receiving.length}`;
    setReceiving([{ id, supplier: form.supplier, date: "Jun 30", status: "pending", items: Number(form.items) || 1, value: Number(form.value) || 0 }, ...receiving]);
    setLines({ ...lines, [id]: [{ name: "Pending line item entry", ordered: 0, received: 0 }] });
    setForm(blank);
    setOpen(false);
    flashToast(setToast, `${id} created`);
  };

  return (
    <div className="panel">
      {toast && <Toast text={toast} />}
      <div className="table-head">
        <div className="section-label" style={{ marginBottom: 0 }}>
          Receiving slips - {receiving.length} total
        </div>
        <button className="btn-primary" onClick={() => setOpen(true)}>
          <Plus size={14} />
          New slip
        </button>
      </div>

      {receiving.map((r) => {
        const isOpen = openId === r.id;
        return (
          <div className="grn-block" key={r.id}>
            <button className="grn-header" onClick={() => setOpenId(isOpen ? null : r.id)}>
              <div className="grn-header-left">
                <FileText size={15} color="#8B93A7" />
                <div>
                  <div className="mini-title">
                    {r.id} - {r.supplier}
                  </div>
                  <div className="mini-sub">
                    {r.date} - {r.items} line items - {money(r.value)}
                  </div>
                </div>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <Pill status={r.status} />
                <ChevronDown size={16} style={{ transform: isOpen ? "rotate(180deg)" : "none", transition: "0.15s" }} />
              </div>
            </button>
            {isOpen && (
              <table className="data-table nested">
                <thead>
                  <tr>
                    <th>Item</th>
                    <th>Ordered</th>
                    <th>Received</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {(lines[r.id] || []).map((l, i) => {
                    const full = l.received >= l.ordered && l.ordered > 0;
                    const none = l.received === 0;
                    return (
                      <tr key={i}>
                        <td>{l.name}</td>
                        <td>{l.ordered}</td>
                        <td>{l.received}</td>
                        <td>
                          <span
                            className="pill"
                            style={{
                              color: full ? "#3DDC97" : none ? "#8B93A7" : "#FF8A3D",
                              background: full ? "rgba(61,220,151,0.12)" : none ? "rgba(139,147,167,0.12)" : "rgba(255,138,61,0.12)",
                            }}
                          >
                            {full ? "Complete" : none ? "Awaiting" : "Short"}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            )}
          </div>
        );
      })}

      {open && (
        <Modal title="New receiving slip" onClose={() => setOpen(false)} onSubmit={submit} submitLabel="Create slip">
          <Field label="Supplier">
            <input value={form.supplier} onChange={(e) => setForm({ ...form, supplier: e.target.value })} placeholder="e.g. Premier Pallet Supply" />
          </Field>
          <div className="field-row">
            <Field label="Line items">
              <input type="number" value={form.items} onChange={(e) => setForm({ ...form, items: e.target.value })} />
            </Field>
            <Field label="Estimated value ($)">
              <input type="number" value={form.value} onChange={(e) => setForm({ ...form, value: e.target.value })} />
            </Field>
          </div>
        </Modal>
      )}
    </div>
  );
}

function PaymentsView({ role, transactions, setTransactions }) {
  const income = transactions.filter((t) => t.type === "income").reduce((a, b) => a + b.amount, 0);
  const expense = transactions.filter((t) => t.type === "expense").reduce((a, b) => a + b.amount, 0);
  const visible = role === "Admin" ? transactions : transactions.filter((t) => t.type === "expense");

  const [open, setOpen] = useState(false);
  const blank = { desc: "", category: "", amount: "", type: "expense" };
  const [form, setForm] = useState(blank);
  const [toast, setToast] = useState("");

  const submit = () => {
    if (!form.desc || !form.amount) return;
    const id = `TXN-${9008 + transactions.length}`;
    setTransactions([
      { id, desc: form.desc, category: form.category || "General", amount: Number(form.amount), date: "Jun 30", type: role === "Admin" ? form.type : "expense" },
      ...transactions,
    ]);
    setForm(blank);
    setOpen(false);
    flashToast(setToast, role === "Admin" ? `${id} recorded` : "Expense submitted for approval");
  };

  return (
    <div>
      {toast && <Toast text={toast} />}

      {role === "Admin" && (
        <div className="card-grid payments-summary">
          <div className="kpi-card">
            <div className="kpi-icon" style={{ color: "#3DDC97", background: "#3DDC971F" }}>
              <ArrowUpRight size={17} />
            </div>
            <div>
              <div className="kpi-value">{money(income)}</div>
              <div className="kpi-label">Income (7d)</div>
            </div>
          </div>
          <div className="kpi-card">
            <div className="kpi-icon" style={{ color: "#FF5C5C", background: "#FF5C5C1F" }}>
              <ArrowDownRight size={17} />
            </div>
            <div>
              <div className="kpi-value">{money(expense)}</div>
              <div className="kpi-label">Expenses (7d)</div>
            </div>
          </div>
          <div className="kpi-card">
            <div className="kpi-icon" style={{ color: "#FF8A3D", background: "#FF8A3D1F" }}>
              <Wallet size={17} />
            </div>
            <div>
              <div className="kpi-value">{money(income - expense)}</div>
              <div className="kpi-label">Net cashflow</div>
            </div>
          </div>
        </div>
      )}

      <div className="panel">
        <div className="table-head">
          <div className="section-label" style={{ marginBottom: 0 }}>
            Transactions - {visible.length} entries
          </div>
          <button className="btn-primary" onClick={() => setOpen(true)}>
            <Plus size={14} />
            New entry
          </button>
        </div>

        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Description</th>
              <th>Category</th>
              <th>Date</th>
              <th>Amount</th>
              <th>Type</th>
            </tr>
          </thead>
          <tbody>
            {visible.map((t) => (
              <tr key={t.id}>
                <td className="mono-cell">{t.id}</td>
                <td>{t.desc}</td>
                <td>{t.category}</td>
                <td>{t.date}</td>
                <td className={t.type === "income" ? "income-cell" : "expense-cell"}>{t.type === "income" ? "+" : "-"}{money(t.amount)}</td>
                <td>
                  <span className="pill" style={{ color: t.type === "income" ? "#3DDC97" : "#FF5C5C", background: t.type === "income" ? "rgba(61,220,151,0.12)" : "rgba(255,92,92,0.12)" }}>
                    {t.type}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {open && (
        <Modal title={role === "Admin" ? "New transaction" : "Submit expense"} onClose={() => setOpen(false)} onSubmit={submit} submitLabel={role === "Admin" ? "Record" : "Submit"}>
          <Field label="Description">
            <input value={form.desc} onChange={(e) => setForm({ ...form, desc: e.target.value })} placeholder="e.g. Diesel refuel - TRK-0731" />
          </Field>
          <Field label="Category">
            <input value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} placeholder="e.g. Fuel" />
          </Field>
          <div className="field-row">
            <Field label="Amount ($)">
              <input type="number" value={form.amount} onChange={(e) => setForm({ ...form, amount: e.target.value })} />
            </Field>
            {role === "Admin" && (
              <Field label="Type">
                <select value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })}>
                  <option value="expense">expense</option>
                  <option value="income">income</option>
                </select>
              </Field>
            )}
          </div>
        </Modal>
      )}
    </div>
  );
}

function PeopleView({ staff, setStaff, role }) {
  const [open, setOpen] = useState(false);
  const blank = { name: "", role: "Driver", access: "Staff" };
  const [form, setForm] = useState(blank);
  const [toast, setToast] = useState("");

  const submit = () => {
    if (!form.name) return;
    const initials = form.name
      .split(" ")
      .slice(0, 2)
      .map((part) => part[0]?.toUpperCase())
      .join("");

    setStaff([{ ...form, status: "active", initials }, ...staff]);
    setForm(blank);
    setOpen(false);
    flashToast(setToast, `${form.name} added`);
  };

  return (
    <div className="panel">
      {toast && <Toast text={toast} />}
      <div className="table-head">
        <div className="section-label" style={{ marginBottom: 0 }}>
          Team directory - {staff.length} people
        </div>
        <button className="btn-primary" onClick={() => setOpen(true)}>
          <Plus size={14} />
          New person
        </button>
      </div>

      <div className="people-grid">
        {staff.map((person) => (
          <div key={person.name} className="person-card">
            <div className="person-avatar">{person.initials}</div>
            <div className="person-main">
              <div className="person-name-row">
                <div>
                  <div className="mini-title">{person.name}</div>
                  <div className="mini-sub">
                    {person.role} - {person.access}
                  </div>
                </div>
                <Pill status={person.status} />
              </div>
            </div>
          </div>
        ))}
      </div>

      {open && (
        <Modal title="Add team member" onClose={() => setOpen(false)} onSubmit={submit} submitLabel="Add person">
          <Field label="Full name">
            <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="e.g. Ana Perez" />
          </Field>
          <div className="field-row">
            <Field label="Role">
              <input value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })} placeholder="e.g. Dispatcher" />
            </Field>
            <Field label="Access">
              <select value={form.access} onChange={(e) => setForm({ ...form, access: e.target.value })}>
                <option value="Staff">Staff</option>
                <option value="Admin">Admin</option>
              </select>
            </Field>
          </div>
          {role !== "Admin" && <div className="hint">Only admins can change user access in the real app.</div>}
        </Modal>
      )}
    </div>
  );
}

export default function App() {
  const [role, setRole] = useState("Admin");
  const [section, setSection] = useState("dashboard");
  const [stock, setStock] = useState(STOCK);
  const [receiving, setReceiving] = useState(RECEIVING);
  const [lines, setLines] = useState(RECEIVING_LINES);
  const [transactions, setTransactions] = useState(TRANSACTIONS);
  const [staff, setStaff] = useState(STAFF);
  const [query, setQuery] = useState("");

  const pageTitle = NAV_ITEMS.find((item) => item.id === section)?.label || "Dashboard";
  const filteredShipments = SHIPMENTS.filter((shipment) => {
    const term = query.trim().toLowerCase();
    if (!term) return true;
    return [shipment.id, shipment.client, shipment.origin, shipment.dest].some((value) => value.toLowerCase().includes(term));
  });

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <div className="brand-mark">
            <Truck size={18} style={{ color: '#ff8a3d' }} />
          </div>
          <div className="brand-copy">
            <div className="brand-name" style={{ fontSize: '0.9rem', lineHeight: '1.2', fontWeight: '800' }}>HAJI BARKAT KHAN JADOON</div>
            <div className="brand-sub" style={{ fontSize: '0.78rem', color: '#ff8a3d', fontWeight: '600' }}>GOODS TRANSPORT</div>
          </div>
        </div>

        <nav className="nav-list">
          {NAV_ITEMS.map((item) => (
            <button key={item.id} className={`nav-item ${section === item.id ? "active" : ""}`} onClick={() => setSection(item.id)}>
              <item.icon size={16} />
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="role-card">
            <div className="role-label">Session role</div>
            <div className="role-switch">
              <button className={role === "Admin" ? "active" : ""} onClick={() => setRole("Admin")}>
                Admin
              </button>
              <button className={role === "Staff" ? "active" : ""} onClick={() => setRole("Staff")}>
                Staff
              </button>
            </div>
          </div>
          <div className="role-note">
            <Shield size={14} />
            {role === "Admin" ? "Full operations access" : "Limited self-service access"}
          </div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div>
            <div className="eyebrow">Operations overview</div>
            <h1>{pageTitle}</h1>
          </div>
          <div className="topbar-tools">
            <div className="search-box">
              <Search size={16} />
              <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search shipments, clients, or hubs" />
            </div>
            <div className="topbar-pill">
              <MapPin size={14} />
              Live network
            </div>
          </div>
        </header>

        <section className="content-frame">
          {section === "dashboard" && <Dashboard role={role} stock={stock} receiving={receiving} transactions={transactions} staff={staff} />}
          {section === "shipments" && (
            <div>
              {query.trim() ? <div className="hint" style={{ marginBottom: 16 }}>{filteredShipments.length} shipment(s) matched your search.</div> : null}
              <ShipmentsView shipments={filteredShipments} />
            </div>
          )}
          {section === "inventory" && <StockView stock={stock} setStock={setStock} />}
          {section === "receiving" && <ReceivingView receiving={receiving} setReceiving={setReceiving} lines={lines} setLines={setLines} />}
          {section === "payments" && <PaymentsView role={role} transactions={transactions} setTransactions={setTransactions} />}
          {section === "people" && <PeopleView staff={staff} setStaff={setStaff} role={role} />}
        </section>
      </main>
    </div>
  );
}
