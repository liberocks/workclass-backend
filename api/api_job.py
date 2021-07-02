from django.http import HttpResponseBadRequest
from django.db.models import F, Case, When
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .utils import get_data, get_params, jsonify
from database.models import Job
import math


@csrf_exempt
@require_http_methods(["GET"])
def jobs(req):
    """
    Returns all valid jobs

    Can be filtered by these parameters:
      1. pageSize: int (amount of jobs to return)
      2. keyword: string (job titles that match this keyword)
      3. select: string (only return selected attributes)
      4. page: int (page number)
    """
    params = get_params(req)

    keyword = params.get("keyword")
    select = params.get("select")

    page_size = int(params.get("page_size", 12))  # default is 12
    page_size = page_size if page_size > 0 else 12

    page = int(params.get("page", 1))  # default is 1
    page = page if page > 0 else 1

    # pagination offset
    offset = (page-1) * page_size

    # jobs object
    jobs = Job.objects

    # add computed column : salary_median and monthly_salary_median
    jobs = jobs.annotate(salary_median=(F('salary_from')+F('salary_to'))/2)  # nopep8
    jobs = jobs.annotate(monthly_salary_median=(Case(
        When(salary_period='hourly', then=195*(F('salary_from')+F('salary_to'))/2),  # nopep8 # 195 working our per month , by Singapore's law
        When(salary_period='weekly', then=4*(F('salary_from')+F('salary_to'))/2),  # nopep8
        When(salary_period='yearly', then=(1/12)*(F('salary_from')+F('salary_to'))/2),  # nopep8
        When(salary_period='monthly', then=(F('salary_from')+F('salary_to'))/2),  # nopep8
    )))

    # search, sort, and filter feature
    order_by_list = []
    for key, value in params.items():
        if key == "keyword":
            jobs = jobs.filter(title__icontains=keyword)

        if key.startswith("job_") or key.startswith("employ_") or key in ["active", "featured"]:
            if value == "1":
                jobs = jobs.filter(**{key: True})
            elif value == "0":
                jobs = jobs.filter(**{key: False})

        if key in ["salary_period"]:
            jobs = jobs.filter(**{key: value})

        if key == 'rank_by':
            if value == "monthly_salary_median":
                order_by_list.append("monthly_salary_median")
            elif value == "-monthly_salary_median":
                order_by_list.append("-monthly_salary_median")

    # order by descending date
    jobs = jobs.order_by(*order_by_list, "-activation_date")

    # Trim the amount of jobs to return and return only selected columns
    if select:
        job_list = jobs[offset:offset+page_size].values(*select.split(","))
    else:
        job_list = jobs[offset:offset+page_size].values()
    job_list = list(job_list)

    # metadata
    jobs_count = jobs.count()
    total_page = math.ceil(jobs_count/page_size)

    return jsonify({
        "success": True,
        "jobs": job_list,
        "metadata": {
            "total": jobs_count,
            "total_page": total_page,
            "total_item": len(job_list),
            "page": page,
            "page_size": page_size,
        }
    })


@ csrf_exempt
@ require_http_methods(["GET", "POST"])
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

        return jsonify({"success": True, "job": job})

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

        if not title or not salary_from or not salary_to or not salary_period:
            return HttpResponseBadRequest()

        new_job = Job(
            title=title,
            salary_from=salary_from,
            salary_to=salary_to,
            salary_period=salary_period,
            active=True,
            featured=True
        )

        new_job.save()

        return jsonify({"success": True, "job": new_job.values()})
