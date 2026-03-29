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
    if (!resume || !jd) {
      setStatus("Please upload both resume and JD.");
      return;
    }
    try {
      setLoading(true);
      setStatus("Processing...");
      await uploadResume(resume);
      setStatus("Resume upload successful.");
      await uploadJd(jd);
      setStatus("JD upload successful. Running analysis...");
      const { data } = await analyze(goal);
      setStatus("Analysis complete.");
      sessionStorage.setItem("analysis", JSON.stringify(data));
      navigate("/dashboard");
    } catch (error) {
      setStatus("Failed to process files. Please retry.");
    } finally {
      setLoading(false);
    }
  };

  const handleDemo = async () => {
    try {
      setLoading(true);
      setStatus("Loading demo profile and analyzing...");
      const demoResume = `AI Engineer with 2+ years of experience in Python, SQL, and Machine Learning.
Built customer churn and recommendation models with Data Analysis workflows.
Developed FastAPI endpoints and containerized services using Docker.
Worked with basic cloud concepts and collaborated with cross-functional teams.`;
      const demoJd = `Looking for AI Engineer with Python, Machine Learning, SQL, AWS, Docker, and production deployment experience.
Must build end-to-end ML systems, monitor reliability, and deliver measurable business outcomes.`;
      const { data } = await analyzeText(demoResume, demoJd, goal);
      setStatus("Demo analysis complete.");
      sessionStorage.setItem("analysis", JSON.stringify(data));
      navigate("/dashboard");
    } catch (error) {
      setStatus("Demo analysis failed. Please retry.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="text-3xl font-bold text-slate-900">AI Adaptive Onboarding Engine</h1>
      <p className="mt-2 text-slate-600">Upload your resume and target job description to get a personalized roadmap.</p>

      <div className="mt-8 rounded-xl bg-white p-6 shadow">
        <label className="mb-2 block text-sm font-medium text-slate-700">Resume (PDF/TXT)</label>
        <input className="mb-5 block w-full" type="file" onChange={(e) => setResume(e.target.files?.[0])} />

        <label className="mb-2 block text-sm font-medium text-slate-700">Job Description (PDF/TXT)</label>
        <input className="mb-5 block w-full" type="file" onChange={(e) => setJd(e.target.files?.[0])} />

        <label className="mb-2 block text-sm font-medium text-slate-700">Career Goal</label>
        <input
          className="mb-5 w-full rounded-lg border border-slate-300 px-3 py-2"
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
        />

        <div className="flex gap-3">
          <button
            onClick={handleProcess}
            disabled={loading}
            className="rounded-lg bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Processing..." : "Analyze"}
          </button>
          <button
            onClick={handleDemo}
            disabled={loading}
            className="rounded-lg bg-emerald-600 px-4 py-2 font-semibold text-white hover:bg-emerald-700 disabled:opacity-50"
          >
            ✨ Try Demo (Auto-fill + Analyze)
          </button>
        </div>

        {status && <p className="mt-4 text-sm text-slate-700">{status}</p>}
      </div>
    </div>
  );
}
