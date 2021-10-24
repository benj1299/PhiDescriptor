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

    def __init__(self, objects=[]):
        self.objects = objects # [(A,B), (C, D), ...]

    def _FHistogramme(self, theta):
        # Définir les connected Components
        pass

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
    def _getPhiDescriptor(self, index1, index2):
        # vérifier que les objets appartiennent bien à la meme image
        pass