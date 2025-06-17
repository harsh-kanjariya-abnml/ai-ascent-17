from django.urls import path

from . import views

urlpatterns = [
    path("api/health-check/", views.health_check),
]
