from typing import Dict, Any

def build_markdown_report(profile: Dict[str, Any], ai_report: str, analysis_goal: str = "") -> str:
    lines = []
    lines.append(ai_report.strip())
    lines.append("\n---\n")
    lines.append("# Technical Appendix\n")

    lines.append("## Analysis Goal\n")
    lines.append(analysis_goal or "No specific analysis goal provided.")

    lines.append("\n## Dataset Shape\n")
    lines.append(f"- Rows profiled: {profile['row_count']}")
    lines.append(f"- Columns: {profile['column_count']}")

    lines.append("\n## Numeric Columns\n")
    for col in profile["numeric_columns"]:
        lines.append(f"- {col}")

    lines.append("\n## Categorical Columns\n")
    for col in profile["categorical_columns"]:
        lines.append(f"- {col}")

    lines.append("\n## Missing Values\n")
    if profile["missing_values"].empty:
        lines.append("No missing value summary available.")
    else:
        lines.append(profile["missing_values"].to_markdown(index=False))

    lines.append("\n## Descriptive Statistics\n")
    if profile["descriptive_statistics"].empty:
        lines.append("No numeric descriptive statistics available.")
    else:
        lines.append(profile["descriptive_statistics"].to_markdown())

    lines.append("\n## Possible Outliers\n")
    if profile["possible_outliers"].empty:
        lines.append("No possible outliers detected using the IQR rule.")
    else:
        lines.append(profile["possible_outliers"].to_markdown(index=False))

    return "\n".join(lines).strip() + "\n"
