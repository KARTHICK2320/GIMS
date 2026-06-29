// Alerts Page Component displaying critical and low stock warning cards

export default function Alerts({ inventory }) {
  const critical = inventory.filter((i) => i.status === "critical");
  const lowStock = inventory.filter((i) => i.status === "low-stock");

  const AlertCard = ({ item }) => (
    <div className={`alert-card ${item.status}`}>
      <div className="alert-card-left">
        <span>{item.status === "critical" ? "⚠️" : "📦"}</span>
        <span>{item.name}</span>
      </div>
      <span className="alert-card-qty">{item.stock} {item.unit}</span>
    </div>
  );

  return (
    <div className="page-body fade-in">
      <div className="alerts-section">
        <div className="alerts-section-title critical">
          Critical Stock <span className="alerts-count">({critical.length})</span>
        </div>
        <div className="alerts-cards-grid">
          {critical.map((item) => <AlertCard key={item.id} item={item} />)}
        </div>
      </div>

      <div className="alerts-section">
        <div className="alerts-section-title low">
          Low Stock <span className="alerts-count">({lowStock.length})</span>
        </div>
        <div className="alerts-cards-grid">
          {lowStock.map((item) => <AlertCard key={item.id} item={item} />)}
        </div>
      </div>
    </div>
  );
}