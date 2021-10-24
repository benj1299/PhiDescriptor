import Helper
from PhiDescriptor import *

images = Helper.preprocessImages("./images")
objects = Helper.generateObjects(images)

phi = PhiDescriptor(objects)

relation =  phi.getPhiDescriptor(objects[0], objects[1])

print(relation) 