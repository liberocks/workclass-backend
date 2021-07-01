from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import api_job

urlpatterns = [
    path("jobs", api_job.jobs, name="jobs"),
    path("job", api_job.job, name="job"),
]