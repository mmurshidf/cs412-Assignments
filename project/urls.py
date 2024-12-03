from django.urls import path
from .views import HomePageView, JobDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('job/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
]


