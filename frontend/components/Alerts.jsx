// Alerts Page Component displaying critical and low stock warning cards
import { AlertTriangle, Package, CheckCircle2 } from "lucide-react";

export default function Alerts({ inventory }) {
  const critical = inventory.filter((i) => i.status === "critical");
  const lowStock = inventory.filter((i) => i.status === "low-stock");

  const AlertCard = ({ item }) => (
    <div className={`alert-card ${item.status}`}>
      <div className="alert-card-left">
        {item.status === "critical" ? (
          <AlertTriangle size={16} color="var(--red)" aria-hidden="true" />
        ) : (
          <Package size={16} color="var(--amber)" aria-hidden="true" />
        )}
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
          {critical.length === 0 ? (
            <div style={{ color: "var(--gray-400)", fontSize: 13.5, padding: "12px 0", display: "flex", alignItems: "center", gap: 8 }}>
              <CheckCircle2 size={16} color="var(--green)" aria-hidden="true" /> No critical stock items.
            </div>
          ) : (
            critical.map((item) => <AlertCard key={item.id} item={item} />)
          )}
        </div>
      </div>

      <div className="alerts-section">
        <div className="alerts-section-title low">
          Low Stock <span className="alerts-count">({lowStock.length})</span>
        </div>
        <div className="alerts-cards-grid">
          {lowStock.length === 0 ? (
            <div style={{ color: "var(--gray-400)", fontSize: 13.5, padding: "12px 0", display: "flex", alignItems: "center", gap: 8 }}>
              <CheckCircle2 size={16} color="var(--green)" aria-hidden="true" /> No low stock items.
            </div>
          ) : (
            lowStock.map((item) => <AlertCard key={item.id} item={item} />)
          )}
        </div>
      </div>
    </div>
  );
}
