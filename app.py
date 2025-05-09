import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
from dotenv import load_dotenv
from utils.data_processing import load_data, preprocess_data, filter_data
from utils.visualization import (create_donut_chart, create_line_chart, create_bar_chart,
                                create_histogram, create_scatter_plot, create_wordcloud, create_sunburst_chart)
from utils.nlp_analysis import (analyze_sentiment, extract_themes, get_actionable_insights,
                               search_feedback, answer_custom_question)
from utils.report_generation import generate_pdf_report
from utils.logging_config import setup_logging
import logging
import time

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Streamlit page configuration
st.set_page_config(page_title="Customer Feedback Synthesizer", layout="wide", initial_sidebar_state="expanded")

# Custom inline styles for stunning UI
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom, #0f172a, #1e293b);
        padding: 20px;
        border-radius: 10px;
    }
    .title {
        font-size: 2.5em;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        background: linear-gradient(to right, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .subheader {
        color: #ffffff;
        font-size: 1.5em;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
    }
    .stButton>button {
        background: linear-gradient(to right, #3b82f6, #8b5cf6);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: 600;
        transition: transform 0.2s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    .stTextInput>div>div>input, .stDateInput>div>div>input, .stMultiSelect>div>div {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }
    .stSpinner>div>div {
        border-color: #3b82f6 transparent #3b82f6 transparent;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("<h1 class='title'>Customer Feedback Synthesizer for Retail</h1>", unsafe_allow_html=True)
    
    # Sidebar for file upload and filters
    with st.sidebar:
        st.header("Upload & Filters", anchor=False)
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"], help="Upload a CSV with 'feedback' and 'date' columns.")
        
        if uploaded_file:
            try:
                with st.spinner("Loading data..."):
                    start_time = time.time()
                    df = load_data(uploaded_file)
                    df = preprocess_data(df)
                    logger.info(f"Data loaded and preprocessed in {time.time() - start_time:.2f} seconds")
                    
                    # Date range filter
                    min_date = df['date'].min().date()
                    max_date = df['date'].max().date()
                    date_range = st.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
                    
                    # Sentiment filter (multi-select)
                    sentiments = ['All'] + list(df['sentiment'].unique())
                    selected_sentiments = st.multiselect("Select Sentiments", sentiments, default=['All'])
                    if 'All' in selected_sentiments:
                        selected_sentiments = list(df['sentiment'].unique())
                    
                    # Theme filter (multi-select)
                    themes = ['All'] + list(df['theme'].unique())
                    selected_themes = st.multiselect("Select Themes", themes, default=['All'])
                    if 'All' in selected_themes:
                        selected_themes = list(df['theme'].unique())
                    
                    # Apply filters
                    filtered_df = filter_data(df, date_range, selected_sentiments, selected_themes)
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
                logger.error(f"Error loading data: {str(e)}")
                return
        else:
            st.info("Please upload a CSV file to begin.")
            return

    # Main dashboard
    if uploaded_file:
        with st.container():
            # Search bar
            search_query = st.text_input("Search Feedback", placeholder="Enter keywords to search feedback...")
            if search_query:
                filtered_df = search_feedback(filtered_df, search_query)
            
            # Custom question
            st.markdown("<h2 class='subheader'>Ask a Question</h2>", unsafe_allow_html=True)
            with st.container():
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                custom_question = st.text_input("Ask a Question About the Feedback", placeholder="e.g., What are common service complaints?", key="custom-question")
                if custom_question:
                    with st.spinner("Generating answer..."):
                        answer = answer_custom_question(filtered_df, custom_question, GROQ_API_KEY)
                        if "error" in answer.lower():
                            st.error(answer)
                        else:
                            st.markdown(f"<strong>Answer:</strong> {answer}", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Dashboard layout
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Sentiment Distribution (Donut Chart)
                st.markdown("<h2 class='subheader'>Sentiment Distribution</h2>", unsafe_allow_html=True)
                with st.container():
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    donut_fig = create_donut_chart(filtered_df)
                    st.plotly_chart(donut_fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Sentiment Trend (Line Chart)
                st.markdown("<h2 class='subheader'>Sentiment Trend Over Time</h2>", unsafe_allow_html=True)
                with st.container():
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    line_fig = create_line_chart(filtered_df)
                    st.plotly_chart(line_fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Theme Distribution (Bar Chart)
                st.markdown("<h2 class='subheader'>Theme Distribution</h2>", unsafe_allow_html=True)
                with st.container():
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    bar_fig = create_bar_chart(filtered_df)
                    st.plotly_chart(bar_fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                # Word Clouds
                st.markdown("<h2 class='subheader'>Word Clouds</h2>", unsafe_allow_html=True)
                with st.container():
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    pos_wc, neg_wc = create_wordcloud(filtered_df)
                    st.image(pos_wc, caption="Positive Feedback Word Cloud", use_column_width=True)
                    st.image(neg_wc, caption="Negative Feedback Word Cloud", use_column_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Actionable Insights
                st.markdown("<h2 class='subheader'>Actionable Insights</h2>", unsafe_allow_html=True)
                with st.container():
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    with st.spinner("Generating insights..."):
                        insights = get_actionable_insights(filtered_df, GROQ_API_KEY)
                    st.markdown(insights, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            # Additional Charts
            st.markdown("<h2 class='subheader'>Sentiment per Theme (Histogram)</h2>", unsafe_allow_html=True)
            with st.container():
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                hist_fig = create_histogram(filtered_df)
                st.plotly_chart(hist_fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<h2 class='subheader'>Priority Matrix (Scatter Plot)</h2>", unsafe_allow_html=True)
            with st.container():
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                scatter_fig = create_scatter_plot(filtered_df)
                st.plotly_chart(scatter_fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<h2 class='subheader'>Sentiment by Theme (Sunburst Chart)</h2>", unsafe_allow_html=True)
            with st.container():
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                sunburst_fig = create_sunburst_chart(filtered_df)
                st.plotly_chart(sunburst_fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Representative Feedback Samples
            st.markdown("<h2 class='subheader'>Representative Feedback Samples</h2>", unsafe_allow_html=True)
            with st.container():
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                for sentiment in ['Positive', 'Negative']:
                    samples = filtered_df[filtered_df['sentiment'] == sentiment]['feedback'].head(3).tolist()
                    st.markdown(f"<strong>{sentiment} Feedback</strong>")
                    for sample in samples:
                        st.markdown(f"- {sample}")
                    st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # PDF Report Download
            st.markdown("<h2 class='subheader'>Download Your Report</h2>", unsafe_allow_html=True)
            with st.container():
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                if st.button("Generate and Download Report", key="download-report-button", use_container_width=True):
                    with st.spinner("Generating PDF report..."):
                        try:
                            start_time = time.time()
                            # Debug the themes variable before passing it
                            themes = extract_themes(filtered_df)
                            logger.debug(f"Type of themes before report generation: {type(themes)}, Value: {themes}")
                            pdf_buffer = generate_pdf_report(filtered_df, donut_fig, line_fig, bar_fig, hist_fig, 
                                               scatter_fig, sunburst_fig, pos_wc, neg_wc, themes, insights)
                            logger.info(f"PDF generated in {time.time() - start_time:.2f} seconds")
                            st.download_button(
                                label="Click to Download Report",
                                data=pdf_buffer,
                                file_name="feedback_report.pdf",
                                mime="application/pdf",
                                key="download-report",
                                use_container_width=True
                            )
                            st.success("Report downloaded successfully!")
                        except Exception as e:
                            st.error(f"Failed to generate report: {str(e)}")
                            logger.error(f"Failed to generate report: {str(e)}")
                st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()