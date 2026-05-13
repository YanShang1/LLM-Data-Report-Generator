import streamlit as st
from dotenv import load_dotenv

from src.config import AppConfig
from src.data_loader import load_dataset
from src.profiler import profile_dataset, build_llm_profile_summary
from src.visualizer import (
    create_numeric_histogram,
    create_correlation_heatmap,
    create_categorical_bar_chart,
)
from src.llm_report import generate_data_report
from src.report_builder import build_markdown_report

load_dotenv()

st.set_page_config(page_title="LLM Data Analysis Report Generator", page_icon="📊", layout="wide")
st.title("📊 LLM Data Analysis Report Generator")
st.caption("Upload a CSV or Excel dataset and generate an AI-powered analysis report.")

config = AppConfig.from_env()

with st.sidebar:
    st.header("Settings")
    st.write(f"Model: `{config.openai_model}`")
    max_rows = st.slider("Rows used for profiling", 500, 20000, 5000, step=500)
    st.divider()
    st.write("The full dataset is loaded, but the profile can be limited to keep the LLM prompt efficient.")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded_file is None:
    st.info("Upload a dataset to start.")
    st.stop()

try:
    df = load_dataset(uploaded_file)
except Exception as exc:
    st.error(f"Could not load dataset: {exc}")
    st.stop()

if df.empty:
    st.error("The uploaded dataset is empty.")
    st.stop()

st.success(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")

st.subheader("Data Preview")
st.dataframe(df.head(20), use_container_width=True)

profile_df = df.head(max_rows).copy()
profile = profile_dataset(profile_df)

st.divider()
st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Rows Profiled", profile_df.shape[0])

st.markdown("### Column Types")
st.dataframe(profile["column_types"], use_container_width=True)

st.markdown("### Missing Values")
st.dataframe(profile["missing_values"], use_container_width=True)

st.markdown("### Descriptive Statistics")
st.dataframe(profile["descriptive_statistics"], use_container_width=True)

if not profile["possible_outliers"].empty:
    st.markdown("### Possible Outliers")
    st.dataframe(profile["possible_outliers"], use_container_width=True)

st.divider()
st.subheader("Automatic Visualizations")

numeric_columns = profile["numeric_columns"]
categorical_columns = profile["categorical_columns"]

if numeric_columns:
    selected_num = st.selectbox("Choose a numeric column for histogram", numeric_columns)
    st.pyplot(create_numeric_histogram(profile_df, selected_num))
else:
    st.info("No numeric columns found for histograms.")

if len(numeric_columns) >= 2:
    st.markdown("### Correlation Heatmap")
    st.pyplot(create_correlation_heatmap(profile_df[numeric_columns]))

if categorical_columns:
    selected_cat = st.selectbox("Choose a categorical column for bar chart", categorical_columns)
    st.pyplot(create_categorical_bar_chart(profile_df, selected_cat))

st.divider()
st.subheader("Generate AI Report")

analysis_goal = st.text_area(
    "Optional: What do you want the report to focus on?",
    placeholder="Example: Focus on customer behavior, revenue trends, missing values, and business recommendations.",
    height=100,
)

if st.button("Generate Report", type="primary"):
    if not config.openai_api_key:
        st.error("Missing OPENAI_API_KEY. Please create a .env file and add your API key.")
        st.stop()

    with st.spinner("Generating AI analysis report..."):
        llm_profile_summary = build_llm_profile_summary(profile)
        ai_report = generate_data_report(
            profile_summary=llm_profile_summary,
            analysis_goal=analysis_goal,
            model=config.openai_model,
        )

    markdown_report = build_markdown_report(profile, ai_report, analysis_goal)
    st.session_state["ai_report"] = ai_report
    st.session_state["markdown_report"] = markdown_report

if "ai_report" in st.session_state:
    st.markdown("## AI-Generated Analysis Report")
    st.markdown(st.session_state["ai_report"])

    st.download_button(
        "Download Markdown Report",
        data=st.session_state["markdown_report"],
        file_name="data_analysis_report.md",
        mime="text/markdown",
    )
