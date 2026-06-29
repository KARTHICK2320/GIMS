// Sidebar Navigation Component with page switching routes

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: "⊞" },
  { id: "inventory", label: "Inventory",  icon: "📋" },
  { id: "alerts",    label: "Alerts",     icon: "🔔" },
  { id: "reports",   label: "Reports",    icon: "📊" },
];

export default function Sidebar({ activePage, onNavigate, onAddItem }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">📦</div>
        <div className="sidebar-logo-text">
          <h2>Inventory</h2>
          <span>Management</span>
        </div>
      </div>
      <button className="sidebar-add-btn" onClick={onAddItem}>
        <span>+</span> Add New Item
      </button>
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <div
            key={item.id}
            className={`nav-item ${activePage === item.id ? "active" : ""}`}
            onClick={() => onNavigate(item.id)}
          >
            <span className="nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </div>
        ))}
      </nav>
    </aside>
  );
}
