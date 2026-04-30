import re
from typing import Dict, List, Set

SKILL_CATEGORIES = {
    "frontend": {
        "react", "javascript", "typescript", "vue.js", "angular", "html", "css", "tailwind", "next.js", "sass"
    },
    "backend": {
        "python", "node.js", "laravel", "fastapi", "django", "flask", "spring", "go", "ruby", "php", "c#", "java"
    },
    "database": {
        "postgresql", "mongodb", "mysql", "sql", "nosql", "redis", "elasticsearch", "oracle", "mariadb"
    },
    "devops": {
        "docker", "kubernetes", "aws", "azure", "gcp", "git", "jenkins", "terraform", "ansible", "linux"
    }
}

def extract_skills_by_category(text: str) -> Dict[str, List[str]]:
    text_lower = text.lower()
    found_skills = {cat: [] for cat in SKILL_CATEGORIES}
    
    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            escaped_skill = re.escape(skill)
            if re.search(rf"\b{escaped_skill}\b", text_lower):
                # Formatting
                if skill in ["php", "html", "css", "sql", "aws", "gcp"]:
                    formatted = skill.upper()
                elif skill == "node.js":
                    formatted = "Node.js"
                elif skill == "vue.js":
                    formatted = "Vue.js"
                elif skill == "next.js":
                    formatted = "Next.js"
                else:
                    formatted = skill.title()
                
                found_skills[category].append(formatted)
                
    return found_skills

def extract_complexity_signals(text: str) -> List[str]:
    complexity_keywords = {
        "microservices", "distributed systems", "scalable", "high-availability",
        "real-time", "cloud-native", "architecture", "serverless", "event-driven",
        "machine learning", "big data", "concurrency", "performance optimization"
    }
    text_lower = text.lower()
    return [kw for kw in complexity_keywords if kw in text_lower]

def extract_devops_signals(text: str) -> List[str]:
    devops_keywords = {
        "ci/cd", "pipeline", "automation", "infrastructure as code", "terraform",
        "ansible", "docker", "kubernetes", "jenkins", "github actions", "monitoring",
        "prometheus", "grafana", "observability"
    }
    text_lower = text.lower()
    return [kw for kw in devops_keywords if kw in text_lower]

def detect_experience_years(text: str) -> float:
    text_lower = text.lower()
    # Find patterns like "5 years", "10+ years", "3.5 years"
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*\+?\s*years?", text_lower)
    if matches:
        # Return the highest value found
        return max(float(m) for m in matches)
    return 0.0

def detect_experience_level(text: str) -> str:
    years = detect_experience_years(text)
    text_lower = text.lower()
    
    if years >= 5 or re.search(r"(senior|lead|principal|architect|chef\s+de\s+projet)", text_lower):
        return "Senior"
    if years >= 2 or re.search(r"(mid-level|confirmé|3\s*years?|4\s*years?)", text_lower):
        return "Mid"
    return "Junior"
