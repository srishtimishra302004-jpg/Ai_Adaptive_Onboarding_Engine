import { Route, Routes } from "react-router-dom";
import { useState } from "react";
import UploadPage from "./pages/UploadPage";
import DashboardPage from "./pages/DashboardPage";

export default function App() {
  const [dark, setDark] = useState(true);

  return (
    <div className={`min-h-screen ${dark ? "dark bg-slate-900" : "bg-slate-50"}`}>
      
      <div className="flex justify-end p-4">
        <button
          onClick={() => setDark(!dark)}
          className="px-4 py-2 rounded bg-blue-600 text-white"
        >
          {dark ? "☀️ Light Mode" : "🌙 Dark Mode"}
        </button>
      </div>

      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </div>
  );
}