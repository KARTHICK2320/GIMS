# GIMS — Grocery Inventory Management System

A complete, modular frontend built with **React + Vite + Pure CSS**.

---

## Project Structure

```
GIMS/
├── html/
│   └── index.html              ← HTML entry point
├── css/
│   ├── variables.css           ← CSS custom properties / design tokens
│   ├── base.css                ← Reset, animations & utility classes
│   ├── layout.css              ← Sidebar, Header, page layout
│   ├── dashboard.css           ← Dashboard page styles
│   ├── inventory.css           ← Inventory page styles
│   ├── alerts.css              ← Alerts page styles
│   ├── reports.css             ← Reports page styles
│   └── modal.css               ← Add/Edit modal styles
├── components/
│   ├── Sidebar.jsx             ← Navigation sidebar
│   ├── Header.jsx              ← Top header with global search
│   ├── Dashboard.jsx           ← Stats, alerts & dept overview
│   ├── Inventory.jsx           ← Full table with search & filters
│   ├── Alerts.jsx              ← Critical & low stock grouped view
│   ├── Reports.jsx             ← Analytics, bars & dept breakdown
│   └── ItemModal.jsx           ← Add / Edit item form modal
├── data/
│   └── inventoryData.js        ← Shared mock data & constants
├── App.jsx                     ← Root component & state management
├── main.jsx                    ← React entry point + CSS imports
├── package.json
└── vite.config.js
```

---

## Features

| Page | What it does |
|------|-------------|
| **Dashboard** | Stat cards (Total, Critical, Low Stock, In Stock), stock alert chips, department list, mini inventory table |
| **Inventory** | Full sortable table, search by name/dept, filter by department tabs, filter by status tabs, Edit & Delete per row |
| **Alerts** | Critical items (red) and Low Stock items (amber) in a card grid |
| **Reports** | Total inventory value, product count, departments count, stock distribution bar chart, per-department breakdown |
| **Add / Edit Modal** | Form with Product Name, Department, Stock + Unit, Cost, Status — accessible from sidebar button or Edit row action |

---

## Getting Started

```bash
# 1. Install dependencies
npm install

# 2. Start dev server
npm run dev
# Opens → http://localhost:3000

# 3. Build for production
npm run build
```

---

## Tech Stack

- **React 18** — UI components & state
- **Vite 5** — Dev server & bundler
- **Pure CSS** — No frameworks; modular files with CSS custom properties
- **DM Sans** — Google Font for clean, modern typography

---

## CSS Architecture

All styles use **CSS custom properties** defined in `variables.css`.  
Each page/module has its own dedicated CSS file — no global pollution.

Load order in `main.jsx`:
1. `variables.css` — must be first
2. `base.css`
3. `layout.css`
4. Page CSS files
5. `modal.css` — overlay on top

---

## Data

`data/inventoryData.js` exports:
- `initialInventory` — 21 pre-seeded products across 6 departments
- `departments` — department config (id, name, icon, color)
- `statusConfig` — status display config (label, color, bg, border)

All state lives in `App.jsx` and is passed down via props.
