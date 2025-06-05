
# 🛍️ Customer Feedback Synthesizer for Retail 📊

A powerful AI-driven tool to **analyze customer feedback**, generate actionable insights, and create **professional reports** for retail businesses.

---

## 🚀 Overview

The **Customer Feedback Synthesizer for Retail** is a **Streamlit-based web application** that enables retail businesses to:

- Efficiently **analyze customer feedback**.
- Perform **sentiment analysis** & **theme extraction** using NLP.
- Generate **AI-powered recommendations**.
- Create **stunning PDF reports** featuring charts, word clouds, and more.

---

## ✨ Key Features

- 🔍 **Sentiment Analysis**  
  Classifies feedback as Positive, Negative, or Neutral using NLP models.

- 🧠 **Theme Extraction**  
  Detects recurring themes like *Service*, *Product*, *Delivery*, etc.

- 📊 **Interactive Dashboard**  
  Visualize data with:
  - Donut Charts
  - Line & Bar Charts
  - Histograms
  - Scatter Plots
  - Sunburst Diagrams

- ☁️ **Word Clouds**  
  Highlights prominent words from both positive & negative feedback.

- 🤖 **Actionable Insights**  
  Uses **Grok API** to suggest meaningful, data-backed business improvements.

- 📝 **Professional PDF Reports**  
  Automatically generate and download comprehensive reports featuring:
  - Visual analytics
  - Insights
  - Customer personas

---

## 🛠️ Installation

### ✅ Prerequisites
- Python **3.8+**
- Git
- Grok API key (from [xAI](https://x.ai/))

### 📦 Setup Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/dhirajharane/customer-feedback-synthesizer.git
   cd customer-feedback-synthesizer
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv mynewenv
   source mynewenv/bin/activate  # On Windows: mynewenv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**  
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_grok_api_key
   ```

---

## ▶️ Usage

### 🖥️ Run the App
```bash
streamlit run app.py
```

### 🌐 Access the Dashboard
Open your browser and go to:  
👉 `http://localhost:8501`

### 📁 Upload Feedback Data
Upload a `.csv` file with `feedback` and `date` columns:
```csv
feedback,date
"Love the product, fast delivery!",2024-01-15
"Poor packaging, item damaged.",2024-02-10
```

### 🔎 Explore Insights
- Use filters for date range, sentiment, and themes.
- Ask questions about the data.
- Generate and download a full **PDF report**.

---

## 📸 Screenshots

### 🎛️ Dashboard Overview
*Insert screenshot image here*

### 🧾 Generated Report
*Insert report sample preview image here*

---

## 📑 Report Features

The generated PDF report includes:

- 📄 **Cover Page**: Title, team, date  
- 🧭 **Table of Contents**: With page numbers  
- 💬 **Sentiment Visualizations**: Donut, line, sunburst charts  
- ☁️ **Word Clouds**: Positive & negative side-by-side  
- 🧵 **Themes**: Highlighted with keywords  
- 📌 **Insights**: AI-generated action items in callouts  
- 👥 **Customer Personas**: Fictional customer types  
- 🔁 **Before & After**: Business impact visualizations  
- 🗂️ **Feedback Samples**: Tabulated sentiment examples  

---

## 🧑‍💻 Contributing

We welcome contributions! 🙌

1. Fork the repo  
2. Create your feature branch:  
   `git checkout -b feature/your-feature`  
3. Commit your changes:  
   `git commit -m "Add your feature"`  
4. Push to GitHub:  
   `git push origin feature/your-feature`  
5. Open a Pull Request 🚀

---

## 📜 License

This project is licensed under the **MIT License**.  
See the [`LICENSE`](./LICENSE) file for details.

---

## ❤️ Built With

- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [ReportLab](https://www.reportlab.com/)
- [Grok API](https://x.ai/)
