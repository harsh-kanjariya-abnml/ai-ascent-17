from django.urls import path

from . import views

urlpatterns = [
    path("api/health-check/", views.health_check),
    path("api/process/", views.process_resume_endpoint, name="process_resume"),
    path("api/get-candidates/", views.get_candidates, name="get_candidates"),
]
