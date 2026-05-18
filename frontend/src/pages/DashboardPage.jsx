import { useMemo } from "react";
import { Link } from "react-router-dom";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

const COLORS = ["#2563eb", "#14b8a6", "#f97316", "#e11d48"];

export default function DashboardPage() {
  const analysis = useMemo(() => {
    const raw = sessionStorage.getItem("analysis");
    return raw ? JSON.parse(raw) : null;
  }, []);

  if (!analysis) {
    return (
      <div className="flex min-h-[80vh] items-center justify-center px-4">
        <div className="text-center">
          <p className="text-xl text-slate-600 dark:text-slate-400 mb-4">No analysis found yet.</p>
          <Link to="/" className="rounded-xl bg-blue-600 text-white px-6 py-3 font-semibold hover:bg-blue-700">
            Go to Upload Page
          </Link>
        </div>
      </div>
    );
  }

  const scores = analysis.scores || {};
  const skills = analysis.skills || {};
  const matchedSkills = skills.matched || [];
  const missingSkills = skills.missing || [];
  const partialSkills = skills.partial || [];
  const skillStrength = analysis.skill_strength || {};
  const roadmap = analysis.learning_roadmap || [];

  const categoryData = [
    { name: "Matched", value: matchedSkills.length },
    { name: "Missing", value: missingSkills.length },
    { name: "Partial", value: partialSkills.length },
  ];
  const total = matchedSkills.length + missingSkills.length + partialSkills.length;
  const chartData = categoryData.filter((d) => d.value > 0);
  const strengthEntries = Object.entries(skillStrength).sort((a, b) => b[1] - a[1]);

  const scoreCards = [
    { label: "Resume Score", value: `${scores.resume_score ?? 0}/100`, color: "text-blue-600 dark:text-blue-400" },
    { label: "Similarity", value: `${scores.similarity_score ?? 0}%`, color: "text-teal-600 dark:text-teal-400" },
    { label: "ATS Score", value: `${scores.ats_score ?? 0}%`, color: "text-orange-500 dark:text-orange-400" },
    { label: "Confidence", value: `${scores.confidence_score ?? 0}%`, color: "text-purple-600 dark:text-purple-400" },
    { label: "Missing Skills", value: missingSkills.length, color: "text-red-500 dark:text-red-400" },
  ];

  return (
    <div className="w-full px-4 py-8 max-w-5xl mx-auto">

      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 mb-8">
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Candidate Dashboard</h1>
        <Link to="/" className="rounded-xl bg-blue-600 text-white px-4 py-2 text-sm font-semibold hover:bg-blue-700 transition-colors">
          + New Analysis
        </Link>
      </div>

      {/* Score Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 mb-6">
        {scoreCards.map(({ label, value, color }) => (
          <div key={label} className="rounded-2xl bg-white dark:bg-slate-800 p-4 shadow border border-slate-200 dark:border-slate-700 text-center">
            <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">{label}</p>
            <p className={`text-2xl font-bold ${color}`}>{value}</p>
          </div>
        ))}
      </div>

      {/* Skills */}
      <div className="grid sm:grid-cols-2 gap-4 mb-6">
        <Panel title="✅ Matched Skills">
          <p className="text-slate-700 dark:text-slate-300 leading-relaxed">
            {matchedSkills.join(", ") || "None"}
          </p>
        </Panel>
        <Panel title="❌ Missing Skills">
          <p className="text-slate-700 dark:text-slate-300 leading-relaxed">
            {missingSkills.join(", ") || "None"}
          </p>
        </Panel>
      </div>

      {/* Chart */}
      <Panel title="📊 Skill Match Overview" className="mb-6">
        <div className="grid sm:grid-cols-2 gap-6 items-center">
          <div className="h-64 w-full">
            {total === 0 ? (
              <div className="flex h-full items-center justify-center text-slate-400">No data</div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={chartData} dataKey="value" nameKey="name" outerRadius="80%"
                    label={({ name, value }) => `${name}: ${Math.round((value / total) * 100)}%`}>
                    {chartData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                  </Pie>
                  <Tooltip formatter={(v) => [v, "Count"]} />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>
          <div>
            {categoryData.map((cat) => (
              <div key={cat.name} className="mb-4">
                <div className="flex justify-between text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                  <span>{cat.name}</span><span>{cat.value}</span>
                </div>
                <div className="h-3 rounded-full bg-slate-200 dark:bg-slate-600">
                  <div className="h-3 rounded-full bg-blue-600"
                    style={{ width: `${Math.min(100, Math.round((cat.value / Math.max(1, total)) * 100))}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </Panel>

      {/* Experience */}
      <Panel title="🎓 Experience & Gap Analysis" className="mb-6">
        <p className="text-slate-700 dark:text-slate-300 mb-2">
          <span className="font-semibold">Level:</span> {analysis.experience_level || "N/A"}
        </p>
        <p className="text-slate-600 dark:text-slate-400">{analysis.skill_gap_analysis}</p>
      </Panel>

      {/* Strength */}
      <Panel title="💪 Skill Strength Meter" className="mb-6">
        {strengthEntries.length === 0 ? <p className="text-slate-500">No data.</p>
          : strengthEntries.map(([skill, value]) => (
            <div key={skill} className="mb-4">
              <div className="flex justify-between text-sm text-slate-700 dark:text-slate-300 mb-1">
                <span>{skill}</span><span className="font-semibold">{value}%</span>
              </div>
              <div className="h-3 rounded-full bg-slate-200 dark:bg-slate-600">
                <div className="h-3 rounded-full bg-emerald-500" style={{ width: `${value}%` }} />
              </div>
            </div>
          ))}
      </Panel>

      {/* Roadmap */}
      <Panel title="🗺️ Learning Roadmap" className="mb-6">
        {roadmap.map((step, idx) => (
          <div key={idx} className="mb-4 rounded-xl border border-slate-200 dark:border-slate-600 p-4 bg-slate-50 dark:bg-slate-700">
            <p className="font-bold text-slate-900 dark:text-white mb-1">{idx + 1}. {step.track}</p>
            <p className="text-sm text-slate-500 dark:text-slate-400 mb-2">{step.why}</p>
            <p className="text-sm text-slate-700 dark:text-slate-300 mb-2">
              <span className="font-semibold">Learn:</span> {(step.what_to_learn || []).join(", ") || "N/A"}
            </p>
            <ul className="list-disc pl-5 text-sm text-blue-600 dark:text-blue-400 space-y-1">
              {(step.resources || []).map((res) => (
                <li key={res}><a href={res} target="_blank" rel="noreferrer" className="hover:underline break-all">{res}</a></li>
              ))}
            </ul>
          </div>
        ))}
      </Panel>

      {/* Partial Matches */}
      {partialSkills.length > 0 && (
        <Panel title="🔗 Partial Semantic Matches" className="mb-6">
          <ul className="list-disc pl-5 text-slate-700 dark:text-slate-300 space-y-1">
            {partialSkills.map((item) => (
              <li key={`${item.required_skill}-${item.related_user_skill}`}>
                {item.required_skill} ~ {item.related_user_skill} ({item.similarity}%)
              </li>
            ))}
          </ul>
        </Panel>
      )}

      {/* Reasoning */}
      <Panel title="🧠 Reasoning Trace" className="mb-8">
        <p className="whitespace-pre-line text-slate-700 dark:text-slate-300 leading-relaxed">
          {analysis.reasoning_trace || "Not available."}
        </p>
      </Panel>
    </div>
  );
}

function Panel({ title, children, className = "" }) {
  return (
    <div className={`rounded-2xl bg-white dark:bg-slate-800 p-5 shadow border border-slate-200 dark:border-slate-700 ${className}`}>
      <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-3">{title}</h2>
      {children}
    </div>
  );
}
