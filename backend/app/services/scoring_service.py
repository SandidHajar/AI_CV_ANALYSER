from typing import Dict, List, Any

class ScoringService:
    def calculate_score(
        self, 
        categorized_skills: Dict[str, List[str]], 
        experience_level: str,
        experience_years: float,
        complexity_signals: List[str],
        devops_signals: List[str]
    ) -> Dict[str, Any]:
        """
        Multi-dimensional scoring engine:
        - Skill coverage (40%)
        - Skill depth (20%)
        - Experience signal (20%)
        - Project complexity (10%)
        - DevOps maturity (10%)
        """
        
        # 1. Skill Coverage (40%) - How many categories are covered?
        categories_count = sum(1 for skills in categorized_skills.values() if len(skills) > 0)
        coverage_score = (categories_count / 4) * 100
        
        # 2. Skill Depth (20%) - Average skills per active category
        total_skills = sum(len(skills) for skills in categorized_skills.values())
        depth_score = min((total_skills / 8) * 100, 100) if categories_count > 0 else 0
        
        # 3. Experience Signal (20%)
        if experience_level == "Senior":
            exp_score = min((experience_years / 10) * 100, 100) if experience_years >= 5 else 80
        elif experience_level == "Mid":
            exp_score = min((experience_years / 5) * 100, 100) if experience_years >= 2 else 60
        else:
            exp_score = min((experience_years / 2) * 100, 100) if experience_years > 0 else 40
            
        # 4. Project Complexity (10%)
        complexity_score = min((len(complexity_signals) / 4) * 100, 100)
        
        # 5. DevOps Maturity (10%)
        devops_score = min((len(devops_signals) / 4) * 100, 100)
        
        # Weighted Total
        weighted_score = (
            (coverage_score * 0.40) +
            (depth_score * 0.20) +
            (exp_score * 0.20) +
            (complexity_score * 0.10) +
            (devops_score * 0.10)
        )
        
        # Normalization based on level (No unrealistic scores)
        normalized_score = self._normalize(weighted_score, experience_level)
        
        return {
            "total": int(normalized_score),
            "breakdown": {
                "skill_coverage": int(coverage_score),
                "skill_depth": int(depth_score),
                "experience": int(exp_score),
                "project_complexity": int(complexity_score),
                "devops_maturity": int(devops_score)
            },
            "interpretation": self._get_interpretation(normalized_score, experience_level)
        }

    def _normalize(self, score: float, level: str) -> float:
        # Prevent juniors from hitting high scores regardless of keyword stuffing
        if level == "Junior":
            return min(score * 0.8, 78)
        if level == "Mid":
            return min(score * 0.9, 88)
        # Seniors can reach 98 but never 100
        return min(score, 98)

    def fuse_with_ai(self, rule_results: Dict[str, Any], ai_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fusion Engine:
        - Combines Rule-based score with AI adjustments (max +/- 10)
        - Enforces global score bounds (60-88)
        - Finalizes conservative level detection
        """
        base_score = rule_results["total"]
        ai_adjustment = max(-10, min(10, ai_results.get("score_adjustment", 0)))
        
        # Hybrid Score
        final_score = base_score + ai_adjustment
        
        # Enforce conservative bounds (60-88 as requested)
        final_score = max(60, min(88, final_score))
        
        # Conservative Level Selection
        rule_level = rule_results.get("experience_level", "Junior")
        ai_level = ai_results.get("role_level", "Junior")
        
        # If AI says Senior but rules say Junior, stay Junior or Mid
        levels = ["Junior", "Mid", "Senior"]
        rule_idx = levels.index(rule_level)
        ai_idx = levels.index(ai_level)
        
        # Take the most conservative level or at most 1 level higher than rule-based
        final_idx = min(ai_idx, rule_idx + 1)
        final_level = levels[final_idx]
        
        return {
            "total": int(final_score),
            "breakdown": rule_results["breakdown"],
            "interpretation": ai_results.get("interpretation") or rule_results["interpretation"],
            "experience_level": final_level,
            "confidence": ai_results.get("confidence", 0.5)
        }

    def _get_interpretation(self, score: float, level: str) -> str:
        if score >= 90: return f"Elite {level} profile with exceptional technical depth."
        if score >= 80: return f"Strong {level} candidate, highly recommended for technical roles."
        if score >= 70: return f"Competent {level} profile, meets core market expectations."
        if score >= 60: return f"Solid {level} foundation, potential for rapid growth."
        return f"Developing {level} profile, requires further technical strengthening."

scoring_service = ScoringService()
