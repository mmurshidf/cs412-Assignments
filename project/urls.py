from django.urls import path
from .views import HomePageView, JobDetailView, CreateAccountView, UserProfileView, UpdateProfileView, ApplyToJobView, CreateJobView, JobApplicationsForJobView, ScheduleInterviewView, WithdrawApplicationView, CompanyListView, CreateCompanyView, OfferOrRejectApplicationView
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
    path('create_job/', CreateJobView.as_view(), name='create_job'),
    path('job/<int:pk>/applications/', JobApplicationsForJobView.as_view(), name='job_applications_for_job'),
    path('job_application/<int:job_application_id>/schedule_interview/', ScheduleInterviewView.as_view(), name='schedule_interview'),
    path('job_application/<int:pk>/withdraw/', WithdrawApplicationView.as_view(), name='withdraw_application'),
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('companies/create/', CreateCompanyView.as_view(), name='create_company'),
    path('job_application/<int:application_id>/<str:action>/offer_or_reject/', OfferOrRejectApplicationView.as_view(), name='offer_or_reject_application'),
]