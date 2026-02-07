import axios from "axios";
import { useState } from "react";

function App() {
  const [resume, setResume] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    if (!resume || !jobDesc) {
      alert("Please upload resume and paste job description");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jobDesc);

    try {
      const response = await axios.post(
      "http://127.0.0.1:5000/analyze",
      formData
      );
      setResult(response.data);
    } catch (error) {
      alert("Error connecting to backend");
      console.error(error);
    }
  };

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h2>AI Resume Analyzer</h2>

      <input
        type="file"
        onChange={(e) => setResume(e.target.files[0])}
      />

      <br /><br />

      <textarea
        rows="6"
        cols="70"
        placeholder="Paste Job Description here"
        onChange={(e) => setJobDesc(e.target.value)}
      />

      <br /><br />

      <button onClick={handleSubmit}>Analyze</button>

      {result && (
        <div style={{ marginTop: "30px" }}>
          <h3>Match Score: {result.match_score}%</h3>

          <p><b>Resume Skills:</b> {result.resume_skills.join(", ")}</p>
          <p><b>Job Skills:</b> {result.job_skills.join(", ")}</p>
          <p><b>Missing Skills:</b> {result.missing_skills.join(", ")}</p>

          <h4>Suggestions</h4>
          <ul>
            {result.suggestions.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;

