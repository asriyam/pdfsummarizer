import anthropic 
import json
import re

from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
import os
from schema import PaperSummary, get_summary_tool_schema
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
                ],
                tools=[get_summary_tool_schema()],
                tool_choice={"type": "tool", "name": "summarize_paper"}
            )

            # Extract tool use from response
            if response.content[0].type == "tool_use":
                tool_input = response.content[0].input
                paper_summary = PaperSummary(**tool_input)
                print("✅ Paper analysis successful!")
                return paper_summary
            else:
                print("❌ No tool use found in response")
                return None

        except ValidationError as e:
            print(f"❌ Validation error: {e}")
                
        except Exception as e:
            print(f"Unexpected error: {e}")

        return None