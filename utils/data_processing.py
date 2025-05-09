import pandas as pd
import logging

logger = logging.getLogger(__name__)

def load_data(uploaded_file):
    """Load and validate CSV file."""
    try:
        df = pd.read_csv(uploaded_file)
        if 'feedback' not in df.columns or 'date' not in df.columns:
            raise ValueError("CSV must contain 'feedback' and 'date' columns")
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

def preprocess_data(df):
    """Preprocess data: add sentiment and theme columns."""
    from utils.nlp_analysis import analyze_sentiment, extract_themes
    df['sentiment'] = df['feedback'].apply(analyze_sentiment)
    themes = extract_themes(df)
    df['theme'] = df['feedback'].apply(lambda x: next((k for k, v in themes.items() if any(kw in x.lower() for kw in v)), 'General'))
    return df

def filter_data(df, date_range, sentiments, themes):
    """Apply filters to the dataframe."""
    filtered_df = df.copy()
    if len(date_range) == 2:
        filtered_df = filtered_df[(filtered_df['date'].dt.date >= date_range[0]) & 
                                (filtered_df['date'].dt.date <= date_range[1])]
    if sentiments:
        filtered_df = filtered_df[filtered_df['sentiment'].isin(sentiments)]
    if themes:
        filtered_df = filtered_df[filtered_df['theme'].isin(themes)]
    return filtered_df