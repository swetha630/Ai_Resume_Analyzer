from flask import Flask, request, jsonify
from flask_cors import CORS

from resume_parser import extract_text_from_pdf, parse_resume_sections, extract_experience_level, detect_domain_context
from skill_extractor import extract_skills, detect_job_role, get_critical_missing_skills
from similarity import calculate_similarity, calculate_comprehensive_score
from gap_analyzer import find_skill_gap, get_bonus_skills, classify_match, generate_comprehensive_suggestions
from comprehensive_scorer import ComprehensiveScorer

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
    
    Returns: Comprehensive analysis with 7-factor scoring
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

    # === RESUME PARSING ===
    resume_text = extract_text_from_pdf(resume_path)
    resume_sections = parse_resume_sections(resume_text)
    resume_skills = extract_skills(resume_text)
    experience_level = extract_experience_level(resume_sections)

    # === JOB ANALYSIS ===
    jd_skills = extract_skills(job_description)
    detected_role = detect_job_role(jd_skills)

    # === SKILL GAP ANALYSIS ===
    missing_skills = find_skill_gap(resume_skills, jd_skills)
    bonus_skills = get_bonus_skills(resume_skills, jd_skills)
    critical_missing_skills = get_critical_missing_skills(missing_skills, detected_role)
    matched_skills = [skill for skill in resume_skills if skill in jd_skills]

    # === 7-FACTOR SCORING ===
    scorer = ComprehensiveScorer(detected_role, experience_level)
    
    # Factor 1: Required skill coverage (40%)
    factor1 = scorer.score_factor_1_required_skills(matched_skills, jd_skills, missing_skills)
    
    # Factor 2: Skill relevance (25%)
    factor2 = scorer.score_factor_2_skill_relevance(resume_skills, jd_skills)
    
    # Factor 3: Skill depth signals (15%)
    factor3 = scorer.score_factor_3_skill_depth(resume_sections, matched_skills)
    
    # Factor 4: Experience alignment (10%)
    factor4 = scorer.score_factor_4_experience_alignment(len(missing_skills), len(jd_skills))
    
    # Factor 5: Domain context (5%)
    domain_relevance = detect_domain_context(resume_sections, job_description)
    factor5 = scorer.score_factor_5_domain_context(domain_relevance)
    
    # Factor 6: ATS optimization (3%)
    factor6 = scorer.score_factor_6_ats_optimization(resume_text)
    
    # Factor 7: Signal vs noise (2%)
    factor7 = scorer.score_factor_7_signal_noise_ratio(bonus_skills, missing_skills)
    
    # Calculate weighted final score
    factor_scores = {
        "required_skills": factor1,
        "skill_relevance": factor2,
        "skill_depth": factor3,
        "experience_alignment": factor4,
        "domain_context": factor5,
        "ats_optimization": factor6,
        "signal_noise": factor7,
    }
    
    final_7_factor_score = scorer.calculate_weighted_score(factor_scores)
    
    # === TEXT SIMILARITY (for reference) ===
    text_similarity = calculate_similarity(resume_text, job_description)

    # === MATCH CLASSIFICATION (confidence-aware) ===
    match_classification = classify_match(final_7_factor_score, critical_missing_skills)

    # === SUGGESTIONS (role-aware) ===
    suggestions = generate_comprehensive_suggestions(
        missing_skills,
        resume_skills,
        bonus_skills,
        final_7_factor_score,
        len(matched_skills),
        len(jd_skills),
        detected_role=detected_role,
        critical_missing_skills=critical_missing_skills
    )

    # === SIMPLIFIED METRICS ===
    skill_match_percentage = int((len(matched_skills) / len(jd_skills)) * 100) if len(jd_skills) > 0 else 0
    bonus_percentage = min(len(bonus_skills) * 2, 20)  # Cap bonus at 20%
    
    # === RESPONSE ===
    response = {
        "resume_skills": resume_skills,
        "job_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "bonus_skills": bonus_skills,
        "detected_role": detected_role,
        "experience_level": experience_level,
        "critical_missing_skills": critical_missing_skills,
        "match_classification": match_classification,
        
        # Simplified Metrics
        "skill_match_percentage": skill_match_percentage,
        "bonus_percentage": bonus_percentage,
        
        # 7-Factor Score Breakdown (PRIMARY)
        "score_breakdown_7_factor": {
            "required_skill_coverage": factor1,
            "skill_relevance": factor2,
            "skill_depth_signals": factor3,
            "experience_level_alignment": factor4,
            "domain_context": factor5,
            "ats_optimization": factor6,
            "signal_vs_noise_ratio": factor7,
        },
        
        # Legacy 3-layer breakdown (kept for compatibility)
        "scoring_breakdown": {
            "final_score": final_7_factor_score,
            "text_similarity_score": round(text_similarity, 2)
        },
        
        "suggestions": suggestions
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




