import json
from typing import Dict, Any
from openai import OpenAI

SYSTEM_PROMPT = """
You are a senior data analyst.
Generate a clear, practical, business-friendly data analysis report based on a dataset profile.
Do not claim to know individual rows unless they are included in the profile.
Be honest about limitations.
"""

def generate_data_report(
    profile_summary: Dict[str, Any],
    analysis_goal: str = "",
    model: str = "gpt-4o-mini",
) -> str:
    client = OpenAI()

    prompt = f"""
Dataset profile summary:
{json.dumps(profile_summary, ensure_ascii=False, indent=2)}

User's optional analysis goal:
{analysis_goal or "No specific goal provided."}

Write a Markdown report with these sections:

# Data Analysis Report

## 1. Executive Summary
## 2. Dataset Overview
## 3. Data Quality Issues
## 4. Key Patterns and Insights
## 5. Possible Outliers or Risks
## 6. Recommended Visualizations
## 7. Recommended Next Steps

Rules:
- Be specific and reference column names when useful.
- Do not overstate conclusions.
- Explain limitations if the dataset profile is not enough.
- Use concise bullet points.
"""

    response = client.chat.completions.create(
        model=model,
        temperature=0.3,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
