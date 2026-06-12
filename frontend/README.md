# Frontend — React App

Deployed to **Vercel** at safescope-ai.vercel.app

## Stack
- React.js + Tailwind CSS
- React Leaflet (maps + heatmap layers)
- Chart.js / Recharts (risk score charts)
- Axios (API calls to backend)

## Pages (src/pages/)
| File | Page | What It Does |
|---|---|---|
| Home.jsx | Home | Landing page, project intro |
| AskSafeScope.jsx | Ask SafeScope | Main query page — type area/time/persona, get risk scores + RAG explanation |
| CitySafetyTwin.jsx | City Safety Twin | Interactive map with toggleable risk layers |
| SaferRoute.jsx | Safer Route | Compare routes by safety score |
| CommunitySignals.jsx | Community Signals | Submit and view trust-scored safety reports |
| Admin.jsx | Admin | Upload NCRB data, trigger model training |

## Components (src/components/)
| File | What It Does |
|---|---|
| MapView.jsx | Base Leaflet map wrapper |
| RiskCard.jsx | Displays one risk score (0–100) with colour coding |
| RoutePanel.jsx | Shows route comparison with safety rankings |
| QueryBox.jsx | Input box that accepts Hindi + English |
| HeatmapLayer.jsx | Renders crime heatmap on the map |
| TrustBadge.jsx | Shows user trust score badge on community signals |

## Build
```bash
npm install
npm start       # dev server on localhost:3000
npm run build   # production build
```
