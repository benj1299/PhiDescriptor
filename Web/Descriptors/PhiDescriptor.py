# -*-coding:utf-8 -*
"""
Répresentation du phi-descripteur dont les propriétés attendues sont

P1 - The  descriptor  can  handle  raster  objects, whatever  their  topology and  whether they  are  disjoint  or  not.  
P2 - The descriptor can handle these objects efficiently. 
P3 - The descriptor can handle vector objects. 
P4 - The descriptor can handle distance relationships, i.e., meaningful distance relationship information can be extracted in no time from the descriptor. 
P5 - The descriptor  can  handle  set  relationships;  at  the  very least, it can be used to determine whether two objects intersect, and whether one object includes the other. 
P6 - The descriptor can handle topological, non-set relationships;  at  the  very  least,  it  can  be  used  to determine  whether  the  boundaries  of  two  objects intersect, and whether the interiors intersect. 
P7 - The descriptor can handle directional relationships; at the very least, it can be used to assess relationships like to the right of, to the left of, above and below. 
P8 - The  descriptor  can  handle  the  relationship surround. 
P9 - Relative positions can be somehow compared, and similar positions detected, regardless of which relationships hold. 
P10 - Given two objects A and B, the position of B relative to A can be derived from the position of A relative to B. 
P11 - Given an affine transformation t and two objects A and B, the position of t(A) relative to t(B) can be derived from t and the position of Arelative to B. 
P12 - Given an affine transformation tand two objects A and B, the transformation t can be derived from the position of A relative to B and the position of t(A) relative to t(B). 
P13 - Consider four objects A, B, A' and B' ; whether there exists an affine transformation t such that A'=t(A) and B'=t(B) can be derived from the position of A relative to B and the position of A' relative to B'. 

"""
class PhiDescriptor:

    TOPOLOGICAL = []
    DIRECTIONAL = []
    DISTANTIAL = []

    GROUPS = [
        {"A-A": ["argument", "void", "overlap", "referent"]}, 
        {"B-B": ["referent", "void", "overlap", "argument"]}, 
        {"A-B": ["covers", "trails", "overlaps", "uncovers"]}, 
        {"B-A": ["uncovers", "trails", "overlaps", "covers"]}, 
        {"A-AB": ["leads", "trails", "starts", "follows"]}, 
        {"B-AB": ["follows", "trails", "starts", "leads"]}, 
        {"AB-A": ["starts", "follows", "leads", "trails"]}, 
        {"AB-B": ["starts", "follows", "leads", "trails"]}, 
        {"AB-AB": ["starts", "follows", "leads", "trails"]}
        ] # Certaines points pairs peuvent être ignorées car redondantes avec d'autres

    def __init__(self, object1, object2):
        self.objects = [object1, object2] # ensemble des objets de l'espace euclidien [(A,B), (C, D), ...]
        
        # self.spacial = object[0].shape # Ensemble représentant l'espace euclidien entier (longueur, largeur)
        # Vérifier que objects n'est pas vide et que l'image est la meme entre les objets

    """
        Renvoies la liste des 
    """
    def _FHistogramme(self, theta):
        histogram = []
        rows, cols = self.objects[0].image.shape if self.objects[0].image.shape == self.objects[1].image.shape else None
        
        if rows == None:
            return "Les tailles d'image doivent être les memes"


        for row in range(rows):
            for col in range(cols):
                pixel = self.objects[0][row, col]
                if pixel == 0:
                    histogram.append(pixel)

        # Bresenham
        
        return histogram

    def _AllenHistogramm(self):
        pass

    def _getAreaFHistogramme(self):
        pass

    def _lengthHistogramme(self):
        pass

    """
        Arguments : 
            - (Object) index1 -> position dans objects de l'objet 1
            - (Objects) index2 -> position dans objects de l'objet 2
        
        Return :
            - (string) Définition de la relation entre les objects
    """
    def getPhiDescriptor(self):
        # vérifier que les objets appartiennent bien à la meme image
        return "a au dessus de b"