import axios from "axios";

const api = axios.create({
  baseURL: "https://aiadaptiveonboardingengine-production.up.railway.app",
});

export async function uploadResume(file) {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/upload-resume", formData);
}

export async function uploadJd(file) {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/upload-jd", formData);
}

export async function analyze(careerGoal) {
  return api.post("/analyze", { career_goal: careerGoal });
}

export async function analyzeText(resumeText, jdText, careerGoal) {
  return api.post("/analyze-text", {
    resume_text: resumeText,
    jd_text: jdText,
    career_goal: careerGoal,
  });
}
