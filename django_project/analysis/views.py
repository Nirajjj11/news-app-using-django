# Core Django view and authentication imports
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

# Application models for sentiment analysis data
from articles.models import Article, Comment

# Utility imports for data aggregation and sentiment analysis
from collections import defaultdict  # For efficiently grouping trend data by date
from django.db.models.functions import TruncDate  # Converts DateTimeField to date for grouping
from django.db.models import Count  # Database count aggregation
from textblob import TextBlob  # CRITICAL: Third-party library for sentiment polarity analysis

User = get_user_model()


def get_sentiment(text):
      """Analyze text sentiment and classify as Positive, Negative, or Neutral.
      
      CRITICAL: Uses TextBlob polarity score (-1 to +1):
      - Positive: polarity > 0.1
      - Negative: polarity < -0.1
      - Neutral: -0.1 to 0.1 (no strong sentiment)
      """
      polarity = TextBlob(text).sentiment.polarity

      # IMPORTANT: Thresholds determine sentiment classification accuracy
      if polarity > 0.1:
            return "Positive"
      elif polarity < -0.1:
            return "Negative"
      else:
            return "Neutral"


class DashboardView(TemplateView):
      template_name = "analysis/dashboard.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            # CRITICAL: Fetch user or return 404 - prevents processing non-existent users
            user = get_object_or_404(User, id=self.kwargs.get("user_id"))
            
            # IMPORTANT: Retrieve all user-generated content for analysis
            articles = Article.objects.filter(author=user)
            comments = Comment.objects.filter(author=user)

            # CRITICAL SECTION: Analyze sentiment distribution for all user articles
            # This loops through each article and classifies sentiment
            article_data = {"positive": 0, "negative": 0, "neutral": 0}

            for a in articles:
                  sentiment = get_sentiment(a.body)  # IMPORTANT: Expensive operation per article

                  if sentiment == "Positive":
                        article_data["positive"] += 1
                  elif sentiment == "Negative":
                        article_data["negative"] += 1
                  else:
                        article_data["neutral"] += 1

            # Analyze sentiment distribution for all user comments
            comment_data = {"positive": 0, "negative": 0, "neutral": 0}

            for c in comments:
                  sentiment = get_sentiment(c.comment)  

                  if sentiment == "Positive":
                        comment_data["positive"] += 1
                  elif sentiment == "Negative":
                        comment_data["negative"] += 1
                  else:
                        comment_data["neutral"] += 1

            # Combine article and comment sentiment metrics
            sentiment_data = {
                  "positive": article_data["positive"] + comment_data["positive"],
                  "negative": article_data["negative"] + comment_data["negative"],
                  "neutral": article_data["neutral"] + comment_data["neutral"],
            }

            # CRITICAL SECTION: Retrieve sentiment trends over time
            # NOTE: Uses stored sentiment field from database for performance optimization
            trend_qs = (
                  articles
                  .annotate(day=TruncDate('date'))  # IMPORTANT: Groups by calendar date
                  .values('day', 'sentiment')   # Database-level grouping (fast)
                  .annotate(count=Count('id'))  # Aggregates count per sentiment per day
                  .order_by('day')  # IMPORTANT: Chronological ordering for visualization
            )

            # IMPORTANT: Initialize defaultdict to handle missing dates gracefully
            trend = defaultdict(lambda: {"Positive": 0, "Negative": 0, "Neutral": 0})

            # Map database results to chart-ready format
            for item in trend_qs:
                  trend[str(item['day'])][item['sentiment']] = item['count']

            dates = sorted(trend.keys())

            # CRITICAL SECTION: Generate user insight based on sentiment distribution
            # This determines the displayed message on the dashboard
            positive = sentiment_data["positive"]
            negative = sentiment_data["negative"]

            # IMPORTANT: Decision logic for user content analysis
            if positive > negative:
                  insight = "User mostly writes positive content 😊"
            elif negative > positive:
                  insight = "User tends to write negative content 😐"
            else:
                  insight = "User has balanced sentiment"

            # CRITICAL SECTION: Compile all dashboard data for template rendering
            # IMPORTANT: All values here must match template variable names exactly
            context.update({
                  "profile_user": user,  # User object for profile section
                  "articles": articles,  # User's articles for display

                  # Sentiment breakdown for summary cards
                  "article_data": article_data,
                  "comment_data": comment_data,
                  "sentiment_data": sentiment_data,

                  # Time-series data for trend chart visualization
                  "dates": dates,  # IMPORTANT: X-axis labels for chart
                  "article_positive": [trend[d]["Positive"] for d in dates],
                  "article_negative": [trend[d]["Negative"] for d in dates],
                  "article_neutral": [trend[d]["Neutral"] for d in dates],

                  # User insight message
                  "insight": insight
            })

            return context