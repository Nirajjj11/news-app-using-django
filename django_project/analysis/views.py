from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from articles.models import Article, Comment

from collections import defaultdict
from django.db.models.functions import TruncDate
from django.db.models import Count
from textblob import TextBlob

User = get_user_model()


def get_sentiment(text):
      """Analyze text sentiment and classify as Positive, Negative, or Neutral."""
      polarity = TextBlob(text).sentiment.polarity

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

            user = get_object_or_404(User, id=self.kwargs.get("user_id"))
            articles = Article.objects.filter(author=user)
            comments = Comment.objects.filter(author=user)

            # Analyze sentiment distribution for all user articles
            article_data = {"positive": 0, "negative": 0, "neutral": 0}

            for a in articles:
                  sentiment = get_sentiment(a.body)

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

            # Retrieve sentiment trends over time using stored sentiment field
            trend_qs = (
                  articles
                  .annotate(day=TruncDate('date'))
                  .values('day', 'sentiment')   # uses DB field (fast)
                  .annotate(count=Count('id'))
                  .order_by('day')
            )

            trend = defaultdict(lambda: {"Positive": 0, "Negative": 0, "Neutral": 0})

            for item in trend_qs:
                  trend[str(item['day'])][item['sentiment']] = item['count']

            dates = sorted(trend.keys())

            # Generate sentiment insight based on data distribution
            positive = sentiment_data["positive"]
            negative = sentiment_data["negative"]

            if positive > negative:
                  insight = "User mostly writes positive content 😊"
            elif negative > positive:
                  insight = "User tends to write negative content 😐"
            else:
                  insight = "User has balanced sentiment"

            # Compile all dashboard data for template rendering
            context.update({
                  "profile_user": user,
                  "articles": articles,

                  "article_data": article_data,
                  "comment_data": comment_data,
                  "sentiment_data": sentiment_data,

                  "dates": dates,
                  "article_positive": [trend[d]["Positive"] for d in dates],
                  "article_negative": [trend[d]["Negative"] for d in dates],
                  "article_neutral": [trend[d]["Neutral"] for d in dates],

                  "insight": insight
            })

            return context