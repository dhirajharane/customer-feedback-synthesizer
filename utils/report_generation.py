from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, KeepTogether, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
import logging
import io
import plotly.io as pio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import tempfile
from datetime import datetime

logger = logging.getLogger(__name__)

# Define custom colors
header_blue = colors.Color(0/255, 102/255, 204/255)  # RGB(0, 102, 204)
light_gray = colors.Color(240/255, 240/255, 240/255)  # RGB(240, 240, 240)
dark_gray = colors.Color(80/255, 80/255, 80/255)  # RGB(80, 80, 80)
highlight_red = colors.Color(200/255, 0, 0)  # RGB(200, 0, 0)

# Define custom styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleCustom', fontSize=24, leading=28, textColor=header_blue, alignment=1, spaceAfter=12))
styles.add(ParagraphStyle(name='Tagline', fontSize=12, leading=14, textColor=dark_gray, alignment=1, spaceAfter=12))
styles.add(ParagraphStyle(name='SectionHeader', fontSize=18, leading=22, textColor=header_blue, spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle(name='SubHeader', fontSize=14, leading=16, textColor=dark_gray, spaceBefore=8, spaceAfter=4))
styles.add(ParagraphStyle(name='CustomBodyText', fontSize=10, leading=12, textColor=colors.black, spaceAfter=6))
styles.add(ParagraphStyle(name='InsightText', fontSize=10, leading=12, textColor=colors.black, backColor=light_gray, borderPadding=5, borderWidth=1, borderColor=header_blue, spaceAfter=6))
styles.add(ParagraphStyle(name='HighImpactInsight', fontSize=10, leading=12, textColor=colors.black, backColor=light_gray, borderPadding=5, borderWidth=2, borderColor=highlight_red, spaceAfter=6))

def render_chart_to_image(fig, chart_name):
    """Render a Plotly chart to an image using Selenium with a headless browser."""
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            html_path = os.path.join(tmp_dir, f"{chart_name}.html")
            pio.write_html(fig, file=html_path, auto_open=False)

            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=800,400')

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(f"file://{html_path}")
            time.sleep(1)
            img_path = os.path.join(tmp_dir, f"{chart_name}.png")
            driver.save_screenshot(img_path)
            driver.quit()

            with open(img_path, 'rb') as f:
                img_data = f.read()

            return img_data
    except Exception as e:
        logger.error(f"Error rendering chart {chart_name} to image: {str(e)}")
        return None

def create_cover_page():
    """Create a professional cover page for the report."""
    elements = []
    elements.append(Spacer(1, 1 * inch))
    # Placeholder for logo
    elements.append(Paragraph("[Logo Placeholder - Customer Feedback Synthesizer]", styles['Tagline']))
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("Customer Feedback Synthesizer Report", styles['TitleCustom']))
    elements.append(Paragraph("Insights for Retail Excellence", styles['Tagline']))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y')}", styles['Tagline']))
    elements.append(Spacer(1, 1 * inch))
    elements.append(Paragraph("Prepared by:", styles['CustomBodyText']))
    elements.append(Paragraph("Your Name - Lead Analyst", styles['CustomBodyText']))
    elements.append(Paragraph("Team Members: John Doe, Jane Smith", styles['CustomBodyText']))
    elements.append(Paragraph("College: [Your College Name]", styles['CustomBodyText']))
    return elements

def create_table_of_contents():
    """Create a table of contents with page numbers."""
    elements = []
    elements.append(Paragraph("Table of Contents", styles['SectionHeader']))
    toc_data = [
        ["Section", "Page"],
        ["1. Executive Summary", "2"],
        ["2. Sentiment Analysis", "3"],
        ["3. Word Clouds", "4"],
        ["4. Themes and Keywords", "5"],
        ["5. Actionable Insights", "5"],
        ["6. Customer Persona Snapshot", "6"],
        ["7. Before & After Impact", "7"],
        ["8. Representative Feedback Samples", "8"],
        ["9. Conclusion", "9"],
        ["10. Credits", "9"],
    ]
    table = Table(toc_data, colWidths=[4*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), light_gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), dark_gray),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(table)
    return elements

def create_executive_summary():
    """Create an executive summary section."""
    elements = []
    elements.append(Paragraph("📜 Executive Summary", styles['SectionHeader']))
    summary_text = """
    This report provides a comprehensive analysis of customer feedback for retail operations. Key findings include a balanced <b>sentiment distribution</b>, with notable trends in customer satisfaction over time. Themes such as <b>service quality</b>, <b>product issues</b>, and <b>store experience</b> were identified as critical areas. Actionable insights focus on improving customer service training, enhancing packaging standards, and optimizing store layout. The following sections detail these findings with visual data and specific recommendations.
    """
    elements.append(Paragraph(summary_text.strip(), styles['CustomBodyText']))
    return elements

