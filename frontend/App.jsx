// Root App Component managing active views and global inventory state
import { useState, useEffect } from "react";
import { Loader2 } from "lucide-react";
import Sidebar    from "./components/Sidebar.jsx";
import Header     from "./components/Header.jsx";
import Dashboard  from "./components/Dashboard.jsx";
import Inventory  from "./components/Inventory.jsx";
import Alerts     from "./components/Alerts.jsx";
import Reports    from "./components/Reports.jsx";
import ItemModal  from "./components/ItemModal.jsx";
import { initialInventory } from "./data/inventoryData.js";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:5000/api";

// Helper to automate JWT authentication and retries
async function getAuthToken() {
  let token = localStorage.getItem("gims_token");
  if (token) return token;

  const credentials = {
    email: "admin@gims.com",
    password: "adminpassword123",
  };

  try {
    // Attempt registration first
    const regRes = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: "Admin User",
        email: credentials.email,
        password: credentials.password,
        role: "admin",
      }),
    });

    if (regRes.status === 201) {
      // Login immediately on success
      const loginRes = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(credentials),
      });
      if (loginRes.ok) {
        const loginData = await loginRes.json();
        const t = loginData.data.token;
        localStorage.setItem("gims_token", t);
        return t;
      }
    } else {
      // Fallback: Login if user already exists
      const loginRes = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(credentials),
      });
      if (loginRes.ok) {
        const loginData = await loginRes.json();
        const t = loginData.data.token;
        localStorage.setItem("gims_token", t);
        return t;
      }
    }
  } catch (e) {
    console.error("Auth helper error:", e);
  }
  return null;
}

// Wrapper for all fetch requests including token verification
async function fetchAPI(path, options = {}) {
  let token = await getAuthToken();
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  let res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  // Handle token expiration / mismatch
  if (res.status === 401) {
    localStorage.removeItem("gims_token");
    token = await getAuthToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
      res = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers,
      });
    }
  }

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.message || `HTTP error ${res.status}`);
  }

  return res.json();
}

export default function App() {
  const [page, setPage]           = useState("dashboard");
  const [inventory, setInventory] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [editItem, setEditItem]   = useState(null);
  const [searchQuery, setSearch]  = useState("");
  const [loading, setLoading]     = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Dynamic API load inventory function
  const loadInventory = async () => {
    try {
      setLoading(true);
      const result = await fetchAPI("/products?page=1&limit=1000");
      if (result.success) {
        // Map database fields to UI keys (department_id -> department)
        const mapped = result.data.map((item) => ({
          id: item.id,
          name: item.name,
          department: item.department_id,
          stock: item.stock,
          unit: item.unit,
          cost: item.cost,
          status: item.status,
        }));
        setInventory(mapped);
      }
    } catch (e) {
      console.warn("Backend API unavailable, displaying initial inventory dataset:", e.message);
      setInventory(initialInventory);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInventory();
  }, []);

  // Lock background scroll on mobile when sidebar drawer is open
  useEffect(() => {
    if (sidebarOpen && typeof window !== "undefined" && window.innerWidth < 768) {
      document.body.style.overflow = "hidden";
    } else if (!modalOpen) {
      document.body.style.overflow = "";
    }
    return () => {
      if (!modalOpen) {
        document.body.style.overflow = "";
      }
    };
  }, [sidebarOpen, modalOpen]);

  // Lock background scroll when modal dialog is open
  useEffect(() => {
    if (modalOpen) {
      document.body.style.overflow = "hidden";
    } else if (!sidebarOpen || window.innerWidth >= 768) {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [modalOpen, sidebarOpen]);

  // Close sidebar drawer or modal dialog on Escape key press
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "Escape") {
        if (sidebarOpen) setSidebarOpen(false);
        if (modalOpen) setModalOpen(false);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [sidebarOpen, modalOpen]);

  // Automatically close sidebar drawer when resizing to desktop viewport
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 1024 && sidebarOpen) {
        setSidebarOpen(false);
      }
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [sidebarOpen]);

  const openAdd  = () => { setEditItem(null); setModalOpen(true); };
  const openEdit = (item) => { setEditItem(item); setModalOpen(true); };
  const closeModal = () => setModalOpen(false);

  const handleSave = async (formData) => {
    try {
      const payload = {
        name: formData.name,
        departmentId: formData.department,
        stock: Number(formData.stock),
        unit: formData.unit,
        cost: Number(formData.cost),
      };

      if (editItem) {
        await fetchAPI(`/products/${editItem.id}`, {
          method: "PUT",
          body: JSON.stringify(payload),
        });
      } else {
        await fetchAPI("/products", {
          method: "POST",
          body: JSON.stringify(payload),
        });
      }
      await loadInventory();
    } catch (e) {
      alert(`Error saving item: ${e.message}`);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Delete this item?")) {
      try {
        await fetchAPI(`/products/${id}`, {
          method: "DELETE",
        });
        await loadInventory();
      } catch (e) {
        alert(`Error deleting item: ${e.message}`);
      }
    }
  };

  const renderPage = () => {
    if (loading) {
      return (
        <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "60vh", color: "var(--gray-500)", gap: 12 }}>
          <Loader2 size={24} style={{ animation: "spin 1s linear infinite" }} aria-hidden="true" />
          <h3>Loading GIMS database...</h3>
        </div>
      );
    }
    switch (page) {
      case "dashboard": return <Dashboard inventory={inventory} onNavigate={setPage} />;
      case "inventory": return <Inventory inventory={inventory} onEdit={openEdit} onDelete={handleDelete} searchQuery={searchQuery} />;
      case "alerts":    return <Alerts inventory={inventory} />;
      case "reports":   return <Reports inventory={inventory} />;
      default:          return <Dashboard inventory={inventory} onNavigate={setPage} />;
    }
  };

  return (
    <div className={`app-wrapper ${sidebarOpen ? "sidebar-open" : ""}`}>
      {sidebarOpen && <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />}
      <Sidebar
        activePage={page}
        onNavigate={(p) => {
          setPage(p);
          setSidebarOpen(false);
        }}
        onAddItem={() => {
          openAdd();
          setSidebarOpen(false);
        }}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />
      <div className="main-content">
        <Header
          page={page}
          searchQuery={searchQuery}
          onSearch={setSearch}
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          sidebarOpen={sidebarOpen}
        />
        {renderPage()}
      </div>
      <ItemModal
        isOpen={modalOpen}
        onClose={closeModal}
        onSave={handleSave}
        editItem={editItem}
      />
    </div>
  );
}
