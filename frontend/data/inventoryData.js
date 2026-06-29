
// Central Data Store for Inventory Management

export const departments = [
  { id: "grocery", name: "Grocery", icon: "🛒", color: "#3B82F6" },
  { id: "fruits-vegetables", name: "Fruits & Vegetables", icon: "🥬", color: "#22C55E" },
  { id: "dairy", name: "Dairy Products", icon: "🧀", color: "#EAB308" },
  { id: "beverages", name: "Beverages", icon: "🥤", color: "#EF4444" },
  { id: "bakery", name: "Bakery", icon: "📦", color: "#F97316" },
  { id: "household", name: "Household", icon: "🏠", color: "#8B5CF6" },
];

export const initialInventory = [
  { id: 1, name: "Rice", department: "grocery", stock: 200, unit: "Nos", cost: 500000, status: "in-stock" },
  { id: 2, name: "Paste", department: "grocery", stock: 50, unit: "Nos", cost: 2000, status: "low-stock" },
  { id: 3, name: "Shampoo", department: "grocery", stock: 200, unit: "Nos", cost: 500000, status: "critical" },
  { id: 4, name: "Sugar", department: "grocery", stock: 47, unit: "Kg", cost: 12000, status: "low-stock" },
  { id: 5, name: "Tea Powder", department: "grocery", stock: 34, unit: "Kg", cost: 8500, status: "low-stock" },
  { id: 6, name: "Soap", department: "grocery", stock: 124, unit: "Pcs", cost: 6200, status: "in-stock" },
  { id: 7, name: "Soft Drinks", department: "beverages", stock: 141, unit: "Nos", cost: 14100, status: "in-stock" },
  { id: 8, name: "Milk", department: "dairy", stock: 80, unit: "Ltr", cost: 4000, status: "low-stock" },
  { id: 9, name: "Cheese", department: "dairy", stock: 25, unit: "Kg", cost: 12500, status: "low-stock" },
  { id: 10, name: "Apples", department: "fruits-vegetables", stock: 50, unit: "Kg", cost: 10000, status: "in-stock" },
  { id: 11, name: "Tomatoes", department: "fruits-vegetables", stock: 30, unit: "Kg", cost: 3000, status: "low-stock" },
  { id: 12, name: "Onions", department: "fruits-vegetables", stock: 100, unit: "Kg", cost: 5000, status: "in-stock" },
  { id: 13, name: "Bread", department: "bakery", stock: 60, unit: "Pcs", cost: 1800, status: "low-stock" },
  { id: 14, name: "Cake", department: "bakery", stock: 15, unit: "Pcs", cost: 7500, status: "critical" },
  { id: 15, name: "Butter", department: "dairy", stock: 40, unit: "Pcs", cost: 3200, status: "low-stock" },
  { id: 16, name: "Juice", department: "beverages", stock: 90, unit: "Nos", cost: 9000, status: "in-stock" },
  { id: 17, name: "Water", department: "beverages", stock: 200, unit: "Nos", cost: 2000, status: "in-stock" },
  { id: 18, name: "Detergent", department: "household", stock: 75, unit: "Pcs", cost: 7500, status: "low-stock" },
  { id: 19, name: "Mop", department: "household", stock: 10, unit: "Pcs", cost: 3000, status: "critical" },
  { id: 20, name: "Broom", department: "household", stock: 20, unit: "Pcs", cost: 1600, status: "low-stock" },
  { id: 21, name: "Floor Cleaner", department: "household", stock: 45, unit: "Nos", cost: 4500, status: "low-stock" },
];

export const statusConfig = {
  "in-stock":  { label: "In Stock",  color: "#22C55E", bg: "#F0FDF4", border: "#BBF7D0" },
  "low-stock": { label: "Low Stock", color: "#F59E0B", bg: "#FFFBEB", border: "#FDE68A" },
  "critical":  { label: "Critical",  color: "#EF4444", bg: "#FEF2F2", border: "#FECACA" },
};
