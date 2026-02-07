import axios from "axios";
import { useState } from "react";

function App() {
  const [resume, setResume] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!resume || !jobDesc) {
      alert("Please upload resume and paste job description");
      return;
    }

    setLoading(true);

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
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return "#28a745"; // Green
    if (score >= 50) return "#ffc107"; // Yellow
    return "#dc3545"; // Red
  };

  const getMatchColor = (classification) => {
    if (classification === "Strong Match") return "#28a745";
    if (classification === "Moderate Match") return "#ffc107";
    if (classification === "Developing Match") return "#fd7e14";
    return "#dc3545";
  };

  return (
    <div style={{ padding: "30px", fontFamily: "Arial", maxWidth: "1000px", margin: "0 auto" }}>
      <h1>AI Resume Analyzer 🎯</h1>
      <p style={{ color: "#666", marginBottom: "20px" }}>
        Upload your resume and job description to get AI-powered matching analysis
      </p>

      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: "20px",
        marginBottom: "20px"
      }}>
        <div>
          <label style={{ fontWeight: "bold", display: "block", marginBottom: "8px" }}>
            Upload Resume (PDF)
          </label>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setResume(e.target.files[0])}
            style={{
              padding: "10px",
              borderRadius: "5px",
              border: "1px solid #ddd",
              width: "100%",
              boxSizing: "border-box"
            }}
          />
        </div>

        <div>
          <label style={{ fontWeight: "bold", display: "block", marginBottom: "8px" }}>
            Job Description
          </label>
          <textarea
            rows="4"
            placeholder="Paste job description here..."
            onChange={(e) => setJobDesc(e.target.value)}
            style={{
              padding: "10px",
              borderRadius: "5px",
              border: "1px solid #ddd",
              width: "100%",
              boxSizing: "border-box",
              fontFamily: "monospace",
              fontSize: "12px"
            }}
          />
        </div>
      </div>

      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{
          padding: "12px 30px",
          fontSize: "16px",
          fontWeight: "bold",
          backgroundColor: "#007bff",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: loading ? "not-allowed" : "pointer",
          opacity: loading ? 0.7 : 1,
          marginBottom: "30px"
        }}
      >
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>

      {result && (
        <div style={{
          backgroundColor: "#f8f9fa",
          padding: "25px",
          borderRadius: "10px",
          border: "1px solid #dee2e6"
        }}>
          
          {/* Match Classification Banner */}
          <div style={{
            padding: "20px",
            backgroundColor: getMatchColor(result.match_classification),
            color: "white",
            borderRadius: "8px",
            marginBottom: "15px",
            textAlign: "center",
            fontSize: "18px",
            fontWeight: "bold",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            gap: "20px"
          }}>
            <div>✓ {result.match_classification}</div>
            {result.detected_role && (
              <div style={{
                backgroundColor: "rgba(255,255,255,0.2)",
                padding: "6px 14px",
                borderRadius: "20px",
                fontSize: "13px",
                fontWeight: "500",
                textTransform: "capitalize"
              }}>
                📍 {result.detected_role}
              </div>
            )}
          </div>

          {/* Critical Missing Skills Alert */}
          {result.critical_missing_skills && result.critical_missing_skills.length > 0 && (
            <div style={{
              padding: "12px 15px",
              backgroundColor: "#fff3cd",
              border: "1px solid #ffc107",
              borderRadius: "6px",
              marginBottom: "20px",
              fontSize: "13px",
              color: "#856404"
            }}>
              ⚠️ <strong>Core Skills Gap:</strong> {result.critical_missing_skills.map(s => s.charAt(0).toUpperCase() + s.slice(1)).join(", ")} are crucial for this {result.detected_role} role.
            </div>
          )}

          {/* Transparent 7-Factor Scoring Breakdown */}
          <div style={{ marginBottom: "30px" }}>
            <h3 style={{ marginTop: 0, marginBottom: "15px" }}>📊 7-Factor Analysis</h3>
            <p style={{ fontSize: "12px", color: "#666", marginTop: 0, marginBottom: "15px" }}>
              Comprehensive evaluation based on: Required Skills Coverage, Skill Relevance, Skill Depth, Experience Level, Domain Context, ATS Optimization, and Focus Score.
            </p>
            
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr) repeat(2, 1fr)", gap: "12px", marginBottom: "20px" }}>
              {/* Factor 1: Required Skill Coverage (40%) */}
              <div style={{
                padding: "12px",
                backgroundColor: "white",
                borderRadius: "6px",
                border: "2px solid #007bff"
              }}>
                <div style={{ fontSize: "28px", fontWeight: "bold", color: "#007bff", marginBottom: "4px" }}>
                  {result.score_breakdown_7_factor.required_skill_coverage.toFixed(0)}
                </div>
                <div style={{ fontSize: "11px", color: "#666", fontWeight: "500" }}>Required Skills</div>
                <div style={{ fontSize: "9px", color: "#999" }}>(40% weight)</div>
              </div>

              {/* Factor 2: Skill Relevance (25%) */}
              <div style={{
                padding: "12px",
                backgroundColor: "white",
                borderRadius: "6px",
                border: "2px solid #28a745"
              }}>
                <div style={{ fontSize: "28px", fontWeight: "bold", color: "#28a745", marginBottom: "4px" }}>
                  {result.score_breakdown_7_factor.skill_relevance.toFixed(0)}
                </div>
                <div style={{ fontSize: "11px", color: "#666", fontWeight: "500" }}>Relevance</div>
                <div style={{ fontSize: "9px", color: "#999" }}>(25% weight)</div>
              </div>

              {/* Factor 3: Skill Depth (15%) */}
              <div style={{
                padding: "12px",
                backgroundColor: "white",
                borderRadius: "6px",
                border: "2px solid #ffc107"
              }}>
                <div style={{ fontSize: "28px", fontWeight: "bold", color: "#ffc107", marginBottom: "4px" }}>
                  {result.score_breakdown_7_factor.skill_depth_signals.toFixed(0)}
                </div>
                <div style={{ fontSize: "11px", color: "#666", fontWeight: "500" }}>Skill Depth</div>
                <div style={{ fontSize: "9px", color: "#999" }}>(15% weight)</div>
              </div>

              {/* Factor 4: Experience Alignment (10%) */}
              <div style={{
                padding: "12px",
                backgroundColor: "white",
                borderRadius: "6px",
                border: "2px solid #17a2b8"
              }}>
                <div style={{ fontSize: "28px", fontWeight: "bold", color: "#17a2b8", marginBottom: "4px" }}>
                  {result.score_breakdown_7_factor.experience_level_alignment.toFixed(0)}
                </div>
                <div style={{ fontSize: "11px", color: "#666", fontWeight: "500" }}>Experience</div>
                <div style={{ fontSize: "9px", color: "#999" }}>(10% weight)</div>
              </div>

              {/* Factor 5: Domain Context (5%) */}
              <div style={{
                padding: "12px",
                backgroundColor: "white",
                borderRadius: "6px",
                border: "2px solid #6f42c1"
              }}>
                <div style={{ fontSize: "28px", fontWeight: "bold", color: "#6f42c1", marginBottom: "4px" }}>
                  {result.score_breakdown_7_factor.domain_context.toFixed(0)}
                </div>
                <div style={{ fontSize: "11px", color: "#666", fontWeight: "500" }}>Domain Context</div>
                <div style={{ fontSize: "9px", color: "#999" }}>(5% weight)</div>
              </div>

              {/* Factor 6: ATS Optimization (3%) */}
              <div style={{
                padding: "12px",
                backgroundColor: "white",
                borderRadius: "6px",
                border: "2px solid #e83e8c"
              }}>
                <div style={{ fontSize: "28px", fontWeight: "bold", color: "#e83e8c", marginBottom: "4px" }}>
                  {result.score_breakdown_7_factor.ats_optimization.toFixed(0)}
                </div>
                <div style={{ fontSize: "11px", color: "#666", fontWeight: "500" }}>ATS Clarity</div>
                <div style={{ fontSize: "9px", color: "#999" }}>(3% weight)</div>
              </div>

              {/* Factor 7: Signal vs Noise (2%) */}
              <div style={{
                padding: "12px",
                backgroundColor: "white",
                borderRadius: "6px",
                border: "2px solid #20c997"
              }}>
                <div style={{ fontSize: "28px", fontWeight: "bold", color: "#20c997", marginBottom: "4px" }}>
                  {result.score_breakdown_7_factor.signal_vs_noise_ratio.toFixed(0)}
                </div>
                <div style={{ fontSize: "11px", color: "#666", fontWeight: "500" }}>Focus</div>
                <div style={{ fontSize: "9px", color: "#999" }}>(2% weight)</div>
              </div>

              {/* Final Weighted Score - Prominently Displayed */}
              <div style={{
                padding: "15px",
                backgroundColor: getScoreColor(result.scoring_breakdown.final_score),
                borderRadius: "6px",
                border: `3px solid ${getScoreColor(result.scoring_breakdown.final_score)}`,
                color: "white",
                gridColumn: "span 2",
                textAlign: "center"
              }}>
                <div style={{ fontSize: "11px", marginBottom: "6px", opacity: 0.9, fontWeight: "bold" }}>
                  FINAL SCORE (Weighted Average)
                </div>
                <div style={{ fontSize: "40px", fontWeight: "bold" }}>
                  {result.scoring_breakdown.final_score.toFixed(1)}%
                </div>
              </div>
            </div>
          </div>

          {/* Skills Analysis */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px", marginBottom: "25px" }}>
            {/* Matched Skills */}
            <div style={{
              padding: "15px",
              backgroundColor: "white",
              borderRadius: "8px",
              border: "1px solid #dee2e6"
            }}>
              <h4 style={{ margin: "0 0 10px 0", color: "#28a745" }}>
                ✓ Matched Skills ({result.matched_skills.length})
              </h4>
              <p style={{ margin: 0, fontSize: "14px", color: "#333" }}>
                {result.matched_skills.length > 0
                  ? result.matched_skills.join(", ")
                  : "None"}
              </p>
            </div>

            {/* Missing Skills */}
            <div style={{
              padding: "15px",
              backgroundColor: "white",
              borderRadius: "8px",
              border: "1px solid #dee2e6"
            }}>
              <h4 style={{ margin: "0 0 10px 0", color: "#dc3545" }}>
                ✗ Missing Skills ({result.missing_skills.length})
              </h4>
              <p style={{ margin: 0, fontSize: "14px", color: "#333" }}>
                {result.missing_skills.length > 0
                  ? result.missing_skills.join(", ")
                  : "You have all required skills!"}
              </p>
            </div>
          </div>

          {/* Bonus Skills */}
          {result.bonus_skills.length > 0 && (
            <div style={{
              padding: "15px",
              backgroundColor: "white",
              borderRadius: "8px",
              border: "1px solid #dee2e6",
              marginBottom: "25px"
            }}>
              <h4 style={{ margin: "0 0 10px 0", color: "#ffc107" }}>
                ⭐ Extra Skills (Bonus Points)
              </h4>
              <p style={{ margin: 0, fontSize: "14px", color: "#333" }}>
                {result.bonus_skills.join(", ")}
              </p>
            </div>
          )}

          {/* Suggestions */}
          <div style={{
            padding: "20px",
            backgroundColor: "white",
            borderRadius: "8px",
            border: "1px solid #dee2e6"
          }}>
            <h3 style={{ margin: "0 0 20px 0" }}>💡 Suggestions & Recommendations</h3>

            {result.suggestions && (
              <>
                {/* Overall Verdict */}
                <div style={{
                  padding: "15px",
                  backgroundColor: "#f0f7ff",
                  border: "2px solid #0056b3",
                  borderRadius: "6px",
                  marginBottom: "20px"
                }}>
                  <h4 style={{ margin: "0 0 8px 0", color: "#0056b3" }}>📋 Overall Assessment</h4>
                  <p style={{ margin: "0 0 12px 0", color: "#333", lineHeight: "1.6" }}>
                    {result.suggestions.overall_verdict}
                  </p>
                  
                  {/* Simplified Metrics */}
                  <div style={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: "12px",
                    marginTop: "12px",
                    paddingTop: "12px",
                    borderTop: "1px solid #b0d4ff"
                  }}>
                    <div>
                      <div style={{ fontSize: "12px", color: "#555", fontWeight: "600" }}>Skill Match</div>
                      <div style={{ fontSize: "20px", fontWeight: "bold", color: "#0056b3", marginTop: "4px" }}>
                        {result.skill_match_percentage}%
                      </div>
                    </div>
                    {result.bonus_percentage > 0 && (
                      <div>
                        <div style={{ fontSize: "12px", color: "#555", fontWeight: "600" }}>Bonus Skills</div>
                        <div style={{ fontSize: "20px", fontWeight: "bold", color: "#ffc107", marginTop: "4px" }}>
                          +{result.bonus_percentage}%
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                {/* Strategic Recommendations */}
                {result.suggestions.strategic_recommendations && result.suggestions.strategic_recommendations.length > 0 && (
                  <div style={{
                    padding: "15px",
                    backgroundColor: "#f8f9fa",
                    border: "2px solid #6c757d",
                    borderRadius: "6px",
                    marginBottom: "20px"
                  }}>
                    <h4 style={{ margin: "0 0 12px 0", color: "#6c757d" }}>🎯 Strategic Roadmap</h4>
                    <ul style={{ margin: 0, paddingLeft: "20px" }}>
                      {result.suggestions.strategic_recommendations.map((rec, idx) => (
                        <li key={idx} style={{
                          marginBottom: "8px",
                          color: "#333",
                          lineHeight: "1.6",
                          fontSize: "13px"
                        }}>
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Learning Projects (GROUP-BASED, not per-skill) */}
                {result.suggestions.learning_projects && result.suggestions.learning_projects.length > 0 && (
                  <div style={{ marginBottom: "20px" }}>
                    <h4 style={{ margin: "0 0 15px 0", color: "#28a745" }}>
                      📚 Recommended Learning Projects
                    </h4>
                    <div style={{ display: "grid", gap: "15px" }}>
                      {result.suggestions.learning_projects.map((project, idx) => (
                        <div key={idx} style={{
                          padding: "15px",
                          backgroundColor: "#f0f8f0",
                          border: "2px solid #28a745",
                          borderRadius: "6px"
                        }}>
                          <div style={{
                            fontWeight: "bold",
                            color: "#28a745",
                            fontSize: "15px",
                            marginBottom: "8px"
                          }}>
                            {idx + 1}. {project.title}
                          </div>
                          <p style={{
                            color: "#333",
                            fontSize: "13px",
                            lineHeight: "1.6",
                            margin: "0 0 10px 0"
                          }}>
                            {project.description}
                          </p>
                          <div style={{
                            display: "flex",
                            gap: "8px",
                            flexWrap: "wrap",
                            marginBottom: "10px"
                          }}>
                            {project.skills_covered.map((skill, sidx) => (
                              <span key={sidx} style={{
                                padding: "4px 8px",
                                backgroundColor: "#d4edda",
                                color: "#155724",
                                borderRadius: "4px",
                                fontSize: "12px",
                                fontWeight: "600"
                              }}>
                                {skill}
                              </span>
                            ))}
                          </div>
                          <div style={{
                            fontSize: "12px",
                            color: "#555",
                            fontStyle: "italic"
                          }}>
                            ⏱ Effort: {project.effort}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Resume Positioning Tips */}
                {result.suggestions.resume_positioning && (
                  <div style={{
                    padding: "15px",
                    backgroundColor: "#fff3cd",
                    border: "2px solid #ffc107",
                    borderRadius: "6px",
                    marginBottom: "20px"
                  }}>
                    <h4 style={{ margin: "0 0 12px 0", color: "#856404" }}>✏️ Resume Positioning Guide</h4>
                    <ul style={{ margin: "0", paddingLeft: "20px" }}>
                      <li style={{ marginBottom: "8px", color: "#333", fontSize: "13px", lineHeight: "1.6" }}>
                        <strong>Headline:</strong> {result.suggestions.resume_positioning.headline}
                      </li>
                      <li style={{ marginBottom: "8px", color: "#333", fontSize: "13px", lineHeight: "1.6" }}>
                        <strong>Projects Section:</strong> {result.suggestions.resume_positioning.project_section_tip}
                      </li>
                      <li style={{ marginBottom: "8px", color: "#333", fontSize: "13px", lineHeight: "1.6" }}>
                        <strong>Skills Listing:</strong> {result.suggestions.resume_positioning.skill_listing_tip}
                      </li>
                      {result.suggestions.resume_positioning.bonus_skills_mention && (
                        <li style={{ color: "#333", fontSize: "13px", lineHeight: "1.6" }}>
                          <strong>Bonus Skills:</strong> {result.suggestions.resume_positioning.bonus_skills_mention}
                        </li>
                      )}
                    </ul>
                  </div>
                )}

                {/* Encouragement */}
                {result.suggestions.encouragement && (
                  <div style={{
                    padding: "15px",
                    backgroundColor: "#e8f5e9",
                    border: "2px solid #4caf50",
                    borderRadius: "6px",
                    textAlign: "center"
                  }}>
                    <h4 style={{ margin: "0 0 8px 0", color: "#4caf50" }}>💪 Keep Going!</h4>
                    <p style={{ margin: 0, color: "#333", lineHeight: "1.6", fontStyle: "italic" }}>
                      {result.suggestions.encouragement}
                    </p>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;

