from django.shortcuts import render
from Descriptors.Helper import Helper
from django.core.files.storage import FileSystemStorage

def index(request):
    relation = None
    if request.method == 'POST' and request.FILES['image']:
        upload = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)

        images = Helper.preprocessImages("./media")
        objects = Helper.convertImagesToObjects(images)
        relation = objects[0].getRelationWith(objects[1])
        print(relation)

    context = {
        "relation": relation
    }
    return render(request, "index.html", context)