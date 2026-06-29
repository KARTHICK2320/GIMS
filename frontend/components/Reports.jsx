// Reports Page Component displaying inventory valuation metrics and status graphs

const departments = [
  { id: "grocery", name: "Grocery", icon: "🛒" },
  { id: "fruits-vegetables", name: "Fruits & Vegetables", icon: "🥬" },
  { id: "dairy", name: "Dairy Products", icon: "🧀" },
  { id: "beverages", name: "Beverages", icon: "🥤" },
  { id: "bakery", name: "Bakery", icon: "📦" },
  { id: "household", name: "Household", icon: "🏠" },
];

export default function Reports({ inventory }) {
  const totalValue = inventory.reduce((s, i) => s + i.cost, 0);
  const total      = inventory.length;
  const inStock    = inventory.filter((i) => i.status === "in-stock").length;
  const lowStock   = inventory.filter((i) => i.status === "low-stock").length;
  const critical   = inventory.filter((i) => i.status === "critical").length;

  const deptItems = departments.map((d) => ({
    ...d, count: inventory.filter((i) => i.department === d.id).length,
  }));

  return (
    <div className="page-body fade-in">
      <div className="reports-summary-grid">
        <div className="report-stat-card">
          <div className="report-stat-label">Total Inventory Value</div>
          <div className="report-stat-value">₹{totalValue.toLocaleString("en-IN")}</div>
        </div>
        <div className="report-stat-card">
          <div className="report-stat-label">Total Products</div>
          <div className="report-stat-value">{total}</div>
        </div>
        <div className="report-stat-card">
          <div className="report-stat-label">Departments</div>
          <div className="report-stat-value">{departments.length}</div>
        </div>
      </div>

      <div className="report-section">
        <div className="report-section-title">Stock Distribution</div>
        {[
          { label: "In Stock",  count: inStock,  cls: "green" },
          { label: "Low Stock", count: lowStock, cls: "amber" },
          { label: "Critical",  count: critical, cls: "red"   },
        ].map((row) => (
          <div key={row.label} className="dist-bar-row">
            <div className="dist-bar-label">{row.label}</div>
            <div className="dist-bar-track">
              <div className={`dist-bar-fill ${row.cls}`} style={{ width: `${(row.count / total) * 100}%` }} />
            </div>
            <div className="dist-bar-count">{row.count}</div>
          </div>
        ))}
      </div>

      <div className="report-section">
        <div className="report-section-title">By Department</div>
        <div className="dept-report-grid">
          {deptItems.map((d) => (
            <div key={d.id} className="dept-report-card">
              <div className="dept-report-icon">{d.icon}</div>
              <div>
                <div className="dept-report-name">{d.name}</div>
                <div className="dept-report-count">{d.count} items</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}