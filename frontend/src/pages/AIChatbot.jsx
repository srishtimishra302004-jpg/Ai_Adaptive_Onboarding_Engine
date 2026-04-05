import { useState } from "react";

export default function AIChatbot({ analysis }) {
  const [messages, setMessages] = useState([
    {
      role: "ai",
      text: "Hi 👋 I’m your AI career assistant. Ask me anything about your resume, skills, or improvement plan.",
    },
  ]);
  const [input, setInput] = useState("");

  const generateSmartReply = (question) => {
    const q = question.toLowerCase();

    const ats = analysis?.scores?.ats_score || 0;
    const similarity = analysis?.scores?.similarity_score || 0;
    const confidence = analysis?.scores?.confidence_score || 0;

    const missing = analysis?.skills?.missing || [];
    const matched = analysis?.skills?.matched || [];

    
    if (q.includes("ats")) {
      return `Your ATS score is ${ats}%. To improve it, focus on adding more relevant keywords, proper formatting, and matching job descriptions.`;
    }

    if (q.includes("skill")) {
      return missing.length > 0
        ? `You are missing these key skills: ${missing.join(", ")}. Start learning them step-by-step.`
        : "You already have strong skill coverage. Focus on advanced projects.";
    }

    if (q.includes("improve") || q.includes("how")) {
      return `To improve your profile:\n1. Learn missing skills: ${missing.join(", ") || "None"}\n2. Build real projects\n3. Optimize your resume\n4. Increase ATS score`;
    }

    if (q.includes("score")) {
      return `Your current scores:\nATS: ${ats}%\nSimilarity: ${similarity}%\nConfidence: ${confidence}%`;
    }

    if (q.includes("project")) {
      return `Build projects using your strengths (${matched.join(", ")}) and include missing skills (${missing.join(", ")}) to stand out.`;
    }

    
    return `Based on your profile, you should focus on improving ${missing.join(", ") || "advanced skills"}, building strong projects, and optimizing your resume for ATS systems.`;
  };

  const handleSend = () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    const reply = generateSmartReply(input);

    setMessages((prev) => [
      ...prev,
      userMsg,
      { role: "ai", text: reply },
    ]);

    setInput("");
  };

  return (
    <div className="mt-6 rounded-xl bg-white dark:bg-slate-900 p-6 shadow border border-slate-200 dark:border-slate-700">

      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
          AI Assistant
        </h2>

        <span className="text-xs px-2 py-1 rounded bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300">
          Smart AI
        </span>
      </div>

      
      <div className="h-52 overflow-y-auto mb-4 p-3 bg-slate-50 dark:bg-slate-800 rounded space-y-3 text-sm">

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`px-3 py-2 rounded-lg max-w-[75%] ${
                msg.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-slate-200"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      {/* Input */}
      <div className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything about your profile..."
          className="flex-1 p-2 rounded border dark:bg-slate-800 dark:text-white"
        />

        <button
          onClick={handleSend}
          className="px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
          Send
        </button>
      </div>
    </div>
  );
}