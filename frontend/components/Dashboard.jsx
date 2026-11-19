// Dashboard Page Component showing statistics, alerts, and department overview
import {
  Boxes,
  AlertTriangle,
  TrendingDown,
  CircleCheck,
  Package,
} from "lucide-react";
import {
  departments,
  DepartmentIcon,
  StatusBadge,
} from "../data/inventoryData.js";

const statCardsConfig = [
  {
    cls: "stat-blue",
    label: "Total Items",
    Icon: Boxes,
    iconColor: "var(--primary)",
    ibg: "#BFDBFE",
  },
  {
    cls: "stat-red",
    label: "Critical Stock",
    Icon: AlertTriangle,
    iconColor: "var(--red)",
    ibg: "#FECACA",
  },
  {
    cls: "stat-amber",
    label: "Low Stock Alerts",
    Icon: TrendingDown,
    iconColor: "var(--amber)",
    ibg: "#FDE68A",
  },
  {
    cls: "stat-green",
    label: "In Stock",
    Icon: CircleCheck,
    iconColor: "var(--green)",
    ibg: "#BBF7D0",
  },
];

export default function Dashboard({ inventory, onNavigate }) {
  const total      = inventory.length;
  const critical   = inventory.filter((i) => i.status === "critical").length;
  const lowStock   = inventory.filter((i) => i.status === "low-stock").length;
  const inStock    = inventory.filter((i) => i.status === "in-stock").length;
  const totalValue = inventory.reduce((s, i) => s + i.cost, 0);
  const alertItems = inventory.filter((i) => i.status !== "in-stock").slice(0, 4);
  const getDeptName = (id) => departments.find((d) => d.id === id)?.name || id;
  const deptCounts = departments.map((d) => ({
    ...d,
    count: inventory.filter((i) => i.department === d.id).length,
  }));

  const statValues = {
    "Total Items": total,
    "Critical Stock": critical,
    "Low Stock Alerts": lowStock,
    "In Stock": inStock,
  };

  return (
    <div className="page-body fade-in">
      <div className="stats-grid">
        {statCardsConfig.map(({ cls, label, Icon, iconColor, ibg }) => (
          <div key={label} className={`stat-card ${cls}`}>
            <div className="stat-card-header">
              <span className="stat-card-label">{label}</span>
              <div className="stat-card-icon" style={{ background: ibg }}>
                <Icon size={18} color={iconColor} aria-hidden="true" />
              </div>
            </div>
            <div className="stat-card-value">{statValues[label]}</div>
          </div>
        ))}
      </div>

      <div className="section-title">Stock Alerts</div>
      <div className="alerts-grid">
        {alertItems.map((item) => (
          <div key={item.id} className={`alert-chip ${item.status === "critical" ? "critical" : "low"}`}>
            <div className="alert-chip-left">
              {item.status === "critical" ? (
                <AlertTriangle size={15} color="var(--red)" aria-hidden="true" />
              ) : (
                <Package size={15} color="var(--amber)" aria-hidden="true" />
              )}
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
              <div
                key={d.id}
                className="dept-item"
                onClick={() => onNavigate("inventory")}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => e.key === "Enter" && onNavigate("inventory")}
              >
                <div className="dept-item-left">
                  <DepartmentIcon id={d.id} size={16} />
                  <span>{d.name}</span>
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
          <div className="inv-table-wrapper">
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
    </div>
  );
}
