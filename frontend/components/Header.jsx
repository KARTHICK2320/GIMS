// Header Component displaying active page titles and global search bar
import { Menu, Search, Bell, Settings } from "lucide-react";

const pageTitles = {
  dashboard: { title: "Dashboard",  subtitle: "Overview of your inventory status" },
  inventory: { title: "Inventory",  subtitle: "Manage all items" },
  alerts:    { title: "Alerts",     subtitle: "Items that need attention" },
  reports:   { title: "Reports",    subtitle: "Inventory analytics and summaries" },
};

export default function Header({ page, searchQuery, onSearch, onToggleSidebar, sidebarOpen }) {
  const info = pageTitles[page] || pageTitles.dashboard;
  return (
    <header className="header">
      <div className="header-left">
        <button
          className="sidebar-toggle-btn"
          onClick={onToggleSidebar}
          aria-label="Toggle navigation menu"
          aria-expanded={Boolean(sidebarOpen)}
          type="button"
        >
          <Menu size={22} aria-hidden="true" />
        </button>
        <div className="header-title">
          <h1>{info.title}</h1>
          <p>{info.subtitle}</p>
        </div>
      </div>
      <div className="header-actions">
        <div className="search-box">
          <Search size={15} color="var(--gray-400)" aria-hidden="true" style={{ flexShrink: 0 }} />
          <input
            type="text"
            placeholder="Search items..."
            value={searchQuery}
            onChange={(e) => onSearch(e.target.value)}
          />
        </div>
        <button
          type="button"
          className="header-icon-btn"
          title="Notifications"
          aria-label="Notifications"
        >
          <Bell size={17} aria-hidden="true" />
        </button>
        <button
          type="button"
          className="header-icon-btn"
          title="Settings"
          aria-label="Settings"
        >
          <Settings size={17} aria-hidden="true" />
        </button>
      </div>
    </header>
  );
}
