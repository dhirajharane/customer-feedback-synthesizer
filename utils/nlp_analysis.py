from groq import Groq
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import logging
import os
import httpx

# Download NLTK data with error handling
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    logging.error(f"Error downloading NLTK data: {str(e)}")

stop_words = set(stopwords.words('english'))

logger = logging.getLogger(__name__)

def analyze_sentiment(text):
    """Analyze sentiment of feedback text (simplified)."""
    text = text.lower()
    if any(word in text for word in ['great', 'amazing', 'satisfied', 'love', 'friendly']):
        return 'Positive'
    elif any(word in text for word in ['poor', 'bad', 'defective', 'unresponsive', 'messy']):
        return 'Negative'
    return 'Neutral'

def extract_themes(df):
    """Extract themes and keywords using TF-IDF."""
    vectorizer = TfidfVectorizer(stop_words=list(stop_words), max_features=100)
    tfidf_matrix = vectorizer.fit_transform(df['feedback'])
    feature_names = vectorizer.get_feature_names_out()
    
    themes = {
        'Service': ['service', 'staff', 'support', 'customer', 'friendly', 'unresponsive'],
        'Product': ['product', 'item', 'quality', 'defective', 'collection'],
        'Store': ['store', 'checkout', 'wait', 'messy', 'find'],
        'Delivery': ['delivery', 'fast', 'shipping', 'discounts']
    }
    
    return themes

def get_actionable_insights(df, api_key):
    """Generate actionable insights using Groq LLM with optimized prompt."""
    try:
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set. Please configure it in the .env file.")
        
        # Explicitly disable proxy settings in the environment
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        
        # Log the environment to debug
        logger.debug("Environment variables before Groq client init: HTTP_PROXY=%s, HTTPS_PROXY=%s", 
                     os.environ.get("HTTP_PROXY", "Not set"), os.environ.get("HTTPS_PROXY", "Not set"))
        logger.debug("Groq API key: %s", api_key[:5] + "..." if api_key else "Not set")

        # Create an httpx client with proxies explicitly disabled
        http_client = httpx.Client(proxies=None)
        
        # Initialize Groq client with the custom httpx client
        client = Groq(api_key=api_key, http_client=http_client)
        feedback_data = df['feedback'].head(20).to_list()
        prompt = f"""You are a retail business consultant specializing in customer feedback analysis. Analyze the following feedback data:\n{feedback_data}\nProvide 3 highly specific, actionable, and practical insights to improve customer experience in a retail setting. Focus on strategies like staff training, inventory management, store layout optimization, or customer service improvements. Format your response as a concise bulleted list."""
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Updated to a supported model
            messages=[
                {"role": "system", "content": "You are a retail business consultant providing actionable insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5
        )
        insights = response.choices[0].message.content
        # Format insights as HTML bullet points
        insights = insights.strip()
        if not insights.startswith('-'):
            insights = '- ' + insights.replace('\n', '\n- ')
        return f"<ul>{insights.replace('-', '<li>').replace('\n', '')}</ul>"
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        return "<ul><li>Unable to generate insights due to an error: Ensure GROQ_API_KEY is correctly set and the Groq API is accessible.</li></ul>"

def search_feedback(df, query):
    """Search feedback for a query."""
    return df[df['feedback'].str.contains(query, case=False, na=False)]

def answer_custom_question(df, question, api_key):
    """Answer a custom question using Groq LLM with optimized prompt."""
    try:
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set. Please configure it in the .env file.")
        
        # Explicitly disable proxy settings in the environment
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        
        # Log the environment to debug
        logger.debug("Environment variables before Groq client init: HTTP_PROXY=%s, HTTPS_PROXY=%s", 
                     os.environ.get("HTTP_PROXY", "Not set"), os.environ.get("HTTPS_PROXY", "Not set"))
        logger.debug("Groq API key: %s", api_key[:5] + "..." if api_key else "Not set")

        # Create an httpx client with proxies explicitly disabled
        http_client = httpx.Client(proxies=None)
        
        # Initialize Groq client with the custom httpx client
        client = Groq(api_key=api_key, http_client=http_client)
        feedback_data = df['feedback'].head(20).to_list()
        prompt = f"""You are a retail customer feedback analysis expert. Based on the following feedback data:\n{feedback_data}\nAnswer the following question in a concise, accurate, and professional manner, focusing on the specific details requested:\n{question}"""
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Updated to a supported model
            messages=[
                {"role": "system", "content": "You are a retail feedback analyst providing precise and relevant answers."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.5
        )
        answer = response.choices[0].message.content
        return answer if answer else "No relevant answer could be generated."
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        return f"Unable to answer the question due to an error: Ensure GROQ_API_KEY is correctly set and the Groq API is accessible."