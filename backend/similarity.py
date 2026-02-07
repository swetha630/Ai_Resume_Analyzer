from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_text, jd_text):
    """Calculate TF-IDF cosine similarity (used for Layer 3 - text similarity bonus)"""
    documents = [resume_text, jd_text]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return round(similarity_score * 100, 2)


def calculate_comprehensive_score(matched_skills, job_skills, bonus_skills, text_similarity):
    """
    3-Layer Scoring System:
    - Layer 1 (70%): Primary skill match score based on job requirements
    - Layer 2 (20%): Bonus for extra relevant skills
    - Layer 3 (10%): NLP text similarity
    """
    
    job_skills_count = len(job_skills)
    matched_count = len(matched_skills)
    bonus_count = len(bonus_skills)
    
    # Layer 1: Core skill match (PRIMARY - 70% weight)
    # Score based on job requirements, not resume length
    if job_skills_count > 0:
        skill_match_score = (matched_count / job_skills_count) * 100
    else:
        skill_match_score = 0
    
    # Layer 2: Extra skills bonus (20% weight)
    # Each extra skill is worth up to 2% (max 20% if 10+ extra skills)
    bonus_score = min(bonus_count * 2, 20)
    
    # Layer 3: Text similarity (10% weight)
    # Use as small modifier, not the base
    text_similarity_score = min(text_similarity, 100)
    
    # Weighted final score
    final_score = (
        0.7 * skill_match_score +
        0.2 * bonus_score +
        0.1 * text_similarity_score
    )
    
    return {
        "skill_match_score": round(skill_match_score, 2),
        "bonus_score": round(bonus_score, 2),
        "text_similarity_score": round(text_similarity_score, 2),
        "final_score": round(final_score, 2)
    }
