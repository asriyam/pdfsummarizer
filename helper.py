import PyPDF2
from schema import PaperSummary
from typing import Dict, Any, List, Optional
import re

def extract_pdf(pdf_path:str) -> str:
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                text += f"\n[PAGE {page_num}]\n{page_text}\n"
            
            print(f"✅ Extracted text from {len(pdf_reader.pages)} pages")
            return text
    except Exception as e:
        print(f"❌ Error extracting PDF: {e}")
        return ""

def _extract_json(text: str) -> str:
    """Extract JSON from response and fix common formatting issues"""
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*$', '', text)

    start = text.find('{')
    end = text.rfind('}') + 1

    if start >= 0 and end > start:
        json_text = text[start:end]
    else:
        json_text = text.strip()
    
    # Don't escape single quotes - they are valid in JSON strings
    # Just make sure we handle the JSON properly
    fixed_text = json_text
    
    # Fix trailing commas before closing braces/brackets
    fixed_text = re.sub(r',(\s*[}\]])', r'\1', fixed_text)
    
    # Fix literal escape sequences that should be actual characters
    # The AI sometimes returns JSON with literal \n instead of actual newlines
    fixed_text = fixed_text.replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t')
    
    return fixed_text

def create_summary_prompt(paper_text: str) -> str:
    """Create optimized prompt for paper summarization"""
    return f"""
        You are an expert research analyst. Analyze this academic paper and provide a comprehensive structured summary.

        CRITICAL: Your response must be ONLY valid JSON following the exact schema below.

        Required JSON structure:
        {{
            "title": "paper title",
            "authors": ["author1", "author2"],
            "abstract": "paper's abstract or executive summary",
            "research_question": "main research question or objective", 
            "key_findings": [
                {{
                    "finding": "specific finding",
                    "evidence": "supporting evidence/data",
                    "page_reference": page_number_or_null,
                    "significance": "why this finding matters"
                }}
            ],
            "methodology": {{
                "approach": "overall methodological approach",
                "data_sources": ["source1", "source2"],
                "analysis_methods": ["method1", "method2"],
                "sample_size": "sample size or null",
                "limitations": ["limitation1", "limitation2"]
            }},
            "conclusions": "main conclusions and implications",
            "limitations": ["limitation1", "limitation2"],
            "future_research": ["direction1", "direction2"],
            "citations": [
                {{
                    "authors": ["author1", "author2"],
                    "title": "cited paper title",
                    "journal": "journal name or null",
                    "year": year_number_or_null,
                    "doi": "doi or null",
                    "page_numbers": "page range or null",
                    "citation_context": "how this citation is used"
                }}
            ],
            "paper_category": "empirical/theoretical/review/meta-analysis/case-study",
            "relevance_score": score_1_to_10
        }}

        ANALYSIS INSTRUCTIONS:
        1. Focus on extracting 3-8 KEY findings (most important results)
        2. Identify ALL major citations and explain their role
        3. Be specific about methodology - what exactly was done?
        4. Note page references when possible using [PAGE X] markers
        5. Assess limitations honestly
        6. Suggest concrete future research directions
        7. Rate relevance/impact on 1-10 scale (10 = groundbreaking)

        PAPER TEXT:
        {paper_text}

        Analyze thoroughly and return ONLY the JSON response.
        """

def format_summary(summary: PaperSummary) -> str:
    """Format summary for display"""
    output = []
    output.append("📄 RESEARCH PAPER SUMMARY")
    output.append("=" * 50)

    # Basic Info
    output.append(f"Title: {summary.title}")
    output.append(f"Authors: {', '.join(summary.authors)}")
    output.append(f"Category: {summary.paper_category}")
    output.append(f"Relevance Score: {summary.relevance_score}/10")

    # Research Question
    output.append(f"\n🎯 RESEARCH QUESTION:")
    output.append(summary.research_question)

    # Abstract
    output.append(f"\n📋 ABSTRACT:")
    output.append(summary.abstract[:300] + "..." if len(summary.abstract) > 300 else summary.abstract)

    # Key Findings
    output.append(f"\n🔍 KEY FINDINGS ({len(summary.key_findings)}):")
    for i, finding in enumerate(summary.key_findings, 1):
        output.append(f"{i}. {finding.finding}")
        output.append(f"   Evidence: {finding.evidence}")
        output.append(f"   Significance: {finding.significance}")
        if finding.page_reference:
            output.append(f"   (Page {finding.page_reference})")
        output.append("")

    # Methodology
    output.append(f"🔬 METHODOLOGY:")
    output.append(f"Approach: {summary.methodology.approach}")
    output.append(f"Data Sources: {', '.join(summary.methodology.data_sources)}")
    output.append(f"Analysis Methods: {', '.join(summary.methodology.analysis_methods)}")
    if summary.methodology.sample_size:
        output.append(f"Sample Size: {summary.methodology.sample_size}")

    # Conclusions
    output.append(f"\n💡 CONCLUSIONS:")
    output.append(summary.conclusions)

    # Limitations
    output.append(f"\n⚠️  LIMITATIONS:")
    for limitation in summary.limitations:
        output.append(f"• {limitation}")

    # Future Research
    output.append(f"\n🚀 FUTURE RESEARCH DIRECTIONS:")
    for direction in summary.future_research:
        output.append(f"• {direction}")

    # Citations
    output.append(f"\n📚 KEY CITATIONS ({len(summary.citations)}):")
    for i, citation in enumerate(summary.citations, 1):
        authors = ', '.join(citation.authors)
        year_str = f"({citation.year})" if citation.year else ""
        output.append(f"{i}. {authors} {year_str}")
        output.append(f"   \"{citation.title}\"")
        if citation.journal:
            output.append(f"   {citation.journal}")
        output.append(f"   Context: {citation.citation_context}")
        output.append("")

    return "\n".join(output)