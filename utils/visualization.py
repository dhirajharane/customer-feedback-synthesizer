import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import io
from PIL import Image

def create_donut_chart(df):
    """Create a donut chart for sentiment distribution."""
    sentiment_counts = df['sentiment'].value_counts()
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        hole=0.4,
        color_discrete_sequence=['#3b82f6', '#ef4444', '#facc15']
    )
    fig.update_layout(
        showlegend=True,
        margin=dict(t=0, b=0, l=0, r=0),
        font=dict(color="#ffffff", size=14),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    fig.update_traces(textinfo='percent+label', textfont_size=16)
    return fig

def create_line_chart(df):
    """Create a line chart for sentiment trend over time."""
    sentiment_trend = df.groupby([df['date'].dt.date, 'sentiment']).size().unstack(fill_value=0)
    fig = go.Figure()
    colors = {'Positive': '#3b82f6', 'Negative': '#ef4444', 'Neutral': '#facc15'}
    for sentiment in sentiment_trend.columns:
        fig.add_trace(go.Scatter(
            x=sentiment_trend.index,
            y=sentiment_trend[sentiment],
            name=sentiment,
            line=dict(width=3, color=colors[sentiment]),
            mode='lines+markers'
        ))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Count",
        showlegend=True,
        font=dict(color="#ffffff", size=14),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickangle=45),
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)")
    )
    return fig

def create_bar_chart(df):
    """Create a bar chart for theme distribution."""
    theme_counts = df['theme'].value_counts()
    fig = px.bar(
        x=theme_counts.index,
        y=theme_counts.values,
        color=theme_counts.index,
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig.update_layout(
        xaxis_title="Theme",
        yaxis_title="Count",
        showlegend=False,
        font=dict(color="#ffffff", size=14),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickangle=45)
    )
    fig.update_traces(marker_line_color='white', marker_line_width=1.5)
    return fig

def create_histogram(df):
    """Create a histogram for sentiment per theme."""
    fig = px.histogram(
        df,
        x='theme',
        color='sentiment',
        barmode='group',
        color_discrete_sequence=['#3b82f6', '#ef4444', '#facc15']
    )
    fig.update_layout(
        xaxis_title="Theme",
        yaxis_title="Count",
        showlegend=True,
        font=dict(color="#ffffff", size=14),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickangle=45)
    )
    return fig

def create_scatter_plot(df):
    """Create a scatter plot for priority matrix (impact vs frequency)."""
    theme_counts = df['theme'].value_counts().reset_index()
    theme_counts.columns = ['theme', 'frequency']
    theme_counts['impact'] = theme_counts['theme'].apply(
        lambda x: df[df['theme'] == x]['sentiment'].map({'Positive': 1, 'Neutral': 0, 'Negative': -1}).mean()
    )
    fig = px.scatter(
        theme_counts,
        x='frequency',
        y='impact',
        text='theme',
        size='frequency',
        color='impact',
        color_continuous_scale='Plasma',
        size_max=40
    )
    fig.update_traces(textposition='top center', textfont=dict(color='#ffffff', size=14))
    fig.update_layout(
        xaxis_title="Frequency",
        yaxis_title="Impact",
        showlegend=False,
        font=dict(color="#ffffff", size=14),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def create_sunburst_chart(df):
    """Create a sunburst chart for sentiment by theme."""
    sunburst_data = df.groupby(['theme', 'sentiment']).size().reset_index(name='count')
    fig = px.sunburst(
        sunburst_data,
        path=['theme', 'sentiment'],
        values='count',
        color='sentiment',
        color_discrete_sequence=['#3b82f6', '#ef4444', '#facc15']
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        font=dict(color="#ffffff", size=14),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def create_wordcloud(df):
    """Create word clouds for positive and negative feedback."""
    pos_text = ' '.join(df[df['sentiment'] == 'Positive']['feedback'])
    neg_text = ' '.join(df[df['sentiment'] == 'Negative']['feedback'])
    
    pos_wc = WordCloud(
        width=400,
        height=200,
        background_color='rgba(0,0,0,0)',
        colormap='Blues',
        font_path=None,
        min_font_size=10,
        max_font_size=50
    ).generate(pos_text if pos_text else 'No positive feedback')
    
    neg_wc = WordCloud(
        width=400,
        height=200,
        background_color='rgba(0,0,0,0)',
        colormap='Reds',
        font_path=None,
        min_font_size=10,
        max_font_size=50
    ).generate(neg_text if neg_text else 'No negative feedback')
    
    # Convert WordCloud to NumPy array and then to PIL Image
    pos_array = pos_wc.to_array()
    neg_array = neg_wc.to_array()
    
    pos_img = Image.fromarray(pos_array)
    neg_img = Image.fromarray(neg_array)
    
    return pos_img, neg_img