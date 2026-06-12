// TODO (Day 22): All Axios API calls to the backend
// Functions: querySafety(), getRoutes(), submitSignal(), getSignals()
import axios from "axios";

const BASE_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:5000";

// placeholder — real implementations added on Day 22
export const api = axios.create({ baseURL: BASE_URL });
