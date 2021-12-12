from PhiDescriptor import *

class Object:

    def __init__(self, image):
        self.image = image
        self.positions = [] # ensemble des positions de l'objet dans l'image
        self.core = [] # Ensemble des points d'intersection de la ligne theta(p)

    def getRelationWith(self, object):
        phi = PhiDescriptor(self, object)
        return phi.getPhiDescriptor()
