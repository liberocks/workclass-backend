from django.http import HttpResponse
from datetime import datetime, date, timedelta, time, timezone
import numpy as np
import json
"""

"""

def jsonify(data):
	"""
	This function takes a valid dictionary and makes it into JSON format
	"""
	def dt_handler(obj):
		if isinstance(obj, (datetime, date, time)):
			return obj.isoformat()

		elif isinstance(obj, np.int64):
			return int(obj)

		elif isinstance(obj, timedelta):
			return obj.total_seconds()

		else:
			return None

	return HttpResponse(json.dumps(data, default=dt_handler))


def get_params(req):
	try:
			return req.GET.dict()
	except:
			return None

def get_data(req):
	try:
		return json.loads(req.body)
	except:
		return None