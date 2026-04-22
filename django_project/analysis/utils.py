from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
      score = sia.polarity_scores(text)['compoud']
      
      if score >= 0.05:
            return "Positive"
      elif score <= -0.05:
            return "Negative"
      return "Neutral"