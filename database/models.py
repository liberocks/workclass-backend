from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone


class Job(models.Model):
  class SalaryPeriodChoice(models.TextChoices):
      monthly = "monthly"
      hourly = "hourly"
      weekly = "weekly"
      yearly = "yearly"

  job_id = models.AutoField(primary_key=True, unique=True)

  # Job Details
  title = models.CharField(max_length=400)
  description = models.TextField()
  activation_date = models.DateTimeField(default=timezone.now)
  active = models.BooleanField()
  featured = models.BooleanField()
  salary_from = models.FloatField()
  salary_period = models.CharField(max_length=7, choices=SalaryPeriodChoice.choices)
  salary_to = models.FloatField()

  # Company Details
  company_name = models.CharField(max_length=400)
  logo_url = models.CharField(max_length=500)

  # Job Categories
  job_admin = models.BooleanField(default=False)
  job_customerservice = models.BooleanField(default=False)
  job_distributionshipping = models.BooleanField(default=False)
  job_grocery = models.BooleanField(default=False)
  job_hospitalityhotel = models.BooleanField(default=False)
  job_covid19 = models.BooleanField(default=False)
  job_marketingsales = models.BooleanField(default=False)
  job_other = models.BooleanField(default=False)
  job_production = models.BooleanField(default=False)
  job_restaurantfoodservice = models.BooleanField(default=False)
  job_retail = models.BooleanField(default=False)
  job_supplychain = models.BooleanField(default=False)
  job_transportation = models.BooleanField(default=False)
  job_warehouse = models.BooleanField(default=False)

  # Employment Type
  employ_fulltime = models.BooleanField(default=False)
  employ_contract = models.BooleanField(default=False)
  employ_parttime = models.BooleanField(default=False)
  employ_adhoc = models.BooleanField(default=False)
  employ_internship = models.BooleanField(default=False)

  def values(self):
    return model_to_dict(self)