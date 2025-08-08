from summarizer import Summarizer
from helper import format_summary
from dotenv import load_dotenv

load_dotenv()

summarizer = Summarizer()

pdf_path = "bacteria.pdf"

print("🚀 Starting paper analysis...")
summary = summarizer.summarize(pdf_path)

if summary:
    # Display results
    print(format_summary(summary))
else:
    print("❌ Failed to analyze paper")
