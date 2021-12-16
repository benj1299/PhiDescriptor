# -*-coding:utf-8 -*
from Helper import Helper

image = Helper.preprocessImage("./images/logo.png")
objects = Helper.convertImageToObjects(image)

relation = objects[0].getRelationWith(objects[1])

print(relation)

# faire des rotations de l'image à div par sin(theta) et commencer par des objets disjoints

# F histogramme est une généralisation de l'histogramme d'angle

# Transformée de radon
