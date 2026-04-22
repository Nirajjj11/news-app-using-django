from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from articles.models import Article, Comment

from collections import defaultdict
from django.db.models.functions import TruncDate
from django.db.models import Count

User = get_user_model()


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
            # ✅ ARTICLE SENTIMENT
            # ======================
            article_data = {"positive": 0, "negative": 0, "neutral": 0}

            for a in articles:
                  if a.sentiment == "Positive":
                        article_data["positive"] += 1
                  elif a.sentiment == "Negative":
                        article_data["negative"] += 1
                  else:
                        article_data["neutral"] += 1

            # ======================
            # ✅ COMMENT SENTIMENT
            # ======================
            comment_data = {"positive": 0, "negative": 0, "neutral": 0}

            for c in comments:
                  if c.sentiment == "Positive":
                        comment_data["positive"] += 1
                  elif c.sentiment == "Negative":
                        comment_data["negative"] += 1
                  else:
                        comment_data["neutral"] += 1

            # ======================
            # 📈 TIME-BASED TREND
            # ======================
            trend_qs = (
                  articles
                  .annotate(day=TruncDate('date'))   # ✅ FIXED
                  .values('day', 'sentiment')
                  .annotate(count=Count('id'))
                  .order_by('day')
            )

            trend = defaultdict(lambda: {"Positive": 0, "Negative": 0, "Neutral": 0})

            for item in trend_qs:
                  trend[str(item['day'])][item['sentiment']] = item['count']

            dates = sorted(trend.keys())

            # ======================
            # 🤖 INSIGHT (MERGED HERE)
            # ======================
            positive = articles.filter(sentiment="Positive").count()
            negative = articles.filter(sentiment="Negative").count()

            if positive > negative:
                  insight = "User mostly writes positive content 😊"
            elif negative > positive:
                  insight = "User tends to write negative content 😐"
            else:
                  insight = "User has balanced sentiment ⚖️"

            # ======================
            # 📦 CONTEXT
            # ======================
            context.update({
                  "profile_user": user,

                  # Sentiment
                  "article_data": article_data,
                  "comment_data": comment_data,

                  # Trend
                  "dates": dates,
                  "article_positive": [trend[d]["Positive"] for d in dates],
                  "article_negative": [trend[d]["Negative"] for d in dates],
                  "article_neutral": [trend[d]["Neutral"] for d in dates],

                  # Insight
                  "insight": insight
            })

            return context