import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text


def parse_resume_sections(resume_text):
    """
    Parse resume into sections: skills, projects, experience, education
    Returns dict with extracted sections for deeper analysis
    """
    text_lower = resume_text.lower()
    
    # Section headers to look for (common patterns)
    section_markers = {
        "skills": r"(skills|technical skills|languages|technologies|proficiencies)",
        "projects": r"(projects|portfolio|work samples|applications)",
        "experience": r"(experience|professional experience|work experience|job history|employment)",
        "education": r"(education|academic|degree|university|college)",
    }
    
    sections = {
        "skills": "",
        "projects": "",
        "experience": "",
        "education": "",
        "other": ""
    }
    
    # Find section positions
    section_positions = {}
    for section_name, pattern in section_markers.items():
        match = re.search(pattern, text_lower)
        if match:
            section_positions[section_name] = match.start()
    
    # Extract text for each section
    if section_positions:
        sorted_sections = sorted(section_positions.items(), key=lambda x: x[1])
        
        for i, (section_name, pos) in enumerate(sorted_sections):
            start = pos
            # Find end position (start of next section or end of text)
            if i + 1 < len(sorted_sections):
                end = sorted_sections[i + 1][1]
            else:
                end = len(resume_text)
            
            sections[section_name] = resume_text[start:end]
    else:
        sections["other"] = resume_text
    
    return sections


def detect_skill_depth(resume_sections):
    """
    Detect if skills are just listed or actually used in projects/experience
    Returns dict mapping skills to depth level: 'used' or 'listed'
    """
    # Action verbs indicating skill usage
    action_verbs = [
        "build", "built", "develop", "developed", "implement", "implemented",
        "create", "created", "design", "designed", "deploy", "deployed",
        "manage", "managed", "optimize", "optimized", "write", "wrote",
        "engineer", "engineered", "architect", "architected", "lead", "led",
        "maintain", "maintained", "test", "tested", "debug", "debugged"
    ]
    
    depth_map = {}
    
    # Check projects and experience for skill usage
    context_text = (resume_sections.get("projects", "") + " " + 
                    resume_sections.get("experience", "")).lower()
    
    skills_section = resume_sections.get("skills", "").lower()
    
    # If skill appears with action verb in projects/experience, it's "used"
    # If only in skills section, it's "listed"
    # This is a simple heuristic
    
    return depth_map


def extract_experience_level(resume_sections):
    """
    Detect experience level: internship, junior, mid, senior
    Returns: 'internship', 'junior', 'mid', 'senior'
    """
    experience_text = (resume_sections.get("experience", "") + " " +
                      resume_sections.get("education", "")).lower()
    
    # Senior indicators
    if any(kw in experience_text for kw in ["senior", "lead", "manager", "architect", "principal"]):
        return "senior"
    
    # Mid indicators
    elif any(kw in experience_text for kw in ["mid-level", "intermediate", "years", "6+ years", "5+ years"]):
        return "mid"
    
    # Junior indicators
    elif any(kw in experience_text for kw in ["junior", "associate", "2 years", "3 years", "recent", "graduate"]):
        return "junior"
    
    # Internship indicators
    elif any(kw in experience_text for kw in ["internship", "intern", "gpa", "coursework", "projects only"]):
        return "internship"
    
    # Default based on years of experience mentioned
    years_match = re.search(r"(\d+)\+?\s*years", experience_text)
    if years_match:
        years = int(years_match.group(1))
        if years >= 7:
            return "senior"
        elif years >= 4:
            return "mid"
        elif years >= 2:
            return "junior"
    
    return "junior"  # Default


def detect_domain_context(resume_sections, job_description=""):
    """
    Detect if candidate has worked in related domain
    Returns relevance score 0-100
    """
    resume_text = " ".join(resume_sections.values()).lower()
    jd_text = job_description.lower()
    
    # Domain keywords
    domain_patterns = {
        "web": ["frontend", "backend", "react", "nodejs", "express", "api", "rest", "http"],
        "data": ["data", "sql", "database", "analytics", "visualization", "etl", "pipeline"],
        "ml": ["machine learning", "neural", "tensorflow", "sklearn", "prediction", "training"],
        "mobile": ["mobile", "ios", "android", "flutter", "react native"],
        "devops": ["docker", "kubernetes", "ci/cd", "jenkins", "deployment", "infrastructure"],
    }
    
    # Simple scoring: count domain keyword matches
    resume_domain_matches = 0
    jd_domain_matches = 0
    
    for domain, keywords in domain_patterns.items():
        for keyword in keywords:
            if keyword in resume_text:
                resume_domain_matches += 1
            if keyword in jd_text:
                jd_domain_matches += 1
    
    if jd_domain_matches == 0:
        return 50  # Neutral if can't determine
    
    relevance = (resume_domain_matches / jd_domain_matches) * 100
    return min(relevance, 100)
