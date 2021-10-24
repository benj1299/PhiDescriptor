import os
import numpy as np
import cv2
from math import *
import shutil
import Objects

class Helper:

    """ 
        Make a numpy array of all images in the folder's path

        Parameters
        ----------
        folder (string) : the folder's path
    
        Returns
        -------
        Numpy array of all images readed by OpenCV
    """
    @staticmethod
    def load_images_from_folder(folder):
        images = []
        for filename in os.listdir(folder):
            img = cv2.imread(os.path.join(folder,filename), 0) # Gray Color converting
            if img is not None:
                images.append(img)
        return np.array(images, dtype=object)

    """ 
        Supprime le contenu d'un dossier

        Parameters
        ----------
        folder (string) : the folder's path
    
        Returns
        -------
    """
    @staticmethod
    def auto_remove_results(folder="./resultats"):
        if not os.path.exists(folder):
            os.makedirs(folder)
            return
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Problème de suppression %s. Raisonz: %s' % (file_path, e))

    """ 
        Bresenham's Algorithm
        Produces a list of tuples from start and end

         Parameters
        ----------
            start (tuple of float) : the departure point
            end (tuple of float) : the end point

        Returns
        -------
            Numpy array of all points of the segment

        Tests
        -----
            points1 = get_line((0, 0), (3, 4))
            points2 = get_line((3, 4), (0, 0))
            assert(set(points1) == set(points2))
            print points1
        [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
            print points2
        [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    @staticmethod
    def bresenham(start, end):
        # Setup initial conditions
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
    
        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)
    
        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
    
        # Swap start and end points if necessary and store swap state
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True
    
        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1
    
        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1
    
        # Iterate over bounding box generating points between start and end
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx
    
        # Reverse the list if the coordinates were swapped
        if swapped:
            points.reverse()
        return np.array(points)

    """
        Calcule la distance euclidienne de deux vecteurs

        Argument
        --------
        Vecteurs

        Return
        ------
        Distance en Float
    """
    @staticmethod
    def euclidean_distance(vec1, vec2):
        return np.sum(np.sqrt((vec1 - vec2)**2))

    @staticmethod
    def distance(a,b):
        x1 = a[0]
        x2 = b[0]
        y1 = a[1]
        y2 = b[1]
        return sqrt((x1-x2)**2+(y1-y2)**2)

    @staticmethod
    def sumDistance(a,points):
        sum = 0
        for point in points:
            sum += distance(a,point)
        return sum

    @staticmethod
    def preprocessImages(images_path):
        images = Helper.load_images_from_folder(images_path)

        for index, image in enumerate(images):
            # Resizing de l'image en 100x100
            image = cv2.resize(image, (100,100), interpolation=cv2.INTER_LINEAR) # Vérifier les autres types d'interpolation

            # Binarisation et utilisation de OTSU pour déterminer le seuil automatiquement
            _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) # Ne detecte que les flèches noires, il faut modifier le param 2 et 3 pour inverser cela et ajouter l'inverse de l'image
            
            # Ajouter un convexHull pour rendre l'image convex et faciliter le traitement

            # Remplace l'ancienne image par la nouvelle
            images[index] = image

            # Sauvegarde les images
            cv2.imwrite(images_path+'/resultats/image_{}.png'.format(index), image)
        
        return images

    """
        Génère la liste des objets des images injectées en argument 
    """
    def generateObjects(images):
        liste = []
        for image in images:
            object = Objects(image)
            liste.append(object)
        return liste