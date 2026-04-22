import json
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.db.models import Count
from django.db.models.functions import TruncDate
from articles.models import Article, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class HomePageView(TemplateView):
      template_name = "home.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            
            # Gather statistics for dashboard cards
            context['article_count'] = Article.objects.count()
            context['comment_count'] = Comment.objects.count()
            context['user_count'] = User.objects.count()
            
            # Query user registration and article creation trends by day
            user_registrations = User.objects.annotate(day=TruncDate('date_joined')) \
                  .values('day').annotate(count=Count('id')).order_by('day')

            post_creations = Article.objects.annotate(day=TruncDate('date')) \
                  .values('day').annotate(count=Count('id')).order_by('day')

            # Align both datasets on consistent date labels for chart visualization
            all_dates = sorted(list(set(
                  [str(x['day']) for x in user_registrations] + 
                  [str(x['day']) for x in post_creations]
            )))

            # Create lookup dictionaries for efficient data retrieval
            user_counts = {str(x['day']): x['count'] for x in user_registrations}
            post_counts = {str(x['day']): x['count'] for x in post_creations}

            # Prepare chart data with JSON serialization for frontend consumption
            context['chart_labels'] = json.dumps(all_dates)
            context['user_chart_data'] = json.dumps([user_counts.get(date, 0) for date in all_dates])
            context['post_chart_data'] = json.dumps([post_counts.get(date, 0) for date in all_dates])
            
            return context

      def post(self, request, *args, **kwargs):
            """ Handles Likes/Dislikes directly on the home page if articles are listed there """
            article_id = request.POST.get('article_id')
            action = request.POST.get('action')
            
            if not request.user.is_authenticated:
                  return redirect('login')

            if article_id and action:
                  try:
                        article = Article.objects.get(pk=article_id)
                        if action == 'like':
                              if article.likes.filter(id=request.user.id).exists():
                                    article.likes.remove(request.user)
                              else:
                                    article.likes.add(request.user)
                                    article.dislikes.remove(request.user)
                        elif action == 'dislike':
                              if article.dislikes.filter(id=request.user.id).exists():
                                    article.dislikes.remove(request.user)
                              else:
                                    article.dislikes.add(request.user)
                                    article.likes.remove(request.user)
                  except Article.DoesNotExist:
                        pass

            return redirect(request.path_info)