import logging
from typing import Dict, List, Any
from app.models.schemas import CVAnalyzeRequest, CVAnalyzeResponse
from app.utils.text_utils import extract_skills_by_category, detect_experience_level, detect_experience_years, extract_complexity_signals, extract_devops_signals
from app.services.scoring_service import scoring_service
from app.services.openai_service import openai_service

logger = logging.getLogger(__name__)

async def analyze_cv_service(request: CVAnalyzeRequest) -> CVAnalyzeResponse:
    cv_text = request.cv_text
    
    # 1. Step A: Rule-based Analysis (Local)
    categorized_skills = extract_skills_by_category(cv_text)
    all_skills = [skill for sublist in categorized_skills.values() for skill in sublist]
    experience_level = detect_experience_level(cv_text)
    experience_years = detect_experience_years(cv_text)
    complexity_signals = extract_complexity_signals(cv_text)
    devops_signals = extract_devops_signals(cv_text)
    
    rule_results = scoring_service.calculate_score(
        categorized_skills, 
        experience_level, 
        experience_years,
        complexity_signals,
        devops_signals
    )
    rule_results["experience_level"] = experience_level # Ensure level is passed for fusion
    
    # 2. Step B: AI Analysis (OpenAI)
    try:
        ai_results = await openai_service.analyze_cv(cv_text)
        if ai_results:
            # 3. Step C: Hybrid Fusion
            fused_data = scoring_service.fuse_with_ai(rule_results, ai_results)
            
            response_data = {
                "skills": all_skills,
                "score": fused_data["total"],
                "score_breakdown": fused_data["breakdown"],
                "interpretation": fused_data["interpretation"],
                "experience_level": fused_data["experience_level"],
                "summary": ai_results["summary"],
                "strengths": ai_results["strengths"],
                "weaknesses": ai_results["weaknesses"],
                "confidence": fused_data["confidence"]
            }
            return CVAnalyzeResponse(**response_data)
            
    except Exception as e:
        logger.error(f"AI Analysis failed or timed out: {e}")
        
    # 4. Fallback: Use only rule-based results if AI fails
    logger.info("Falling back to rule-based analysis")
    response_data = {
        "skills": all_skills,
        "score": max(60, min(88, rule_results["total"])), # Enforce global bounds even in fallback
        "score_breakdown": rule_results["breakdown"],
        "interpretation": rule_results["interpretation"],
        "experience_level": experience_level,
        "summary": _generate_fallback_summary(all_skills, experience_level),
        "strengths": _generate_fallback_strengths(categorized_skills),
        "weaknesses": _generate_fallback_weaknesses(categorized_skills),
        "confidence": 0.3 # Low confidence for fallback
    }
    return CVAnalyzeResponse(**response_data)

def _generate_fallback_summary(skills: List[str], level: str) -> str:
    if not skills:
        return f"Professional in transition with a focus on learning new technologies. Suitable for {level} positions."
    
    top_skills = skills[:3]
    skills_str = ", ".join(top_skills)
    return f"{level} developer with specialized skills in {skills_str}. Demonstrates a solid foundation for modern web environments."

def _generate_fallback_strengths(categorized_skills: Dict[str, List[str]]) -> List[str]:
    strengths = []
    if categorized_skills.get("frontend"):
        strengths.append(f"Strong frontend foundations ({', '.join(categorized_skills['frontend'][:2])})")
    if categorized_skills.get("backend"):
        strengths.append(f"Backend proficiency with {categorized_skills['backend'][0]}")
    if categorized_skills.get("devops"):
        strengths.append("Knowledge of modern DevOps and version control")
    
    if len(strengths) < 3:
        strengths.append("Clear professional objective and structured profile")
        
    return strengths[:3]

def _generate_fallback_weaknesses(categorized_skills: Dict[str, List[str]]) -> List[str]:
    weaknesses = []
    if not categorized_skills.get("devops"):
        weaknesses.append("Limited exposure to DevOps and cloud infrastructure")
    if not categorized_skills.get("database"):
        weaknesses.append("Potential gap in database management and optimization")
    
    if len(weaknesses) < 2:
        weaknesses.append("Lack of experience with large-scale distributed systems")
        
    return weaknesses[:2]
