import anthropic 
import json
import re

from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
import os
from schema import PaperSummary
import helper

class Summarizer: 
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model =  "claude-3-haiku-20240307"
        self.max_tokens_per_request = 150000
    
    def summarize(self, pdf_path:str) -> Optional[PaperSummary]:
        paper_text = helper.extract_pdf(pdf_path)
        if not paper_text:
            print("Could not extract text from PDF")
            return None
        
        return self.analyze(paper_text)
    
    def analyze(self, text:str) -> Optional[PaperSummary]:
        try:
            response = self.client.messages.create(
                model = self.model,
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": helper.create_summary_prompt(text)
                    }
                ]
            )

            raw_response = response.content[0].text.strip()
            json_text = helper._extract_json(raw_response)

            summary_dict = json.loads(json_text)
            paper_summary = PaperSummary(**summary_dict)

            print("✅ Paper analysis successful!")
            return paper_summary

        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            # Save the problematic JSON for debugging
            with open("debug_json.txt", "w", encoding="utf-8") as f:
                f.write(json_text)
            print("❌ Saved problematic JSON to debug_json.txt for inspection")
                
        except Exception as e:
            print(f"Unexpected error: {e}")

        return None