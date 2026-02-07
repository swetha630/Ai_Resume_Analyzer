# Skill synonyms for normalization (LEVEL 1: Synonym Engine)
SKILL_SYNONYMS = {
    "js": "javascript",
    "html5": "html",
    "css3": "css",
    "ml": "machine learning",
    "deep learning": "machine learning",
    "nlp": "machine learning",
    "data science": "machine learning",
    "ai": "machine learning",
    "java script": "javascript",
    "react.js": "react",
    "nodejs": "node",
    "node.js": "node",
    "postgres": "sql",
    "postgresql": "sql",
    "nosql": "database",
    "mongodb": "database",
    "frontend": "html",
    "backend": "python",
    "rest": "apis",
    "api": "apis",
    "expressjs": "javascript",
    "express.js": "javascript",
}

# Role-aware skill classification (LEVEL 1: Role Weighting)
ROLE_SKILL_MAP = {
    "frontend": ["javascript", "react", "html", "css"],
    "backend": ["python", "java", "flask", "django", "sql", "database", "apis"],
    "full-stack": ["javascript", "react", "python", "flask", "sql", "html", "css"],
    "ml": ["python", "machine learning", "nlp", "data structures", "algorithms"],
}

# Core skills by role (important for confidence-aware labels)
CORE_SKILLS_BY_ROLE = {
    "frontend": ["javascript", "html", "css"],
    "backend": ["python", "sql"],
    "full-stack": ["javascript", "python", "sql"],
    "ml": ["python", "machine learning"],
}


def normalize_skill(skill):
    """Normalize skill using synonym map"""
    normalized = SKILL_SYNONYMS.get(skill.lower(), skill.lower())
    return normalized.strip()


def extract_skills(text):
    skills_list = [
        "python", "java", "sql", "mysql", "database",
        "machine learning", "deep learning", "nlp", "data science", "ai",
        "data structures", "algorithms",
        "html", "css", "javascript", "react", "node",
        "flask", "django", "apis", "rest",
        "git"
    ]

    text = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            # Normalize the found skill
            normalized_skill = normalize_skill(skill)
            found_skills.append(normalized_skill)

    # Remove duplicates and return
    return list(set(found_skills))


def detect_job_role(job_skills):
    """
    Detect the primary job role based on skills (LEVEL 1: Role Detection)
    Returns: frontend, backend, full-stack, or ml
    """
    job_skills_set = set(job_skills)
    
    role_scores = {
        "frontend": len(job_skills_set & set(ROLE_SKILL_MAP["frontend"])),
        "backend": len(job_skills_set & set(ROLE_SKILL_MAP["backend"])),
        "ml": len(job_skills_set & set(ROLE_SKILL_MAP["ml"])),
    }
    
    # Detect full-stack if both frontend and backend skills present
    if role_scores["frontend"] >= 2 and role_scores["backend"] >= 2:
        return "full-stack"
    
    # Return role with highest score
    best_role = max(role_scores, key=role_scores.get)
    if role_scores[best_role] > 0:
        return best_role
    
    return "full-stack"  # Default to full-stack if uncertain


def get_critical_missing_skills(missing_skills, detected_role):
    """
    Get core/critical missing skills for the detected role (LEVEL 1: Confidence)
    """
    core_skills = CORE_SKILLS_BY_ROLE.get(detected_role, [])
    critical = [skill for skill in missing_skills if skill in core_skills]
    return critical
