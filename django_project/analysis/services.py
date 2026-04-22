from articles.models import Article, Comment

def get_user_sentiment_summary(user):
      articles = Article.objects.filter(author=user)
      comments = Comment.objects.filter(author=user)

      data = {
            "positive": 0,
            "negative": 0,
            "neutral": 0
      }

      for item in list(articles) + list(comments):
            if item.sentiment == "Positive":
                  data["positive"] += 1
            elif item.sentiment == "Negative":
                  data["negative"] += 1
            else:
                  data["neutral"] += 1

      return data