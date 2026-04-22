from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from articles.models import Article
from .services import get_user_sentiment_summary

User = get_user_model()


class UserAnalysisView(TemplateView):
      template_name = "analysis/user_profile.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            user_id = self.kwargs.get("user_id")
            user = get_object_or_404(User, id=user_id)

            articles = Article.objects.filter(author=user).order_by('-date')
            sentiment_data = get_user_sentiment_summary(user)

            # Optional smart insight
            if sentiment_data["negative"] > sentiment_data["positive"]:
                  insight = "User tends to post more negative content"
            elif sentiment_data["positive"] > sentiment_data["negative"]:
                  insight = "User tends to post more positive content"
            else:
                  insight = "User has balanced sentiment"

            context.update({
                  "profile_user": user,
                  "articles": articles,
                  "sentiment_data": sentiment_data,
                  "insight": insight
            })

            return context