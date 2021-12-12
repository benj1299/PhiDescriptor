from django.shortcuts import render
from Descriptors.Helper import Helper
import os

def index(request):
    relation = None
    if request.method == 'POST':
        images = Helper.preprocessImages("./Descriptors/images")
        objects = Helper.convertImagesToObjects(images)
        relation = objects[0].getRelationWith(objects[1])
        print(relation)
        #image = request.POST.get("image")
    
    context = {
        "relation": relation
    }
    return render(request, "index.html", context)