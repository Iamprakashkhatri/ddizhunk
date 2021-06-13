from django.shortcuts import render
from course.models import Course

def esewarequest(request,id):
	if request.method=='GET':
		# http://127.0.0.1:8000/api/client/esewa-request/?oid=1&amt=300.0&refId=0001WDA
		course = Course.objects.get(id=id)
		context = {
		'course':course
		}

		return render(request,'esewa_request.html',context)
		
def khaltirequest(request,id):
	if request.method=='GET':
		# http://127.0.0.1:8000/api/client/esewa-request/?oid=1&amt=300.0&refId=0001WDA
		course = Course.objects.get(id=id)
		context = {
		'course':course
		}

		return render(request,'khalti_request.html',context)
