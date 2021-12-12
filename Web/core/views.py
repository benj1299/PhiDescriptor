from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    if request.method == 'POST':
        image = request.POST.get("image")
        
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request=request))