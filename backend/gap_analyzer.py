def find_skill_gap(resume_skills, jd_skills):
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    missing_skills = list(jd_set - resume_set)
    return missing_skills


def get_bonus_skills(resume_skills, jd_skills):
    """Get extra skills on resume that aren't in job description"""
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)
    
    bonus_skills = list(resume_set - jd_set)
    return bonus_skills


def classify_match(comprehensive_score, critical_missing_skills=None):
    """
    Confidence-aware match classification using 7-factor score
    
    Parameters:
    - comprehensive_score: The 7-factor weighted score (0-100)
    - critical_missing_skills: List of core/critical missing skills for the role
    """
    if critical_missing_skills is None:
        critical_missing_skills = []
    
    has_critical_gaps = len(critical_missing_skills) > 0
    
    # 7-FACTOR BASED CLASSIFICATION
    if comprehensive_score >= 85:
        return "Strong Match"
    elif comprehensive_score >= 75 and not has_critical_gaps:
        return "Strong Match"
    elif comprehensive_score >= 65 and len(critical_missing_skills) <= 1:
        return "Moderate Match"
    elif comprehensive_score >= 50:
        return "Moderate Match"
    elif comprehensive_score >= 35:
        return "Developing Match"
    else:
        return "Early Stage"


# Skill priority categorization
CORE_SKILLS = {
    "frontend": ["javascript", "react", "html", "css"],
    "backend": ["python", "java", "flask", "django"],
    "database": ["sql", "mysql"],
    "ml": ["machine learning", "deep learning", "nlp"]
}

SECONDARY_SKILLS = ["git", "algorithms", "data structures", "testing"]

# Skill-specific actionable improvements
SKILL_ACTIONS = {
    "javascript": "Add a small JavaScript project demonstrating DOM manipulation, API calls, or form validation.",
    "react": "Build a React component-based project showcasing state management and reusable components.",
    "python": "Create a Python script or automation project that solves a real problem.",
    "java": "Develop a Java application or contribute to a Java open-source project.",
    "html": "Create at least one multi-page HTML project with semantic markup.",
    "css": "Build a responsive design project using CSS Grid or Flexbox.",
    "flask": "Create a Flask REST API with proper routing and error handling.",
    "django": "Build a full Django application with models, views, and URL routing.",
    "sql": "Write complex SQL queries and create a database schema project.",
    "mysql": "Design and optimize a MySQL database schema for a real-world scenario.",
    "machine learning": "Build an end-to-end ML project with data preprocessing, training, and evaluation.",
    "deep learning": "Implement a neural network using TensorFlow or PyTorch.",
    "nlp": "Create an NLP project like sentiment analysis, chatbot, or text classification.",
    "git": "Demonstrate active GitHub contributions with meaningful commits and documentation.",
}


def prioritize_missing_skills(missing_skills):
    """Categorize missing skills by priority (high/medium/low)"""
    high_priority = []
    medium_priority = []
    low_priority = []
    
    for skill in missing_skills:
        is_core = False
        # Check all core skill categories
        for category, skills_list in CORE_SKILLS.items():
            if skill in skills_list:
                high_priority.append(skill)
                is_core = True
                break
        
        if not is_core:
            if skill in SECONDARY_SKILLS:
                low_priority.append(skill)
            else:
                medium_priority.append(skill)
    
    return high_priority, medium_priority, low_priority


def find_bridging_suggestions(resume_skills, missing_skills, bonus_skills):
    """Find ways to bridge existing skills to missing ones"""
    bridging = []
    
    # Python/Flask + missing frontend skills
    if "python" in resume_skills and "flask" in resume_skills:
        frontend_missing = [s for s in missing_skills if s in CORE_SKILLS["frontend"]]
        if frontend_missing:
            bridging.append(
                f"Combine your Flask + Python expertise with HTML/CSS/JavaScript to create a full-stack project. "
                f"This directly addresses the {', '.join(frontend_missing)} gap."
            )
    
    # Java + missing web skills
    if "java" in resume_skills:
        web_missing = [s for s in missing_skills if s in CORE_SKILLS["frontend"]]
        if web_missing:
            bridging.append(
                "Use your Java knowledge to build a Spring Boot REST API with a frontend (HTML/CSS/JS). "
                "This creates a full-stack project that covers missing skills."
            )
    
    # Database + missing backend skills
    if ("sql" in resume_skills or "mysql" in resume_skills) and missing_skills:
        backend_missing = [s for s in missing_skills if s in CORE_SKILLS["backend"]]
        if backend_missing:
            bridging.append(
                "Leverage your database expertise by building a data-driven application using missing backend skills. "
                "This demonstrates practical integration."
            )
    
    return bridging


