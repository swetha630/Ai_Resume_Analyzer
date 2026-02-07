"""
7-Factor Resume Scoring System

Evaluates resumes based on:
1. Required skill coverage (40%) - MOST IMPORTANT
2. Skill relevance (25%) - Role alignment
3. Skill depth signals (15%) - Used vs listed
4. Experience level alignment (10%) - Appropriate level
5. Domain context (5%) - Related domain experience
6. ATS optimization (3%) - Keyword clarity
7. Signal vs noise (2%) - Focus vs scattered
"""

from skill_extractor import CORE_SKILLS_BY_ROLE, ROLE_SKILL_MAP


class ComprehensiveScorer:
    """7-Factor scoring system for professional resume analysis"""
    
    def __init__(self, detected_role, experience_level):
        self.detected_role = detected_role
        self.experience_level = experience_level
        self.scores = {}
    
    def score_factor_1_required_skills(self, matched_skills, jd_skills, missing_skills):
        """
        Factor 1: Required Skill Coverage (40% weight) - MOST IMPORTANT
        
        Evaluates: Does candidate have must-have skills?
        
        Scoring:
        - 100% match: 100 points
        - 80% match: 90 points (missing non-critical)
        - 50% match: 60 points (missing critical)
        - 25% match: 30 points
        - 0%: 0 points
        """
        if len(jd_skills) == 0:
            return 100
        
        match_percentage = (len(matched_skills) / len(jd_skills)) * 100
        
        # Non-linear scoring: emphasis on having core skills
        if match_percentage >= 90:
            score = 100
        elif match_percentage >= 80:
            score = 90
        elif match_percentage >= 70:
            score = 80
        elif match_percentage >= 60:
            score = 70
        elif match_percentage >= 50:
            score = 60
        elif match_percentage >= 30:
            score = 40
        else:
            score = max(0, match_percentage * 0.5)
        
        self.scores["required_skills"] = round(score, 1)
        return score
    
    def score_factor_2_skill_relevance(self, resume_skills, jd_skills):
        """
        Factor 2: Skill Relevance (25% weight)
        
        Evaluates: Are skills aligned with role type?
        
        Scores skills by relevance to detected role.
        Frontend skills high weight for frontend role, etc.
        """
        core_skills = CORE_SKILLS_BY_ROLE.get(self.detected_role, [])
        
        relevant_skills = 0
        matched_relevant = 0
        
        for skill in jd_skills:
            relevant_skills += 1
            if skill in resume_skills and skill in core_skills:
                matched_relevant += 1
            elif skill in resume_skills:
                # Matched but not in core - give partial credit
                matched_relevant += 0.5
        
        if relevant_skills == 0:
            return 50  # Neutral
        
        relevance_percentage = (matched_relevant / relevant_skills) * 100
        
        # Scoring with emphasis on core skills
        if relevance_percentage >= 90:
            score = 100
        elif relevance_percentage >= 70:
            score = 85
        elif relevance_percentage >= 50:
            score = 70
        elif relevance_percentage >= 30:
            score = 50
        else:
            score = max(0, relevance_percentage * 0.8)
        
        self.scores["skill_relevance"] = round(score, 1)
        return score
    
    def score_factor_3_skill_depth(self, resume_sections, matched_skills):
        """
        Factor 3: Skill Depth Signals (15% weight)
        
        Evaluates: Are skills just listed or actually used?
        
        Checks if skills appear in projects/experience with action verbs
        Penalizes skills that only appear in skill list
        """
        action_verbs = [
            "build", "built", "develop", "developed", "implement", "implemented",
            "create", "created", "design", "designed", "deploy", "deployed",
            "manage", "managed", "optimize", "optimized", "architect", "lead"
        ]
        
        projects_exp_text = (
            resume_sections.get("projects", "") + " " + 
            resume_sections.get("experience", "")
        ).lower()
        
        skills_with_depth = 0
        
        for skill in matched_skills:
            skill_lower = skill.lower()
            # Check if skill appears with action verb (indicating usage)
            for verb in action_verbs:
                if verb in projects_exp_text and skill_lower in projects_exp_text:
                    # Check if they're reasonably close
                    if projects_exp_text.find(verb) < projects_exp_text.find(skill_lower) + 500:
                        skills_with_depth += 1
                        break
            else:
                # Skill found but no action verb - still credit 0.3
                if skill_lower in projects_exp_text:
                    skills_with_depth += 0.3
        
        if len(matched_skills) == 0:
            return 50  # Neutral if no matched skills
        
        depth_percentage = (skills_with_depth / len(matched_skills)) * 100
        
        # Scoring
        if depth_percentage >= 80:
            score = 100
        elif depth_percentage >= 60:
            score = 85
        elif depth_percentage >= 40:
            score = 70
        elif depth_percentage >= 20:
            score = 50
        else:
            score = 30
        
        self.scores["skill_depth"] = round(score, 1)
        return score
    
    def score_factor_4_experience_alignment(self, missing_skills_count, jd_skills_count):
        """
        Factor 4: Experience Level Alignment (10% weight)
        
        Evaluates: Is experience level appropriate?
        
        Internships: Learning potential matters, projects > experience
        Entry-level: Some gaps acceptable
        Mid/Senior: Fewer gaps acceptable
        """
        if jd_skills_count == 0:
            return 100
        
        missing_percentage = (missing_skills_count / jd_skills_count) * 100
        
        if self.experience_level == "internship":
            # Interns: More forgiving on missing skills
            if missing_percentage <= 30:
                score = 100
            elif missing_percentage <= 50:
                score = 85
            elif missing_percentage <= 70:
                score = 70
            else:
                score = 50
        
        elif self.experience_level == "junior":
            # Junior: Some gap acceptable
            if missing_percentage <= 20:
                score = 100
            elif missing_percentage <= 40:
                score = 85
            elif missing_percentage <= 60:
                score = 70
            else:
                score = 50
        
        else:  # mid or senior
            # Mid/Senior: Fewer gaps acceptable
            if missing_percentage <= 10:
                score = 100
            elif missing_percentage <= 25:
                score = 90
            elif missing_percentage <= 40:
                score = 75
            else:
                score = 50
        
        self.scores["experience_alignment"] = round(score, 1)
        return score
    
    def score_factor_5_domain_context(self, domain_relevance_score):
        """
        Factor 5: Domain & Context Alignment (5% weight)
        
        Evaluates: Has candidate worked in related domain?
        
        domain_relevance_score: 0-100 from domain detection
        """
        # Domain context improves confidence, not core eligibility
        # So we use it more directly
        self.scores["domain_context"] = round(domain_relevance_score, 1)
        return domain_relevance_score
    
    def score_factor_6_ats_optimization(self, resume_text):
        """
        Factor 6: ATS & Keyword Optimization (3% weight)
        
        Evaluates: Can automated system identify relevant info?
        
        Checks for:
        - Standard section names
        - Clear skill mentions
        - Keyword consistency
        """
        resume_lower = resume_text.lower()
        
        # Check for standard section headers
        section_headers = ["skills", "experience", "projects", "education", "technical"]
        sections_found = sum(1 for header in section_headers if header in resume_lower)
        
        # Check for common ATS-friendly patterns
        ats_score = 0
        
        # Has clear sections
        if sections_found >= 3:
            ats_score += 30
        elif sections_found >= 2:
            ats_score += 20
        else:
            ats_score += 10
        
        # Has bullet points or numbered list
        if "•" in resume_text or "•" in resume_text or "-" in resume_text[:100]:
            ats_score += 25
        
        # Has contact info pattern (email, phone)
        if any(pattern in resume_lower for pattern in ["@", "//", "http"]):
            ats_score += 20
        
        # Has consistent formatting (not all caps, not excessive symbols)
        caps_ratio = sum(1 for c in resume_text if c.isupper()) / max(len(resume_text), 1)
        if caps_ratio < 0.3:  # Less than 30% caps
            ats_score += 15
        
        # Normalize to 0-100
        ats_score = min(ats_score, 100)
        
        self.scores["ats_optimization"] = round(ats_score, 1)
        return ats_score
    
    def score_factor_7_signal_noise_ratio(self, bonus_skills, missing_skills):
        """
        Factor 7: Signal vs Noise Ratio (2% weight)
        
        Evaluates: Is resume focused or scattered?
        
        Relevant extra skills → bonus
        Unrelated skills → neutral (not penalty)
        Missing core skills → penalty only
        """
        # Bonus skills should be limited and relevant
        # Too many extra unrelated skills = noise
        
        bonus_count = len(bonus_skills)
        missing_count = len(missing_skills)
        
        if missing_count > 0:
            # If missing core skills, any extra skills don't help much
            score = 50
        elif bonus_count == 0:
            # All skills are either matched or missing
            score = 75
        elif bonus_count <= 3:
            # Few extra skills - focused resume
            score = 90
        elif bonus_count <= 6:
            # Moderate extra skills
            score = 75
        else:
            # Many extra skills - possible noise
            score = 60
        
        self.scores["signal_noise"] = round(score, 1)
        return score
    
    def calculate_weighted_score(self, factor_scores):
        """
        Calculate final weighted score from all 7 factors
        
        Weights:
        1. Required skills: 40%
        2. Skill relevance: 25%
        3. Skill depth: 15%
        4. Experience alignment: 10%
        5. Domain context: 5%
        6. ATS optimization: 3%
        7. Signal vs noise: 2%
        """
        weights = {
            "required_skills": 0.40,
            "skill_relevance": 0.25,
            "skill_depth": 0.15,
            "experience_alignment": 0.10,
            "domain_context": 0.05,
            "ats_optimization": 0.03,
            "signal_noise": 0.02,
        }
        
        weighted_score = 0
        for factor, weight in weights.items():
            if factor in factor_scores:
                weighted_score += factor_scores[factor] * weight
        
        return round(weighted_score, 2)
    
    def generate_score_breakdown(self):
        """Return all 7 factor scores"""
        return self.scores
