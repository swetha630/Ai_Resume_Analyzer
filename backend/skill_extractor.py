def extract_skills(text):
    skills_list = [
        "python", "java", "sql", "mysql",
        "machine learning", "deep learning", "nlp",
        "data structures", "algorithms",
        "html", "css", "javascript", "react",
        "flask", "django", "git"
    ]

    text = text.lower()
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))