def create_customer_persona_snapshot():
    """Create a customer persona snapshot section."""
    elements = []
    elements.append(Paragraph("👤 Customer Persona Snapshot", styles['SectionHeader']))
    elements.append(Paragraph("Persona 1: Sarah, the Frequent Shopper", styles['SubHeader']))
    persona1_text = """
    <b>Age:</b> 35<br/>
    <b>Occupation:</b> Marketing Manager<br/>
    <b>Feedback:</b> Sarah loves the product variety but often faces delays in shipping, which frustrates her. She values prompt customer service and expects quick resolution to her queries.<br/>
    <b>Needs:</b> Faster shipping, responsive support, and clear communication.
    """
    elements.append(Paragraph(persona1_text.strip(), styles['CustomBodyText']))

    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph("Persona 2: Mike, the First-Time Buyer", styles['SubHeader']))
    persona2_text = """
    <b>Age:</b> 28<br/>
    <b>Occupation:</b> Freelance Designer<br/>
    <b>Feedback:</b> Mike had a poor experience with a damaged product due to inadequate packaging. He felt the customer service was unresponsive when he reached out.<br/>
    <b>Needs:</b> Better packaging quality, proactive customer support, and a hassle-free return process.
    """
    elements.append(Paragraph(persona2_text.strip(), styles['CustomBodyText']))
    return elements

def create_before_after_impact():
    """Create a Before & After impact section."""
    elements = []
    elements.append(Paragraph("🔄 Before & After Impact", styles['SectionHeader']))
    before_text = """
    <b>Current State:</b><br/>
    - Customers face delays in shipping, leading to dissatisfaction.<br/>
    - Poor packaging results in damaged products, increasing returns.<br/>
    - Inconsistent customer service experiences cause frustration.
    """
    elements.append(Paragraph(before_text.strip(), styles['CustomBodyText']))

    elements.append(Spacer(1, 0.1 * inch))
    after_text = """
    <b>Improved State (After Implementing Insights):</b><br/>
    - Streamlined shipping processes reduce delivery times by 30%.<br/>
    - Enhanced packaging reduces product damage by 50%, lowering return rates.<br/>
    - Comprehensive customer service training ensures 90% positive interactions.
    """
    elements.append(Paragraph(after_text.strip(), styles['CustomBodyText']))
    return elements

def create_credits_section():
    """Create a credits section."""
    elements = []
    elements.append(Paragraph("👥 Credits", styles['SectionHeader']))
    credits_text = """
    <b>Your Name</b> - Lead Analyst<br/>
    <b>John Doe</b> - Data Scientist<br/>
    <b>Jane Smith</b> - UX Designer<br/>
    [Team Photo Placeholder]
    """
    elements.append(Paragraph(credits_text.strip(), styles['CustomBodyText']))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(Paragraph("Access the Tool: [Link Placeholder - Customer Feedback Synthesizer Dashboard]", styles['CustomBodyText']))
    return elements

