from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

def hello_world(request):
  return HttpResponse("hello world!!!")

class IndexView(TemplateView):
  template_name = "index.html"
