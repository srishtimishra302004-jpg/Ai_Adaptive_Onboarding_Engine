import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { analyze, analyzeText, uploadJd, uploadResume } from "../api";

export default function UploadPage() {
  const [resume, setResume] = useState(null);
  const [jd, setJd] = useState(null);
  const [goal, setGoal] = useState("AI Engineer");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleProcess = async () => {
    if (!resume || !jd) { setStatus("Please upload both resume and JD."); return; }
    try {
      setLoading(true);
      setStatus("Uploading resume...");
      await uploadResume(resume);
      setStatus("Uploading JD...");
      await uploadJd(jd);
      setStatus("Running analysis...");
      const { data } = await analyze(goal);
      sessionStorage.setItem("analysis", JSON.stringify(data));
      navigate("/dashboard");
    } catch {
      setStatus("Failed to process files. Please retry.");
    } finally { setLoading(false); }
  };

  const handleDemo = async () => {
    try {
      setLoading(true);
      setStatus("Running demo analysis...");
      const demoResume = `AI Engineer with 2+ years of experience in Python, SQL, and Machine Learning.
Built customer churn and recommendation models with Data Analysis workflows.
Developed FastAPI endpoints and containerized services using Docker.
Worked with basic cloud concepts and collaborated with cross-functional teams.`;
      const demoJd = `Looking for AI Engineer with Python, Machine Learning, SQL, AWS, Docker, and production deployment experience.
Must build end-to-end ML systems, monitor reliability, and deliver measurable business outcomes.`;
      const { data } = await analyzeText(demoResume, demoJd, goal);
      sessionStorage.setItem("analysis", JSON.stringify(data));
      navigate("/dashboard");
    } catch {
      setStatus("Demo analysis failed. Please retry.");
    } finally { setLoading(false); }
  };

  return (
    <div className="flex min-h-[calc(100vh-65px)] items-center justify-center px-4 py-12">
      <div className="w-full max-w-xl">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-slate-900 dark:text-white mb-3">
            AI Based Resume Skill Gap Analyzer
          </h1>
          <p className="text-lg text-slate-500 dark:text-slate-400">
            Upload your resume and job description to get a personalized skill gap analysis and learning roadmap.
          </p>
        </div>

        <div className="rounded-2xl bg-white dark:bg-slate-800 p-8 shadow-lg border border-slate-200 dark:border-slate-700">
          <div className="mb-6">
            <label className="block text-base font-semibold text-slate-700 dark:text-slate-200 mb-2">
              📄 Resume (PDF or TXT)
            </label>
            <input
              type="file"
              accept=".pdf,.txt"
              onChange={(e) => setResume(e.target.files?.[0])}
              className="block w-full text-sm text-slate-600 dark:text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 dark:file:bg-slate-700 dark:file:text-blue-300 hover:file:bg-blue-100 cursor-pointer"
            />
            {resume && <p className="mt-1 text-xs text-emerald-600 dark:text-emerald-400">✓ {resume.name}</p>}
          </div>

          <div className="mb-6">
            <label className="block text-base font-semibold text-slate-700 dark:text-slate-200 mb-2">
              📋 Job Description (PDF or TXT)
            </label>
            <input
              type="file"
              accept=".pdf,.txt"
              onChange={(e) => setJd(e.target.files?.[0])}
              className="block w-full text-sm text-slate-600 dark:text-slate-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 dark:file:bg-slate-700 dark:file:text-blue-300 hover:file:bg-blue-100 cursor-pointer"
            />
            {jd && <p className="mt-1 text-xs text-emerald-600 dark:text-emerald-400">✓ {jd.name}</p>}
          </div>

          <div className="mb-8">
            <label className="block text-base font-semibold text-slate-700 dark:text-slate-200 mb-2">
              🎯 Career Goal
            </label>
            <input
              type="text"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="e.g. AI Engineer, Data Scientist..."
              className="w-full rounded-xl border-2 border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white px-4 py-3 text-base focus:outline-none focus:border-blue-500 dark:focus:border-blue-400 transition-colors"
            />
          </div>

          <div className="flex flex-col gap-3">
            <button
              onClick={handleProcess}
              disabled={loading}
              className="w-full rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-bold py-3 text-base transition-colors shadow-md"
            >
              {loading ? "⏳ Processing..." : "🔍 Analyze My Resume"}
            </button>
            <button
              onClick={handleDemo}
              disabled={loading}
              className="w-full rounded-xl bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-bold py-3 text-base transition-colors shadow-md"
            >
              ✨ Try Demo (Auto-fill + Analyze)
            </button>
          </div>

          {status && (
            <div className="mt-5 rounded-lg bg-blue-50 dark:bg-slate-700 px-4 py-3 text-sm text-blue-700 dark:text-blue-300 font-medium">
              {status}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
