from .PhiDescriptor import *
import uuid

class Object:

    def __init__(self, image, component):
        self.image = image
        self.component = component
        self.id = uuid.uuid4()
        self.points = [] # Liste les points d'intersection

    def getRelationWith(self, object):
        phi = PhiDescriptor(self, object)
        return phi.getPhiDescriptor()