def group_missing_skills_into_projects(missing_skills, detected_role):
    """
    Group missing skills into realistic project-based learning paths
    Instead of per-skill nagging, suggest grouped skill projects
    """
    projects = []
    
    # Frontend project group
    frontend_skills = [s for s in missing_skills if s in CORE_SKILLS["frontend"]]
    if frontend_skills and len(frontend_skills) > 0:
        projects.append({
            "title": "Frontend Fundamentals Project",
            "description": f"Build an interactive web application combining {', '.join([s.title() for s in frontend_skills])}. Create a todo app, weather dashboard, or portfolio site to demonstrate your front-end capabilities.",
            "skills_covered": frontend_skills,
            "effort": "Beginner-friendly" if len(frontend_skills) <= 2 else "Intermediate"
        })
    
    # Backend project group
    backend_skills = [s for s in missing_skills if s in CORE_SKILLS["backend"]]
    if backend_skills and len(backend_skills) > 0:
        projects.append({
            "title": "Backend API Project",
            "description": f"Build a RESTful API using {', '.join([s.title() for s in backend_skills])}. Start with user authentication and expand to a full CRUD application.",
            "skills_covered": backend_skills,
            "effort": "Intermediate"
        })
    
    # Data/Database project group
    db_skills = [s for s in missing_skills if s in CORE_SKILLS["database"]]
    if db_skills and len(db_skills) > 0:
        projects.append({
            "title": "Database Design Project",
            "description": f"Design and implement a real-world database schema using {', '.join([s.title() for s in db_skills])}. Build queries for analytics, reporting, or e-commerce.",
            "skills_covered": db_skills,
            "effort": "Intermediate"
        })
    
    # ML/Data project group
    ml_skills = [s for s in missing_skills if s in CORE_SKILLS["ml"]]
    if ml_skills and len(ml_skills) > 0:
        projects.append({
            "title": "ML/Data Science Project",
            "description": f"Build an end-to-end project using {', '.join([s.title() for s in ml_skills])}. Try classification, regression, or NLP on a real dataset.",
            "skills_covered": ml_skills,
            "effort": "Advanced"
        })
    
    # Full-stack project (if missing both frontend and backend)
    if len(frontend_skills) > 0 and len(backend_skills) > 0:
        projects = []  # Replace individual projects with integrated one
        all_skills = frontend_skills + backend_skills
        projects.append({
            "title": "Full-Stack Application Project",
            "description": f"Build a complete application with {', '.join([s.title() for s in all_skills])}. Examples: social media app, note-taking app, project management tool.",
            "skills_covered": all_skills,
            "effort": "Intermediate to Advanced"
        })
    
    return projects


def generate_overall_verdict(skill_match_score, matched_count, total_job_skills, bonus_skills_count):
    """Generate an encouraging overall insight at the top"""
    if skill_match_score >= 80:
        return "Excellent! You're a strong candidate with comprehensive skill coverage."
    elif skill_match_score >= 70:
        coverage = int((matched_count / total_job_skills) * 100)
        missing_count = total_job_skills - matched_count
        return (
            f"You're very close to a strong match. You have {coverage}% of required skills. "
            f"Adding just {missing_count} more core skill(s) will significantly boost your match score."
        )
    elif skill_match_score >= 50:
        coverage = int((matched_count / total_job_skills) * 100)
        return (
            f"You have solid foundational skills ({coverage}% match). "
            f"Improving key competencies can elevate your candidacy to strong match territory."
        )
    else:
        return (
            "You have some relevant skills, but there are notable gaps. "
            "Focused skill development in core areas will dramatically improve your profile."
        )


