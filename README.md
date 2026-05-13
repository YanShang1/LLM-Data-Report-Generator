# LLM Data Analysis Report Generator

An AI-powered data analysis assistant that automatically analyzes uploaded CSV or Excel datasets and generates a natural-language analysis report.

## Features

- Upload CSV or Excel files
- Preview the dataset
- Detect column types
- Analyze missing values
- Generate descriptive statistics
- Detect possible outliers
- Generate correlation analysis
- Create automatic charts
- Use an LLM to generate a readable analysis report
- Export the report as Markdown

## Tech Stack

- Python
- Streamlit
- Pandas
- Matplotlib
- OpenAI API
- python-dotenv
- openpyxl

## Project Structure

```text
llm-data-report-generator/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── src/
│   ├── config.py
│   ├── data_loader.py
│   ├── profiler.py
│   ├── visualizer.py
│   ├── llm_report.py
│   └── report_builder.py
├── data/
└── assets/
```

## Installation

```bash
git clone https://github.com/your-username/llm-data-report-generator.git
cd llm-data-report-generator
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

On Windows, activate the environment with:

```bash
venv\Scripts\activate
```

## Environment Variables

Add your OpenAI API key to `.env`:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

## Resume Description

**LLM Data Analysis Report Generator | Python, Streamlit, Pandas, Matplotlib, OpenAI API**

- Built an AI-powered data analysis assistant that automatically analyzes uploaded CSV and Excel datasets and generates natural-language reports.
- Implemented dataset profiling, missing value detection, descriptive statistics, correlation analysis, and possible outlier detection.
- Created automatic visualizations using Matplotlib and integrated LLM-generated explanations for business-friendly reporting.
- Developed a Streamlit interface for file upload, data preview, chart generation, and downloadable Markdown reports.
