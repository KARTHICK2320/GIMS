// Header Component displaying active page titles and global search bar

const pageTitles = {
  dashboard: { title: "Dashboard",  subtitle: "Overview of your inventory status" },
  inventory: { title: "Inventory",  subtitle: "Manage all items" },
  alerts:    { title: "Alerts",     subtitle: "Items that need attention" },
  reports:   { title: "Reports",    subtitle: "Inventory analytics and summaries" },
};

export default function Header({ page, searchQuery, onSearch }) {
  const info = pageTitles[page] || pageTitles.dashboard;
  return (
    <header className="header">
      <div className="header-title">
        <h1>{info.title}</h1>
        <p>{info.subtitle}</p>
      </div>
      <div className="header-actions">
        <div className="search-box">
          <span style={{ color: "var(--gray-400)", fontSize: 14 }}>🔍</span>
          <input
            type="text"
            placeholder="Search items..."
            value={searchQuery}
            onChange={(e) => onSearch(e.target.value)}
          />
        </div>
        <div className="header-icon-btn" title="Notifications">🔔</div>
        <div className="header-icon-btn" title="Settings">⚙️</div>
      </div>
    </header>
  );
}
