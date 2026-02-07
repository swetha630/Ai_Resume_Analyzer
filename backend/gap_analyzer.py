def find_skill_gap(resume_skills, jd_skills):
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    missing_skills = list(jd_set - resume_set)
    return missing_skills


def generate_suggestions(missing_skills, match_score):
    suggestions = []

    if missing_skills:
        for skill in missing_skills:
            suggestions.append(f"Consider learning or adding a project on {skill}")

    if match_score < 60:
        suggestions.append("Improve resume by adding relevant keywords and project experience")

    if not suggestions:
        suggestions.append("Your resume is a strong match for this job")

    return suggestions
