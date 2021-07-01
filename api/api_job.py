from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .utils import get_data, get_params, jsonify
from database.models import Job


@csrf_exempt
@require_http_methods(["GET"])
def jobs(req):
  """
  Returns all valid jobs

  Can be filtered by these parameters:
    1. pageSize: int (amount of jobs to return)
    2. keyword: string (job titles that match this keyword)
  """
  params = get_params(req)

  keyword = params.get("keyword")
  page_size = params.get("pageSize", 12) # default is 12
  
  jobs = Job.objects

  if keyword:
    jobs.filter(title__icontains=keyword)

  # order by descending date
  jobs = jobs.order_by("-activation_date")
  
  # Trim the amount of jobs to return
  jobs = jobs.values()[:page_size]

  return jsonify({ "success": True, "jobs": list(jobs) })

@csrf_exempt
@require_http_methods(["GET", "POST"])
def job(req):
  """
  API handler for /job
  1. GET method -> Gets a single job
  2. POST method -> Creates a job
  """

  if req.method == "GET":
    """
    Retrieves a singular job given the ID
    """
    job = None
    params = get_params(req)
    job_id = params.get("job_id")

    try:
      job = Job.objects.get(job_id=job_id)
      job = job.values()
    except Exception as ex:
      print(ex)

    return jsonify({ "success": True, "job": job })
  

  elif req.method == "POST":
    """
    Creates a new job given the following data
      1. title
      2. salary_from
      3. salary_to
      4. salary_period
    """
    data = get_data(req)

    title = data.get("title")
    salary_from = data.get("salary_from")
    salary_to = data.get("salary_to")
    salary_period = data.get("salary_period")

    if not title or not salary_from or not  salary_to or not salary_period:
      return HttpResponseBadRequest()

    new_job = Job(\
      title=title, 
      salary_from=salary_from, 
      salary_to=salary_to, 
      salary_period=salary_period, 
      active=True, 
      featured=True
    )

    new_job.save()

    return jsonify({ "success": True, "job": new_job.values() })