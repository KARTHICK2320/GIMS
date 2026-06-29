// Dashboard Page Component showing statistics, alerts, and department overview

const departments = [
  { id: "grocery", name: "Grocery", icon: "🛒" },
  { id: "fruits-vegetables", name: "Fruits & Vegetables", icon: "🥬" },
  { id: "dairy", name: "Dairy Products", icon: "🧀" },
  { id: "beverages", name: "Beverages", icon: "🥤" },
  { id: "bakery", name: "Bakery", icon: "📦" },
  { id: "household", name: "Household", icon: "🏠" },
];

const statusConfig = {
  "in-stock":  { label: "In Stock",  color: "#22C55E", bg: "#F0FDF4" },
  "low-stock": { label: "Low Stock", color: "#F59E0B", bg: "#FFFBEB" },
  "critical":  { label: "Critical",  color: "#EF4444", bg: "#FEF2F2" },
};

function StatusBadge({ status }) {
  const cfg = statusConfig[status];
  return (
    <span className="status-badge" style={{ color: cfg.color, background: cfg.bg }}>
      {cfg.label}
    </span>
  );
}

export default function Dashboard({ inventory, onNavigate }) {
  const total    = inventory.length;
  const critical = inventory.filter((i) => i.status === "critical").length;
  const lowStock = inventory.filter((i) => i.status === "low-stock").length;
  const inStock  = inventory.filter((i) => i.status === "in-stock").length;
  const totalValue = inventory.reduce((s, i) => s + i.cost, 0);
  const alertItems = inventory.filter((i) => i.status !== "in-stock").slice(0, 4);
  const getDeptName = (id) => departments.find((d) => d.id === id)?.name || id;
  const deptCounts = departments.map((d) => ({
    ...d, count: inventory.filter((i) => i.department === d.id).length,
  }));

  return (
    <div className="page-body fade-in">
      <div className="stats-grid">
        {[
          { cls: "stat-blue",  label: "Total Items",      val: total,    icon: "box", ibg: "#BFDBFE" },
          { cls: "stat-red",   label: "Critical Stock",   val: critical, icon: "warn",ibg: "#FECACA" },
          { cls: "stat-amber", label: "Low Stock Alerts", val: lowStock, icon: "down",ibg: "#FDE68A" },
          { cls: "stat-green", label: "In Stock",         val: inStock,  icon: "ok",  ibg: "#BBF7D0" },
        ].map(({ cls, label, val, ibg }) => (
          <div key={label} className={`stat-card ${cls}`}>
            <div className="stat-card-header">
              <span className="stat-card-label">{label}</span>
              <div className="stat-card-icon" style={{ background: ibg }}>
                {cls === "stat-blue" ? "📦" : cls === "stat-red" ? "⚠️" : cls === "stat-amber" ? "📉" : "✅"}
              </div>
            </div>
            <div className="stat-card-value">{val}</div>
          </div>
        ))}
      </div>

      <div className="section-title">Stock Alerts</div>
      <div className="alerts-grid">
        {alertItems.map((item) => (
          <div key={item.id} className={`alert-chip ${item.status === "critical" ? "critical" : "low"}`}>
            <div className="alert-chip-left">
              <span>{item.status === "critical" ? "⚠️" : "📦"}</span>
              <span>{item.name}</span>
            </div>
            <span className="alert-chip-value">{item.stock} {item.unit}</span>
          </div>
        ))}
      </div>

      <div className="dashboard-grid">
        <div className="departments-panel">
          <div className="section-title">Departments</div>
          <div className="dept-list">
            {deptCounts.map((d) => (
              <div key={d.id} className="dept-item" onClick={() => onNavigate("inventory")}>
                <div className="dept-item-left">
                  <span>{d.icon}</span><span>{d.name}</span>
                </div>
                <span className="dept-badge">{d.count}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="inventory-panel">
          <div className="inventory-panel-header">
            <div className="section-title" style={{ marginBottom: 0 }}>Inventory</div>
            <span className="panel-total">Total Value: ₹{totalValue.toLocaleString("en-IN")}</span>
          </div>
          <table className="inv-table">
            <thead>
              <tr><th>Product</th><th>Department</th><th>Stock</th><th>Cost</th><th>Status</th></tr>
            </thead>
            <tbody>
              {inventory.slice(0, 8).map((item) => (
                <tr key={item.id}>
                  <td>{item.name}</td>
                  <td style={{ color: "var(--gray-500)", fontSize: 13 }}>{getDeptName(item.department)}</td>
                  <td>{item.stock} {item.unit}</td>
                  <td>₹{item.cost.toLocaleString("en-IN")}</td>
                  <td><StatusBadge status={item.status} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}