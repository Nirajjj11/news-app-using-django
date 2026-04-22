# JSON serialization for chart data
import json
# Generic class-based template view
from django.views.generic import TemplateView
# HTTP redirection utilities
from django.shortcuts import redirect
# Database aggregation functions
from django.db.models import Count
from django.db.models.functions import TruncDate
# Application models for statistics
from articles.models import Article, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class HomePageView(TemplateView):
      template_name = "home.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            
            # CRITICAL SECTION: Gather statistics for dashboard cards
            context['article_count'] = Article.objects.count()
            context['comment_count'] = Comment.objects.count()
            context['user_count'] = User.objects.count()
            
            # CRITICAL SECTION: Query user registration and article creation trends by day
            # IMPORTANT: Database grouping by date for performance
            user_registrations = User.objects.annotate(day=TruncDate('date_joined')) \
                  .values('day').annotate(count=Count('id')).order_by('day')

            post_creations = Article.objects.annotate(day=TruncDate('date')) \
                  .values('day').annotate(count=Count('id')).order_by('day')

            # CRITICAL SECTION: Align both datasets on consistent date labels for chart visualization
            # IMPORTANT: Ensures X-axis alignment between user and article trend lines
            all_dates = sorted(list(set(
                  [str(x['day']) for x in user_registrations] + 
                  [str(x['day']) for x in post_creations]
            )))

            # IMPORTANT: Create lookup dictionaries for efficient O(1) data retrieval per date
            user_counts = {str(x['day']): x['count'] for x in user_registrations}
            post_counts = {str(x['day']): x['count'] for x in post_creations}

            # CRITICAL SECTION: Prepare chart data with JSON serialization for frontend consumption
            # IMPORTANT: JSON format required for Chart.js compatibility
            context['chart_labels'] = json.dumps(all_dates)
            context['user_chart_data'] = json.dumps([user_counts.get(date, 0) for date in all_dates])
            context['post_chart_data'] = json.dumps([post_counts.get(date, 0) for date in all_dates])
            
            return context

      def post(self, request, *args, **kwargs):
            """ Handles Likes/Dislikes directly on the home page if articles are listed there """
            # CRITICAL: Extract form parameters for action processing
            article_id = request.POST.get('article_id')
            action = request.POST.get('action')
            
            # IMPORTANT: Authorization check - only authenticated users can like/dislike
            if not request.user.is_authenticated:
                  return redirect('login')

            # CRITICAL SECTION: Process like/dislike toggle logic
            if article_id and action:
                  try:
                        article = Article.objects.get(pk=article_id)
                        
                        # IMPORTANT: Mutual exclusivity - user cannot like and dislike simultaneously
                        if action == 'like':
                              if article.likes.filter(id=request.user.id).exists():
                                    # Toggle off: remove existing like
                                    article.likes.remove(request.user)
                              else:
                                    # Toggle on: add like and remove dislike if exists
                                    article.likes.add(request.user)
                                    article.dislikes.remove(request.user)
                        elif action == 'dislike':
                              if article.dislikes.filter(id=request.user.id).exists():
                                    # Toggle off: remove existing dislike
                                    article.dislikes.remove(request.user)
                              else:
                                    # Toggle on: add dislike and remove like if exists
                                    article.dislikes.add(request.user)
                                    article.likes.remove(request.user)
                  except Article.DoesNotExist:
                        # IMPORTANT: Silently fail if article deleted between page load and submission
                        pass

            # CRITICAL: Redirect back to referring page to refresh vote counts
            return redirect(request.path_info)