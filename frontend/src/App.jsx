import { Route, Routes } from "react-router-dom";
import { useTheme } from "./ThemeContext";
import UploadPage from "./pages/UploadPage";
import DashboardPage from "./pages/DashboardPage";

export default function App() {
  const { dark, toggle } = useTheme();

  return (
    <div className="min-h-screen bg-slate-100 dark:bg-slate-900 transition-colors duration-300">
      <nav className="sticky top-0 z-50 bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 shadow-sm">
        <div className="flex items-center justify-between px-4 py-3 min-w-0">
          <span className="text-base font-bold text-slate-800 dark:text-white truncate mr-4">
            🧠 AI Onboarding Engine
          </span>
          <button
            onClick={toggle}
            style={{ whiteSpace: "nowrap", flexShrink: 0 }}
            className="rounded-full px-4 py-2 text-sm font-semibold border-2 border-slate-300 dark:border-slate-500 bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-100 hover:bg-blue-50 dark:hover:bg-slate-600 transition-all"
          >
            {dark ? "☀️ Light" : "🌙 Dark"}
          </button>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </div>
  );
}
