from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

# first argument is HttpRequest
def index(request):
    return HttpResponse("صفحه اول polls.")