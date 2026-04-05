import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import AIChatbot from "../pages/AIChatbot";

const COLORS = ["#2563eb", "#14b8a6", "#f97316", "#e11d48"];

export default function DashboardPage() {
 const [analysis, setAnalysis] = useState(null);
 const [plan, setPlan] = useState([]);

useEffect(() => {
  const loadData = () => {
    const raw = sessionStorage.getItem("analysis");
    setAnalysis(raw ? JSON.parse(raw) : null);
  };

  loadData(); 

  const interval = setInterval(loadData, 3000); 

  return () => clearInterval(interval); 
}, []);

const generatePlan = () => {
  const missing = analysis?.skills?.missing || [];
  const strengths = analysis?.skills?.matched || [];
  const level = analysis?.experience_level || "Beginner";

  if (missing.length === 0) {
    setPlan([
      {
        step: 1,
        title: " Strong Profile",
        text: "You already match most required skills. Focus on advanced projects and real-world experience.",
      },
    ]);
    return;
  }

  const newPlan = missing.map((skill, index) => ({
    step: index + 1,
    title: `📌 Improve ${skill}`,
    text: `Learn ${skill} through hands-on practice and build at least one project.`,
    extra: `💡 Tip: Combine ${skill} with ${strengths[0] || "your existing skills"} to stand out.`,
  }));

  // Add final summary step
  newPlan.push({
    step: newPlan.length + 1,
    title: "🎯 Final Goal",
    text: `Based on your ${level} level, aim to complete these skills within 4–6 weeks and update your resume.`,
  });

  setPlan(newPlan);
};



  if (!analysis) {
    return (
      <div className="mx-auto max-w-4xl px-6 py-10">
        <p className="mb-4 text-slate-700">No analysis found yet.</p>
        <Link to="/" className="text-blue-600 underline">
          Go to upload page
        </Link>
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
  const totalMatchSignals = matchedSkills.length + missingSkills.length + partialSkills.length;
  const chartData = categoryData.filter((item) => item.value > 0);
  const strengthEntries = Object.entries(skillStrength).sort((a, b) => b[1] - a[1]);

  return (
    <div className="mx-auto max-w-6xl px-6 py-8">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Candidate Dashboard</h1>
        <Link to="/" className="text-blue-600 underline">
          New Analysis
        </Link>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        <Card title="Resume Score" value={`${scores.resume_score ?? 0}/100`} />
        <Card title="Similarity Score" value={`${scores.similarity_score ?? 0}%`} />
        <Card title="ATS Score" value={`${scores.ats_score ?? 0}%`} />
        <Card title="Confidence Score" value={`${scores.confidence_score ?? 0}%`} />
        <Card title="Missing Skills" value={`${missingSkills.length}`} />
      </div>

      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        <Section title="Matched Skills">{matchedSkills.join(", ") || "None"}</Section>
        <Section title="Missing Skills">{missingSkills.join(", ") || "None"}</Section>
      </div>

      <div className="mt-6 rounded-xl bg-white p-6 shadow">
        <h2 className="mb-3 text-xl font-semibold text-slate-900">Skill Match Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="h-64">
            {totalMatchSignals === 0 ? (
              <div className="flex h-full items-center justify-center text-sm text-slate-500">No skill match data</div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={chartData}
                    dataKey="value"
                    nameKey="name"
                    outerRadius={90}
                    label={({ name, value }) =>
                      `${name}: ${Math.round((value / Math.max(1, totalMatchSignals)) * 100)}%`
                    }
                  >
                    {chartData.map((_, i) => (
                      <Cell key={`cell-${i}`} fill={COLORS[i % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [`${value}`, "Count"]} />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>
          <div>
            {categoryData.map((cat) => (
              <div key={cat.name} className="mb-4">
                <div className="mb-1 flex justify-between text-sm font-semibold text-black dark:text-white">
                  <span>{cat.name}</span>
                  <span>{cat.value}</span>
                </div>
                <div className="h-2 rounded bg-slate-300 dark:bg-slate-600">
                  <div
                    className="h-2 rounded bg-blue-600"
                    style={{
                      width: `${Math.min(
                        100,
                        Math.round((cat.value / Math.max(1, totalMatchSignals)) * 100)
                      )}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="mt-6 rounded-xl bg-white p-6 shadow">
        <h2 className="mb-3 text-xl font-semibold text-slate-900">Experience & Gap Analysis</h2>
        <p className="text-slate-700">
          <span className="font-semibold">Experience Level:</span> {analysis.experience_level || "N/A"}
        </p>
        <p className="mt-2 text-slate-600">{analysis.skill_gap_analysis || "No analysis available."}</p>
      </div>

      <div className="mt-6 rounded-xl bg-white p-6 shadow">
        <h2 className="mb-3 text-xl font-semibold text-slate-900">Skill Strength Meter</h2>
        {strengthEntries.length === 0 ? (
          <p className="text-slate-600">No strength signals available.</p>
        ) : (
          strengthEntries.map(([skill, value]) => (
            <div key={skill} className="mb-4">
              <div className="mb-1 flex justify-between text-sm">
                <span>{skill}</span>
                <span>{value}%</span>
              </div>
              <div className="h-2 rounded bg-slate-200">
                <div className="h-2 rounded bg-emerald-600" style={{ width: `${value}%` }} />
              </div>
            </div>
          ))
        )}
      </div>

      <div className="mt-6 rounded-xl bg-white p-6 shadow">
        <h2 className="mb-3 text-xl font-semibold text-slate-900">Learning Roadmap</h2>
        {roadmap.map((step, idx) => (
          <div key={`${step.track}-${idx}`} className="mb-4 rounded-lg border border-slate-200 p-4">
            <p className="font-semibold text-slate-900">
              {idx + 1}. {step.track}
            </p>
            <p className="mt-1 text-sm text-slate-600">{step.why}</p>
            <p className="mt-2 text-sm text-slate-700">
              <span className="font-medium">What to learn:</span> {(step.what_to_learn || []).join(", ") || "N/A"}
            </p>
            <ul className="mt-2 list-disc pl-5 text-sm text-blue-700">
              {(step.resources || []).map((res) => (
                <li key={res}>
                  <a href={res} target="_blank" rel="noreferrer">
                    {res}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <div className="mt-6 rounded-xl bg-white p-6 shadow">
        <h2 className="mb-3 text-xl font-semibold text-slate-900">Partial Semantic Matches</h2>
        {partialSkills.length === 0 ? (
          <p className="text-slate-600">No partial matches detected.</p>
        ) : (
          <ul className="list-disc pl-5 text-slate-700">
            {partialSkills.map((item) => (
              <li key={`${item.required_skill}-${item.related_user_skill}`}>
                {item.required_skill} ~ {item.related_user_skill} ({item.similarity}%)
              </li>
            ))}
          </ul>
        )}
      </div>

     <div className="mt-6 rounded-xl bg-white dark:bg-slate-900 p-6 shadow border border-slate-200 dark:border-slate-700">
  
  <h2 className="mb-4 text-lg font-semibold text-slate-900 dark:text-white flex items-center gap-2">
     Reasoning Trace
  </h2>

  {analysis.reasoning_trace ? (
    <div className="space-y-3 text-sm">
      {analysis.reasoning_trace.split("\n").map((line, index) => (
        <div
          key={index}
          className="flex items-start gap-3 p-3 rounded-lg bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-300"
        >
          <span className="text-blue-500">•</span>
          <span>{line}</span>
        </div>
      ))}
    </div>
  ) : (
    <p className="text-slate-500 dark:text-slate-400">Not available.</p>
  )}

  {/* AI Planner */}
<div className="mt-6 rounded-xl bg-white dark:bg-slate-900 p-6 shadow border border-slate-200 dark:border-slate-700">

  <div className="flex items-center justify-between mb-4">
    <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
      AI Planner
    </h2>

    <button
      onClick={generatePlan}
      className="px-3 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
    >
      Generate Plan
    </button>
  </div>

  {plan.length === 0 ? (
    <p className="text-sm text-slate-500 dark:text-slate-400">
      Click "Generate Plan" to get your personalized roadmap.
    </p>
  ) : (
    <div className="space-y-4">
      {plan.map((item) => (
        <div
          key={item.step}
          className="p-4 rounded-xl bg-gradient-to-r from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-700 border border-slate-200 dark:border-slate-700 shadow-sm hover:shadow-md transition-all"
        >
          <p className="font-semibold text-slate-900 dark:text-white">
            {item.step}. {item.title}
          </p>

          <p className="text-sm mt-1 text-slate-700 dark:text-slate-300">
            {item.text}
          </p>

          {item.extra && (
            <p className="text-xs mt-2 text-blue-600 dark:text-blue-400">
              {item.extra}
            </p>
          )}
        </div>
      ))}
    </div>
  )}

</div>

<AIChatbot analysis={analysis} />

</div>
    </div>
  );
}


function Card({ title, value }) {
  return (
    <div className="rounded-xl bg-white p-5 shadow">
      <p className="text-sm text-slate-600">{title}</p>
      <p className="mt-2 text-3xl font-bold text-slate-900">{value}</p>
    </div>
  );
}

function Section({ title, children }) {
  return (
    <div className="rounded-xl bg-white p-6 shadow">
      <h2 className="mb-2 text-xl font-semibold text-slate-900">{title}</h2>
      <p className="text-slate-700">{children}</p>
    </div>
  );
}