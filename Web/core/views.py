from django.shortcuts import render
from Descriptors.Helper import Helper
from django.core.files.storage import FileSystemStorage
import cv2 as cv
import os

def index(request):
    relation = None
    accuracy = None
    if request.method == 'POST' and request.FILES['image']:
        upload = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)

        image = Helper.preprocessImage(os.getcwd() + file_url)
        objects = Helper.convertImageToObjects(image)
        relation, accuracy = objects[0].getRelationWith(objects[1]) if len(objects) > 1 else "Un seul objet détecté", "100"        

    context = {
        "relation": relation,
        "accuracy": accuracy
    }
    return render(request, "index.html", context)