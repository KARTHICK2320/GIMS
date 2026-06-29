import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";

// Import CSS custom properties and design tokens
import "./css/variables.css";

// Import CSS styles in correct cascade order
import "./css/base.css";
import "./css/layout.css";
import "./css/dashboard.css";
import "./css/inventory.css";
import "./css/alerts.css";
import "./css/reports.css";
import "./css/modal.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