def generate_pdf_report(df, donut_fig, line_fig, bar_fig, hist_fig, scatter_fig, sunburst_fig, pos_wc, neg_wc, themes, insights):
    """Generate a professional, creative, and stunning PDF report."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    buffers = []

    # Cover Page
    story.extend(create_cover_page())
    story.append(PageBreak())

    # Table of Contents
    story.extend(create_table_of_contents())
    story.append(PageBreak())

    # Executive Summary
    story.extend(create_executive_summary())
    story.append(Spacer(1, 0.2 * inch))

    # Sentiment Analysis Section
    story.append(Paragraph("📊 Sentiment Analysis", styles['SectionHeader']))
    for fig, title in [
        (donut_fig, "Sentiment Distribution"),
        (line_fig, "Sentiment Trend"),
        (bar_fig, "Theme Distribution"),
        (hist_fig, "Sentiment per Theme"),
        (scatter_fig, "Priority Matrix"),
        (sunburst_fig, "Sentiment by Theme (Sunburst)")
    ]:
        try:
            chart_name = title.lower().replace(" ", "_")
            img_data = render_chart_to_image(fig, chart_name)
            if img_data:
                img_buffer = BytesIO(img_data)
                img_buffer.seek(0)
                buffers.append(img_buffer)
                story.append(Paragraph(title, styles['SubHeader']))
                story.append(Image(img_buffer, width=6*inch, height=3*inch))
                story.append(Spacer(1, 0.1 * inch))
        except Exception as e:
            logger.error(f"Error including {title}: {str(e)}")
            story.append(Paragraph(f"Error: Unable to include {title} chart in report.", styles['CustomBodyText']))
    story.append(PageBreak())

    # Word Clouds
    story.append(Paragraph("☁️ Word Clouds", styles['SectionHeader']))
    word_cloud_elements = []
    for wc, title, caption in [
        (pos_wc, "Positive Feedback Word Cloud", "Key positive themes highlighted by customers"),
        (neg_wc, "Negative Feedback Word Cloud", "Key negative themes highlighted by customers")
    ]:
        try:
            img_buffer = BytesIO()
            wc.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            buffers.append(img_buffer)
            word_cloud_elements.append([
                Paragraph(title, styles['SubHeader']),
                Image(img_buffer, width=3*inch, height=1.5*inch),
                Paragraph(caption, styles['CustomBodyText'])
            ])
        except Exception as e:
            logger.error(f"Error including word cloud {title}: {str(e)}")
            word_cloud_elements.append([Paragraph(f"Error: Unable to include {title} in report.", styles['CustomBodyText'])])

    # Place word clouds side by side
    table = Table([word_cloud_elements], colWidths=[3.5*inch, 3.5*inch])
    story.append(table)
    story.append(PageBreak())

    # Themes and Keywords
    story.append(Paragraph("🔍 Themes and Keywords", styles['SectionHeader']))
    if isinstance(themes, dict):
        for theme, keywords in themes.items():
            story.append(Paragraph(f"<b>{theme}</b>: {', '.join(keywords)}", styles['CustomBodyText']))
    elif isinstance(themes, list):
        themes_dict = {theme: ["No keywords available"] for theme in themes}
        for theme, keywords in themes_dict.items():
            story.append(Paragraph(f"<b>{theme}</b>: {', '.join(keywords)}", styles['CustomBodyText']))
    else:
        story.append(Paragraph("Error: Themes data is not in the expected format.", styles['CustomBodyText']))
    story.append(Spacer(1, 0.2 * inch))

    # Actionable Insights
    story.append(Paragraph("💡 Actionable Insights", styles['SectionHeader']))
    insights_cleaned = insights.replace('<ul>', '').replace('</ul>', '').replace('<li>', '').replace('</li>', '').replace(' - ', ': ')
    insights_list = [insight.strip() for insight in insights_cleaned.split('\n') if insight.strip()]
    high_impact_indices = [0, 1]  # Assuming first two insights are high-impact
    for i, insight in enumerate(insights_list):
        style = styles['HighImpactInsight'] if i in high_impact_indices else styles['InsightText']
        story.append(KeepTogether([
            Paragraph(insight, style),
            Spacer(1, 0.05 * inch)
        ]))

    # Summary Table of Key Insights
    story.append(Paragraph("Summary of Key Insights", styles['SubHeader']))
    summary_data = [
        ["Problem Area", "Insight", "Suggested Action"],
        ["Shipping Delays", "Customers face delays in shipping", "Streamline shipping processes to reduce delivery times by 30%"],
        ["Packaging Issues", "Poor packaging leads to damaged products", "Implement quality control steps and use better materials"],
        ["Customer Service", "Inconsistent customer service experiences", "Invest in comprehensive customer service training"]
    ]
    table = Table(summary_data, colWidths=[2*inch, 2.5*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), light_gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), dark_gray),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(table)
    story.append(PageBreak())

    # Customer Persona Snapshot
    story.extend(create_customer_persona_snapshot())
    story.append(PageBreak())

    # Before & After Impact
    story.extend(create_before_after_impact())
    story.append(PageBreak())

    # Feedback Samples
    story.append(Paragraph("🗣 Representative Feedback Samples", styles['SectionHeader']))
    for sentiment in ['Positive', 'Negative']:
        story.append(Paragraph(f"{sentiment} Feedback", styles['SubHeader']))
        samples = df[df['sentiment'] == sentiment]['feedback'].head(3).tolist()
        if samples:
            data = [[f"Sample {i+1}", sample] for i, sample in enumerate(samples)]
            table = Table(data, colWidths=[1*inch, 6*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), light_gray),
                ('TEXTCOLOR', (0, 0), (-1, 0), dark_gray),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            story.append(table)
        else:
            story.append(Paragraph(f"No {sentiment.lower()} feedback available.", styles['CustomBodyText']))
        story.append(Spacer(1, 0.1 * inch))

    # Conclusion
    story.append(Paragraph("🏁 Conclusion", styles['SectionHeader']))
    conclusion_text = """
    This report highlights key areas for improvement in retail operations based on customer feedback. By addressing the identified issues through targeted strategies, the business can enhance <b>customer satisfaction</b> and <b>loyalty</b>. For further details or custom analyses, please use the Customer Feedback Synthesizer tool.
    """
    story.append(Paragraph(conclusion_text.strip(), styles['CustomBodyText']))
    story.append(Spacer(1, 0.2 * inch))

    # Credits
    story.extend(create_credits_section())

    try:
        doc.build(story)
        buffer.seek(0)
        pdf_data = buffer.getvalue()
        buffer.close()
        download_buffer = BytesIO(pdf_data)
        for buf in buffers:
            buf.close()
        return download_buffer
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        for buf in buffers:
            buf.close()
        raise Exception(f"Failed to generate PDF report: {str(e)}")