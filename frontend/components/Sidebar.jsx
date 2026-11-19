// Sidebar Navigation Component with page switching routes
import {
  LayoutDashboard,
  Package,
  Bell,
  ChartNoAxesCombined,
  Plus,
  X,
} from "lucide-react";

const navItems = [
  { id: "dashboard", label: "Dashboard", Icon: LayoutDashboard },
  { id: "inventory", label: "Inventory",  Icon: Package },
  { id: "alerts",    label: "Alerts",     Icon: Bell },
  { id: "reports",   label: "Reports",    Icon: ChartNoAxesCombined },
];

export default function Sidebar({ activePage, onNavigate, onAddItem, isOpen, onClose }) {
  return (
    <aside className={`sidebar ${isOpen ? "open" : ""}`}>
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">
          <Package size={20} color="#fff" aria-hidden="true" />
        </div>
        <div className="sidebar-logo-text">
          <h2>Inventory</h2>
          <span>Management</span>
        </div>
        <button
          className="sidebar-close-btn"
          onClick={onClose}
          aria-label="Close sidebar"
          type="button"
        >
          <X size={18} aria-hidden="true" />
        </button>
      </div>
      <button className="sidebar-add-btn" onClick={onAddItem} type="button">
        <Plus size={16} aria-hidden="true" /> Add New Item
      </button>
      <nav className="sidebar-nav" aria-label="Main Navigation">
        {navItems.map((item) => {
          const ItemIcon = item.Icon;
          return (
            <button
              key={item.id}
              type="button"
              className={`nav-item ${activePage === item.id ? "active" : ""}`}
              onClick={() => onNavigate(item.id)}
              aria-current={activePage === item.id ? "page" : undefined}
            >
              <span className="nav-icon">
                <ItemIcon size={18} aria-hidden="true" />
              </span>
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
}
