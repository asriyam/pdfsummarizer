from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
import os

class Citation(BaseModel):
    authors: List[str] 
    title: str
    journal: Optional[str] = None
    year: Optional[int] = None
    doi: Optional[str] = None
    page_numbers: Optional[str] = None
    citation_context: str = Field(..., description="How this citation is used in the paper")

class KeyFinding(BaseModel):
    finding: str = Field(..., description="Main finding or result")
    evidence: str = Field(..., description="Supporting evidence or data")
    page_reference: Optional[int] = None
    significance: str = Field(..., description="Why this finding is important")

class Methodology(BaseModel):
    approach: str = Field(..., description="Overall methodological approach")
    data_sources: List[str] = Field(..., description="Data sources used")
    analysis_methods: List[str] = Field(..., description="Analysis techniques employed")
    sample_size: Optional[str] = None
    limitations: List[str] = Field(..., description="Acknowledged limitations")

class PaperSummary(BaseModel):
    title: str
    authors: List[str]
    abstract: str = Field(..., description="Original abstract or executive summary")
    research_question: str = Field(..., description="Main research question or objective")
    key_findings: List[KeyFinding] = Field(..., min_items=3, max_items=8)
    methodology: Methodology
    conclusions: str = Field(..., description="Main conclusions and implications")
    limitations: List[str] = Field(..., description="Study limitations")
    future_research: List[str] = Field(..., description="Suggested future research directions")
    citations: List[Citation] = Field(..., description="Key citations referenced")
    paper_category: str = Field(..., description="Type of research: empirical, theoretical, review, etc.")
    relevance_score: int = Field(..., ge=1, le=10, description="Relevance/impact score 1-10")

