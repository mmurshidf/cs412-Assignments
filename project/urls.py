from django.urls import path
from .views import HomePageView, JobDetailView, CreateAccountView, UserProfileView, UpdateProfileView, ApplyToJobView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
    path('job/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
    path('create_account/', CreateAccountView.as_view(), name='create_account'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('job/<int:job_id>/apply/', ApplyToJobView.as_view(), name='apply_to_job'),
]
