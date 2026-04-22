from django.urls import path
from .views import UserAnalysisView

urlpatterns = [
      path('user/<int:user_id>/', UserAnalysisView.as_view(), name='user_analysis'),
]