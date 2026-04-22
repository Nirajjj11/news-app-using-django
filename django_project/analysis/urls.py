from django.urls import path
from .views import DashboardView

urlpatterns = [
      path('dashboard/<int:user_id>/', DashboardView.as_view(), name='dashboard'),
]
