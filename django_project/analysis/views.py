from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from articles.models import Article, Comment

from collections import defaultdict
from django.db.models.functions import TruncDate
from django.db.models import Count

# 🔥 NEW IMPORT
from textblob import TextBlob

User = get_user_model()


# ======================
# 🔥 SENTIMENT FUNCTION
# ======================
def get_sentiment(text):
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

            # 🔹 Get user
            user = get_object_or_404(User, id=self.kwargs.get("user_id"))

            # 🔹 Query data
            articles = Article.objects.filter(author=user)
            comments = Comment.objects.filter(author=user)

            # ======================
            # ✅ ARTICLE SENTIMENT (REAL ANALYSIS)
            # ======================
            article_data = {"positive": 0, "negative": 0, "neutral": 0}

            for a in articles:
                  sentiment = get_sentiment(a.body)   # 🔥 FIXED HERE

                  if sentiment == "Positive":
                        article_data["positive"] += 1
                  elif sentiment == "Negative":
                        article_data["negative"] += 1
                  else:
                        article_data["neutral"] += 1

            # ======================
            # ✅ COMMENT SENTIMENT (REAL ANALYSIS)
            # ======================
            comment_data = {"positive": 0, "negative": 0, "neutral": 0}

            for c in comments:
                  sentiment = get_sentiment(c.comment)  

                  if sentiment == "Positive":
                        comment_data["positive"] += 1
                  elif sentiment == "Negative":
                        comment_data["negative"] += 1
                  else:
                        comment_data["neutral"] += 1

            # ======================
            # 🔥 COMBINED SENTIMENT
            # ======================
            sentiment_data = {
                  "positive": article_data["positive"] + comment_data["positive"],
                  "negative": article_data["negative"] + comment_data["negative"],
                  "neutral": article_data["neutral"] + comment_data["neutral"],
            }

            # ======================
            # 📈 TIME-BASED TREND (USING STORED FIELD)
            # ======================
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

            # ======================
            # 🤖 INSIGHT
            # ======================
            positive = sentiment_data["positive"]
            negative = sentiment_data["negative"]

            if positive > negative:
                  insight = "User mostly writes positive content 😊"
            elif negative > positive:
                  insight = "User tends to write negative content 😐"
            else:
                  insight = "User has balanced sentiment ⚖️"

            # ======================
            # 📦 FINAL CONTEXT
            # ======================
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