def generate_comprehensive_suggestions(
    missing_skills, 
    resume_skills, 
    bonus_skills,
    comprehensive_score,
    matched_count,
    total_job_skills,
    detected_role="full-stack",
    critical_missing_skills=None
):
    """
    Generate smart, actionable suggestions with GROUP-BASED learning paths
    
    Instead of per-skill nagging, suggests realistic projects that combine skills.
    
    Parameters:
    - comprehensive_score: The 7-factor weighted score (0-100)
    - detected_role: Auto-detected job role (frontend, backend, ml, full-stack)
    - critical_missing_skills: Core skills missing for the role
    """
    if critical_missing_skills is None:
        critical_missing_skills = []
    
    result = {}
    
    # 1. Overall verdict/insight with role context
    role_context = f" for a {detected_role} position"
    skill_percentage = int((matched_count / total_job_skills) * 100) if total_job_skills > 0 else 0
    
    if comprehensive_score >= 85:
        result["overall_verdict"] = f"Excellent! You're a strong candidate{role_context}. Your comprehensive skill coverage aligns well with requirements."
    elif comprehensive_score >= 75:
        critical_focus = f" The {len(critical_missing_skills)} core skill(s) ({', '.join([s.title() for s in critical_missing_skills])}) are your priority." if critical_missing_skills else ""
        result["overall_verdict"] = (
            f"You're very close to a strong match{role_context}. With {skill_percentage}% of required skills, "
            f"focused development will propel you forward.{critical_focus}"
        )
    elif comprehensive_score >= 60:
        result["overall_verdict"] = (
            f"You have solid foundational skills ({skill_percentage}% match){role_context}. "
            f"Strategic projects will bridge the remaining gaps and elevate your candidacy."
        )
    else:
        result["overall_verdict"] = (
            f"You have some relevant skills{role_context}. Build a coherent learning path focusing on core areas."
        )
    
    result["skill_percentage"] = skill_percentage
    
    # 2. GROUP MISSING SKILLS INTO REALISTIC PROJECTS (NOT PER-SKILL)
    if missing_skills:
        project_groups = group_missing_skills_into_projects(missing_skills, detected_role)
        result["learning_projects"] = project_groups
    else:
        result["learning_projects"] = []
    
    # 3. STRATEGIC RECOMMENDATIONS (Not per-skill, but holistic advice)
    strategic_recommendations = []
    
    if comprehensive_score >= 75 and len(critical_missing_skills) <= 1:
        strategic_recommendations.append(
            "🎯 Priority: Build one focused project combining critical missing skills. This demonstrates mastery and fills immediate gaps."
        )
    elif comprehensive_score >= 60:
        strategic_recommendations.append(
            "🎯 Strategy: Pick ONE of the recommended learning projects above. Complete it fully to show depth, not breadth."
        )
    elif comprehensive_score >= 40:
        strategic_recommendations.append(
            "🎯 Foundation First: Start with fundamental projects listed above. Each builds blocks for more advanced work."
        )
    
    # Role-specific strategic advice
    if detected_role == "frontend":
        strategic_recommendations.append(
            "📱 Build Strategy: Create a portfolio of 2-3 frontend projects (progressively complex) showcasing responsive design and interactivity."
        )
    elif detected_role == "backend":
        strategic_recommendations.append(
            "⚙️ Build Strategy: Focus on API design and database patterns. Create projects demonstrating scalability and data integrity."
        )
    elif detected_role == "ml":
        strategic_recommendations.append(
            "🤖 Build Strategy: Create end-to-end ML projects: data collection → preprocessing → model → evaluation. Show real-world impact."
        )
    elif detected_role == "full-stack":
        strategic_recommendations.append(
            "🚀 Build Strategy: Execute ONE full-stack project well (frontend + backend + database). This proves comprehensive capability."
        )
    
    # GitHub/Portfolio advice
    if comprehensive_score < 85:
        strategic_recommendations.append(
            "📝 Portfolio Tip: Publish your projects on GitHub with clear README files, well-structured code, and documentation. This proves communication skills too."
        )
    
    result["strategic_recommendations"] = strategic_recommendations
    
    # 4. RESUME POSITIONING (One coherent strategy, not scattered advice)
    result["resume_positioning"] = {
        "headline": f"Position yourself as a strong {detected_role} candidate with growing expertise.",
        "project_section_tip": "Feature your learning projects prominently. Describe impact, not just features.",
        "skill_listing_tip": f"List skills that appear in your projects. Avoid skill inflation. Quality > Quantity."
    }
    
    if bonus_skills:
        result["resume_positioning"]["bonus_skills_mention"] = f"Highlight relevant bonus skills ({', '.join([s.title() for s in bonus_skills[:3]])}) in project descriptions where applicable."
    
    # 5. ENCOURAGEMENT
    if comprehensive_score >= 75:
        result["encouragement"] = "You're so close—finishing one strong project will make you highly competitive!"
    elif comprehensive_score >= 60:
        result["encouragement"] = "Your foundation is solid. Real projects will show growth and capability."
    elif comprehensive_score >= 40:
        result["encouragement"] = "Every expert path starts here. Focus on ONE project, finish it well, then build from there."
    else:
        result["encouragement"] = "Learning is non-linear. Start with fundamentals and practice consistently."
    
    return result
