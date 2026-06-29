// Inventory Page Component showing full products list with filters and search
import { useState } from "react";

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
  return <span className="status-badge" style={{ color: cfg.color, background: cfg.bg }}>{cfg.label}</span>;
}

export default function Inventory({ inventory, onEdit, onDelete, searchQuery }) {
  const [activeDept, setActiveDept]     = useState("all");
  const [activeStatus, setActiveStatus] = useState("all");
  const [localSearch, setLocalSearch]   = useState(searchQuery || "");

  const getDeptName = (id) => departments.find((d) => d.id === id)?.name || id;

  const filtered = inventory.filter((item) => {
    const matchDept   = activeDept === "all" || item.department === activeDept;
    const matchStatus = activeStatus === "all" || item.status === activeStatus;
    const q = localSearch.toLowerCase();
    const matchSearch = !q || item.name.toLowerCase().includes(q) || getDeptName(item.department).toLowerCase().includes(q);
    return matchDept && matchStatus && matchSearch;
  });

  const counts = {
    all: inventory.length,
    "in-stock":  inventory.filter((i) => i.status === "in-stock").length,
    "low-stock": inventory.filter((i) => i.status === "low-stock").length,
    critical:    inventory.filter((i) => i.status === "critical").length,
  };

  const statusTabs = [
    { key: "all",       label: "All Items" },
    { key: "in-stock",  label: "In Stock" },
    { key: "low-stock", label: "Low Stock" },
    { key: "critical",  label: "Critical" },
  ];

  return (
    <div className="page-body fade-in">
      <div className="filter-bar">
        <span style={{ color: "var(--gray-400)", fontSize: 14 }}>🔍</span>
        <input
          type="text"
          placeholder="Search by name & Departments..."
          value={localSearch}
          onChange={(e) => setLocalSearch(e.target.value)}
        />
      </div>

      <div className="dept-filters">
        <span className="dept-label">Department</span>
        <button className={`dept-btn ${activeDept === "all" ? "active" : ""}`} onClick={() => setActiveDept("all")}>All</button>
        {departments.map((d) => (
          <button
            key={d.id}
            className={`dept-btn ${activeDept === d.id ? "active" : ""}`}
            onClick={() => setActiveDept(d.id)}
          >{d.icon} {d.name}</button>
        ))}
      </div>

      <div className="status-tabs">
        {statusTabs.map((tab) => (
          <button
            key={tab.key}
            className={`status-tab ${activeStatus === tab.key ? "active" : ""}`}
            onClick={() => setActiveStatus(tab.key)}
          >{tab.label} <span className="count">{counts[tab.key]}</span></button>
        ))}
      </div>

      <div className="inventory-table-wrapper">
        <table className="inventory-table">
          <thead>
            <tr>
              <th>Product</th><th>Department</th><th>Stock</th><th>Cost</th><th>Status</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr><td colSpan={6} style={{ textAlign: "center", color: "var(--gray-400)", padding: 40 }}>No items found.</td></tr>
            ) : filtered.map((item) => (
              <tr key={item.id}>
                <td className="product-name">{item.name}</td>
                <td className="dept-text">{getDeptName(item.department)}</td>
                <td>{item.stock} {item.unit}</td>
                <td>₹{item.cost.toLocaleString("en-IN")}</td>
                <td><StatusBadge status={item.status} /></td>
                <td>
                  <div className="action-btns">
                    <button className="btn-edit" onClick={() => onEdit(item)}>Edit</button>
                    <button className="btn-delete" onClick={() => onDelete(item.id)}>Delete</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}