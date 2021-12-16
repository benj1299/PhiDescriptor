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
import numpy as np
import cv2
from .Helper import *
from scipy.integrate import quad
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon, LineString

class PhiDescriptor:

    # Retourne le diviseur de la norme
    def ft(self, category):
        if category in [10, 18, 32]:
            return 1
        if category == 36:
            return 2
        return 0

    # Retourne le diviseur de la norme
    def ff(self, category):
        if category in [26, 30]:
            return 1
        if category == 34:
            return 2
        return 0      

    # Retourne le diviseur de la norme
    def fo(self, category):
        if category in [3, 7]:
            return 2
        if category == 15:
            return 1
        return 0

    # Retourne le diviseur de la norme
    def fl(self, category):
        if category in [27, 31]:
            return 1
        if category == 35:
            return 2
        return 0

    # Retourne le diviseur de la norme
    def fc(self, category):
        if category in [9, 16]:
            return 1
        return 0
    
    # Retourne le diviseur de la norme
    def fs(self, category):
        if category in [25, 29]:
            return 2
        if category == 33:
            return 1
        return 0

    # Retourne le diviseur de la norme
    def fu(self, category):
        if category == 12:
            return 1
        return 0

    # Retourne le diviseur de la norme
    def fv(self, category):
        if category in [2, 6]:
            return 2
        return 0

    # Retourne le diviseur de la norme
    def fa(self, category):
        if category in [1, 8]:
            return 2
        return 0

    # Retourne le diviseur de la norme
    def fr(self, category):
        if category in [4, 5]:
            return 2
        return 0

    # Retourne le diviseur de la norme
    def fe(self, category):
       return 1

    # Retourne le diviseur de la norme
    def fd(self, category):
        return 1
    
    # Retourne le diviseur de la norme
    def fw(self, category):
        return 2

    CATEGORIES = {
        "trails": {
            "function": ft,
            "numbers": []
        },
        "follows": {
            "function": ff,
            "numbers": []
        },
        "overlaps": {
            "function": fo,
            "numbers": []
        },
        "leads": {
            "function": fl,
            "numbers": []
        },
        "covers": {
            "function": fc,
            "numbers": []
        },
        "starts": {
            "function": fs,
            "numbers": []
        },
        "uncovers": {
            "function": fu,
            "numbers": []
        },
        "void": {
            "function": fv,
            "numbers": []
        },
        "argument": {
            "function": fa,
            "numbers": []
        },
        "referent": {
            "function": fr,
            "numbers": []
        },
        "encloses": {
            "function": fe,
            "numbers": []
        },
        "divides": {
            "function": fd,
            "numbers": []
        },
        "width": {
            "function": fw,
            "numbers": []
        }
    }

    TOTAL_CATEGORIES = [
        [2],
        [1, 3],
        [2, 4, 5, 6],
        [1, 3, 4, 5, 6],
        [5],
        [4, 6],
        [1, 2, 3, 5],
        [1, 2, 3, 4, 6],
        [2, 3, 6],
        [1, 6],
        [2, 3, 4, 5],
        [1, 4, 5],
        [3, 5, 6],
        [3, 4],
        [1, 2, 4, 5],
        [1, 2, 4],
        [2, 6],
        [1, 3, 6],
        [2, 4, 5],
        [1, 3, 4, 5],
        [3, 5],
        [3, 4, 6],
        [1, 2, 5],
        [1, 2, 4, 6],
        [2, 5, 6],
        [1, 3, 5, 6],
        [2, 4],
        [1, 3, 4],
        [2, 3, 5],
        [1, 5],
        [2, 3, 4, 6],
        [1, 4, 6],
        [2, 5],
        [1, 3, 5],
        [2, 4, 6],
        [1, 3, 4, 6]
    ]

    def __init__(self, object1, object2):
        self.objects = [object1, object2]
        self.theta = np.pi/2

    """
        Calcule le F-Histogram se basant sur https://www.scitepress.org/Papers/2012/37816/37816.pdf
        La densité de masse de A/B au point p/q est le degré d'appartenance A/B(p)
        On retourne ici l'intégrale de toutes les forces infinidécimales
    """
    def _FHistogramme(self, obj1, obj2):
        forces = []
        for p in obj1.points:
            for q in obj2.points:
                if p.id != q.id:
                    vector = Helper.createVector(p["coordonates"]["x"], q["coordonates"]["x"], p["coordonates"]["y"], q["coordonates"]["y"], self.objects[0].image)
                    magnitude = (p["weight"] * q["weight"])/np.linalg.norm(vector) 
                    forces.append(magnitude * Helper.unit_vector(vector))
        return quad(forces)
    
    """
        Renvoie un tableau contenant les aires de chaque catégorie
    """
    def _getAreaFHistogramme(self):
        result = []
        F = 0
        divider = 1
        for p in self.objects[0].points:
            for q in self.objects[1].points:
                output = self._getPointCategory(p, q)
                denominateur = None
                if output is not None:
                    name, denominateur = output
                if denominateur is not None:
                    raise Exception(self._getPointCategory(p,q))
                    divider += 1 if denominateur != 0 else 0
                    if name == "width":
                        result.append({"force": np.linalg.norm(p,q)/denominateur, "divider": divider, "name": name})
                        continue
                    F += np.linalg.norm(p,q)/denominateur
                    result.append({"force": F, "divider": divider, "name": name})
        return result

    """
        Renvoie le Length Histogram d'une aire
    """
    def _getLengthHistogram(self, area, category):
        return area["force"]/area["divider"]
        
    """
        Construit les 12 catégories de points
        Renvoie la matrice correspondante
    """
    def _buildPointCategory(self, p,q):  
        category_matrix = []  
        join = True

        if p["object"].component["polygon"].contains(q):
            # q in p.polygon
            join = False
            if q["type"] == 0:
                category_matrix = [[0,1], [1,1]]
            else:
                category_matrix = [[1,0], [1,1]]
        else:
            # q not in p.polygon 
            join = False
            if q["type"] == 0:
                category_matrix = [[0,1], [0,0]]
            else:
                category_matrix = [[1,0], [0,0]]

        if q["object"].component["polygon"].contains(p):
            # p in q.polygon
            join = False
            if p["type"] == 0:
                category_matrix = [[1,1], [0,1]]
            else:
                category_matrix = [[1,1], [1,0]]
        else:
            # p not in q.polygon
            join = False
            if p["type"] == 0:
                category_matrix = [[0,0], [0,1]]
            else:
                category_matrix = [[0,0], [1,0]]

        if p["object"].id != q["object"].id and join:
            # AB entry/entry ou exit/exit
            if p["type"] == q["type"]:
                if p["type"] == 0:
                    category_matrix = [[0,1], [0,1]]
                else:
                    category_matrix = [[1,0], [1,0]]
            # AB entry/exit ou exit/entry
            else:
                if p["type"] == 0 and q["type"] == 1:
                    category_matrix = [[0,1], [1,0]]
                if p["type"] == 1 and p["type"] == 0:
                    category_matrix = [[1,0], [0,1]]

        return category_matrix
    
    """
        Renvoie le numéro de la catégorie appartenant aux points donnés en entrée
    """
    def _getPointCategory(self, p, q):
        category_number = -1
        category_name = ""
        category_value = None

        # Revoies None si q n'est pas le successeur de p
        if p["intersection_number"] >= q["intersection_number"] or p["coordonates"]["x"] != p["coordonates"]["x"]:
            return None
        
        p = Point(p["coordonates"]["x"], p["coordonates"]["y"]) # B
        q = Point(q["coordonates"]["x"], q["coordonates"]["y"]) # A

        # Construit les catégories de chaque point 
        p_category = self._buildPointCategory(p,q)
        q_category = self._buildPointCategory(q,p)

        # Applatit puis transforme le tableau pour faire des comparaisons
        pq_category = np.array([ [p_category[0][0], p_category[1][0]], [Helper.dirac(p_category[0][1] + q_category[0][0]), Helper.dirac(p_category[1][1] + q_category[1][0])], [q_category[0][1], q_category[1][1]] ])
        valueToIndex = lambda x: x.index+1 if x == 1 else None
        pg_flat = valueToIndex(pq_category.flatten())

        # Permet d'obtenir le numéro de la categorie
        for idx, cat in enumerate(self.TOTAL_CATEGORIES):
            if cat == pg_flat:
                category_number = idx+1
        
        for item in self.CATEGORIES.items():
            name, category = item
            if category_number in category["numbers"]:
                category_name = name
                category_value = category["function"](category_number)

        return category_name, category_value

    """
        Génère une liste de points associé à un type
    """
    def _generateIntersectionPoints(self):
        image = self.objects[0].image.copy()

        for col in range(0, image.shape[1]):
            line = LineString([(col, 0), (col, image.shape[0])])
            nb_intersections = 0
            last_obj = None

            for row in range(0, image.shape[0]):
                if image[row, col] == 255: # Un point de contour est detecté
                    point = Point(col, row)
                    
                    for i, objet in enumerate(self.objects):
                        # Vérifie que le point se trouve dans l'objet
                        if line.intersects(objet.component["polygon"]) and line.intersects(point):
                            nb_intersections += 1
                            if last_obj is None:
                                type = 0
                            else:
                                type = 1 if last_obj.id == objet.id else 0

                            self.objects[i].points.append({
                                "object": objet,
                                "coordonates": {
                                    "x": col,
                                    "y": row
                                },
                                "intersection_number": nb_intersections,
                                "type": type # 0 : entry, 1 : exit
                            })
                            last_obj = objet

    """
        Arguments : 
            - (Object) index1 -> position dans objects de l'objet 1
            - (Objects) index2 -> position dans objects de l'objet 2
        
        Return :
            - (string) Définition de la relation entre les objects
    """
    def getPhiDescriptor(self):
        phi = []

        # Map tous les points d'intersection
        self._generateIntersectionPoints()

        # Calcul les régions d'interraction (aire)
        areas = self._getAreaFHistogramme()

        # Cacul les length Histograms et génère le phi descripteur
        for area in areas:
            phi.append({
                "category_area": area["name"],
                "length": self._getLengthHistograms(area),
                })

        # retourner la position et sa précision
        return "a au dessus de b", "100"