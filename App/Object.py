from PhiDescriptor import *

class Object:

    def __init__(self, image):
        self.image = image
        self.positions = [] # ensemble des positions de l'objet dans l'image
        self.core = [] # Ensemble des points d'intersection de la ligne theta(p)

    """
        Renvoies les objets (leur matrice de positions) de l'image fournies et les ajoutes à la liste
    """
    def _generateObjects(self):
        pass

    def getRelationWith(self, object):
        phi = PhiDescriptor(self, object)
