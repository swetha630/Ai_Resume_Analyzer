from flask import Flask, request, jsonify
from flask_cors import CORS

from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills
from similarity import calculate_similarity
from gap_analyzer import find_skill_gap, generate_suggestions

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "AI Resume Analyzer Backend is running"


@app.route("/analyze", methods=["POST"])
def analyze_resume():
    """
    Expects:
    - resume file (PDF)
    - job_description (text)
    """

    if "resume" not in request.files:
        return jsonify({"error": "Resume file is required"}), 400

    resume_file = request.files["resume"]
    job_description = request.form.get("job_description", "")

    if job_description.strip() == "":
        return jsonify({"error": "Job description is required"}), 400

    # Save resume temporarily
    resume_path = "uploaded_resume.pdf"
    resume_file.save(resume_path)

    # Resume processing
    resume_text = extract_text_from_pdf(resume_path)
    resume_skills = extract_skills(resume_text)

    # Job description processing
    jd_skills = extract_skills(job_description)

    # Skill-based similarity
    resume_skills_text = " ".join(resume_skills)
    jd_skills_text = " ".join(jd_skills)

    match_score = calculate_similarity(resume_skills_text, jd_skills_text)

    # Skill gap & suggestions
    missing_skills = find_skill_gap(resume_skills, jd_skills)
    suggestions = generate_suggestions(missing_skills, match_score)

    # Response
    response = {
        "resume_skills": resume_skills,
        "job_skills": jd_skills,
        "missing_skills": missing_skills,
        "match_score": match_score,
        "suggestions": suggestions
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




