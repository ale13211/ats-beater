from django.urls import path
from analyzer.views import AnalyzeView, HealthView

urlpatterns = [
    path("api/health/", HealthView.as_view()),
    path("api/analyze/", AnalyzeView.as_view()),
]
