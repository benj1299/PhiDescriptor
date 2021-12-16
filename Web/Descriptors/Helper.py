# -*-coding:utf-8 -*
import os
import numpy as np
import cv2
from math import *
import shutil
from .Object import Object
from shapely.geometry.polygon import Polygon

class Helper:

    # Define Infinite (Using INT_MAX  
    # caused overflow problems)
    INT_MAX = 10000

    @staticmethod
    def createVector(x1,y1,x2,y2, img):
        #Premier vecteur de direction x
        v1 = (img.shape[0] - x1,y1 - y1)
        #Deuxième vecteur de direction passant par les deux points
        v2 = (x2 - x1, y2 - y1)
        return v1,v2

    #Retourne le vecteur unitaire associé au vecteur
    @staticmethod
    def unit_vector(vector):
        return vector / np.linalg.norm(vector)
    
    """
        Fonction de Dirac
    """
    @staticmethod
    def dirac(x):
        if x == 0:
            return 0
        else:
            return 1

    @staticmethod
    def preprocessImage(image_path):
        gray = cv2.imread(image_path, 0)

        # Resizing de l'image en 100x100 # image carré
        #image = cv2.resize(image, (100,100), interpolation=cv2.INTER_LINEAR) # Vérifier les autres types d'interpolation

        # Binarisation et utilisation de OTSU pour déterminer le seuil automatiquement
        _, image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # Sauvegarde les images
        #cv2.imwrite(image_path, image)
        return cv2.Canny(gray, 30, 200)

    """
        Génère la liste des Objets de l'image injectée en argument 
    """
    @staticmethod
    def convertImageToObjects(image):
        objects = []
        
        contours,_ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours :
            pts = []
            for point in cnt:
                pts.append({
                    "x": point[0][0],
                    "y": point[0][1]
                })
            objects.append(Object(image, {
                "points": pts,
                "area": cv2.contourArea(cnt),
                "polygon": Polygon(np.squeeze(cnt)), # Supprime la dimension en trop de findContours()
                "cnt": np.squeeze(cnt)
            }))

        return objects