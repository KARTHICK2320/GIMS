// Add/Edit Item Modal Component for inventory management form
import { useState, useEffect } from "react";
import { X } from "lucide-react";
import { departments } from "../data/inventoryData.js";

const defaultForm = {
  name: "", department: "", stock: "", unit: "Nos", cost: "", status: "in-stock",
};

export default function ItemModal({ isOpen, onClose, onSave, editItem }) {
  const [form, setForm] = useState(defaultForm);

  useEffect(() => {
    if (editItem) setForm({ ...editItem, cost: String(editItem.cost) });
    else setForm(defaultForm);
  }, [editItem, isOpen]);

  if (!isOpen) return null;

  const set = (key, val) => setForm((f) => ({ ...f, [key]: val }));

  const handleSave = () => {
    if (!form.name || !form.department || !form.stock || !form.cost) {
      alert("Please fill in all required fields.");
      return;
    }
    onSave({ ...form, stock: Number(form.stock), cost: Number(form.cost) });
    onClose();
  };

  return (
    <div
      className="modal-overlay"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="modal-box">
        <div className="modal-header">
          <div>
            <div className="modal-title">{editItem ? "Edit Item" : "Add New Item"}</div>
            <div className="modal-subtitle">
              Fill in the details to {editItem ? "update" : "add"} an inventory item.
            </div>
          </div>
          <button
            type="button"
            className="modal-close"
            onClick={onClose}
            aria-label="Close modal"
          >
            <X size={18} aria-hidden="true" />
          </button>
        </div>

        <div className="form-group">
          <label className="form-label">Product Name</label>
          <input
            className="form-input"
            placeholder="e.g. Rice"
            value={form.name}
            onChange={(e) => set("name", e.target.value)}
          />
        </div>

        <div className="form-group">
          <label className="form-label">Department</label>
          <select
            className="form-select"
            value={form.department}
            onChange={(e) => set("department", e.target.value)}
          >
            <option value="">Select department</option>
            {departments.map((d) => (
              <option key={d.id} value={d.id}>{d.name}</option>
            ))}
          </select>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Stock</label>
            <input
              className="form-input"
              placeholder="e.g. 200"
              type="number"
              min="0"
              step="1"
              value={form.stock}
              onChange={(e) => {
                const val = e.target.value;
                if (val === "") {
                  set("stock", "");
                  return;
                }
                const num = Number(val);
                set("stock", num < 0 ? "0" : val);
              }}
            />
          </div>
          <div className="form-group">
            <label className="form-label">Unit</label>
            <select
              className="form-select"
              value={form.unit}
              onChange={(e) => set("unit", e.target.value)}
            >
              <option>Nos</option>
              <option>Kg</option>
              <option>Ltr</option>
              <option>Pcs</option>
            </select>
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Cost (₹)</label>
          <input
            className="form-input"
            placeholder="e.g. 5000"
            type="number"
            min="0"
            step="0.01"
            value={form.cost}
            onChange={(e) => {
              const val = e.target.value;
              if (val === "") {
                set("cost", "");
                return;
              }
              const num = Number(val);
              set("cost", num < 0 ? "0" : val);
            }}
          />
        </div>

        <div className="form-group">
          <label className="form-label">Status</label>
          <select
            className="form-select"
            value={form.status}
            onChange={(e) => set("status", e.target.value)}
          >
            <option value="in-stock">In Stock</option>
            <option value="low-stock">Low Stock</option>
            <option value="critical">Critical</option>
          </select>
        </div>

        <div className="modal-actions">
          <button type="button" className="btn-cancel" onClick={onClose}>Cancel</button>
          <button type="button" className="btn-submit" onClick={handleSave}>
            {editItem ? "Save Changes" : "Add Item"}
          </button>
        </div>
      </div>
    </div>
  );
}
