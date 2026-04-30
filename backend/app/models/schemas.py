from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional

# ---------- Request Model ----------
class CVAnalyzeRequest(BaseModel):
    cv_text: str = Field(..., min_length=10, description="Raw CV text")
    weaknesses: Optional[List[str]] = Field(default=None, description="Optional weaknesses")

    @field_validator('cv_text', mode='before')
    @classmethod
    def sanitize_text(cls, v):
        """PostgreSQL does not allow null bytes \x00 in text fields."""
        if isinstance(v, str):
            return v.replace('\x00', '')
        return v

    @field_validator('weaknesses', mode='before')
    @classmethod
    def empty_list_if_none(cls, v):
        """Convert None to empty list to avoid validation error."""
        return v if v is not None else []

# ---------- Response Model ----------
class CVAnalyzeResponse(BaseModel):
    skills: List[str] = Field(default_factory=list)
    score: int = Field(0, ge=0, le=100)
    score_breakdown: Dict[str, int] = Field(default_factory=dict)
    interpretation: str
    experience_level: str
    summary: str
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    confidence: float = Field(0.0, ge=0.0, le=1.0)

# ---------- Text Extraction Response ----------
class TextExtractionResponse(BaseModel):
    text: str