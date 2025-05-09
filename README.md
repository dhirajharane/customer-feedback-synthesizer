Customer Feedback Synthesizer for Retail 📊

A powerful tool to analyze customer feedback, generate insights, and create stunning reports for retail businesses.

🚀 Overview
The Customer Feedback Synthesizer for Retail is a Streamlit-based application designed to help retail businesses analyze customer feedback efficiently. It processes feedback data, performs sentiment analysis, extracts themes, generates actionable insights, and produces professional PDF reports with visualizations like charts and word clouds.
Key Features

Sentiment Analysis: Analyze feedback to determine positive, negative, or neutral sentiments.
Theme Extraction: Identify recurring themes (e.g., service, product, store) using NLP.
Interactive Dashboard: Visualize data through donut charts, line charts, bar charts, histograms, scatter plots, and sunburst charts.
Word Clouds: Highlight key themes with positive and negative feedback word clouds.
Actionable Insights: Generate recommendations using the Grok API.
Professional Reports: Create stunning PDF reports with charts, insights, and customer personas.


🛠️ Installation
Follow these steps to set up the project locally:
Prerequisites

Python 3.8+
Git
A Grok API key (from xAI)

Steps

Clone the Repository:
git clone https://github.com/your-username/customer-feedback-synthesizer.git
cd customer-feedback-synthesizer


Create a Virtual Environment:
python -m venv mynewenv
source mynewenv/bin/activate  # On Windows: mynewenv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Set Up Environment Variables:Create a .env file in the project root and add your Grok API key:
GROQ_API_KEY=your_grok_api_key




📖 Usage

Run the Application:
streamlit run app.py


Access the Dashboard:Open your browser and go to http://localhost:8501.

Upload Feedback Data:

Upload a CSV file with feedback and date columns.
Use filters to select date ranges, sentiments, and themes.


Explore Insights:

View sentiment trends, theme distributions, and word clouds.
Ask custom questions about the feedback data.
Generate and download a professional PDF report.



Sample Data Format
Your CSV file should look like this:
feedback,date
"Love the product, fast delivery!",2024-01-15
"Poor packaging, item damaged.",2024-02-10


📸 Screenshots
Dashboard Overview

Generated Report


📑 Report Features
The generated PDF report is professional and visually stunning, including:

Cover Page: Project title, team details, and date.
Table of Contents: Easy navigation with page numbers.
Sentiment Analysis: Visualizations like donut charts, line charts, and sunburst charts.
Word Clouds: Side-by-side comparison of positive and negative feedback.
Themes and Keywords: Extracted themes with associated keywords.
Actionable Insights: Highlighted recommendations in callout boxes.
Customer Personas: Fictional personas representing typical customers.
Before & After Impact: Visualizing the impact of implementing insights.
Feedback Samples: Tabulated positive and negative feedback.


🧑‍💻 Contributing
We welcome contributions! Here's how to get started:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes and commit (git commit -m "Add your feature").
Push to your branch (git push origin feature/your-feature).
Open a Pull Request.


📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

👥 Team

Your Name - Lead Analyst
John Doe - Data Scientist
Jane Smith - UX Designer

For questions or support, contact us at your-email@example.com.

Built with ❤️ using Streamlit, Plotly, and ReportLab.
