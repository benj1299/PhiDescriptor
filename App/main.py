import Helper

images = Helper.preprocessImages("./images")
objects = Helper.convertImagesToObjects(images)

relation = objects[0].getRelationWith(objects[1])

print(relation)