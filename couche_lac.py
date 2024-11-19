import math

def densite_eau(salinite=0):
    """
    Calcule la densité de l'eau en fonction de la salinité (en g/L).
    """
    densite_douce = 1000  # Densité de l'eau douce (en kg/m³)
    densite = densite_douce + salinite * 0.8  # Approximation de l'effet de la salinité
    return densite

def stratification_lac(profondeur, oxygene, clarte, salinite=0, saison='été'):
    """
    Détermine la couche d'un lac en fonction de la profondeur, de l'oxygénation, de la clarté de l'eau,
    de la salinité et de la saison.
    """
    
    # Paramètres seuils
    SEUIL_EPILIMNION = 10        # Profondeur maximale de l'épilimnion (en mètres)
    SEUIL_METALIMNION = 20       # Profondeur maximale de la couche métallimnion (en mètres)
    OXYGENE_MIN = 3              # Seuil de l'oxygénation (mg/L)
    CLARTE_MIN = 3               # Seuil de clarté (profondeur du disque de Secchi)
    DENSITE_TRANSITION = 1005    # Seuil de densité pour la stratification
    
    # Calcul de la densité de l'eau en fonction de la salinité
    densite = densite_eau(salinite)
    
    # Vérification des couches basées sur la saison
    if saison == 'hiver':
        # En hiver, les lacs peuvent être moins stratifiés, donc on simplifie la transition
        if profondeur <= SEUIL_EPILIMNION and oxygene > OXYGENE_MIN:
            return "Épilimnion"
        elif profondeur <= SEUIL_METALIMNION:
            return "Métalimnion"
        else:
            return "Hypolimnion"
    
    # En été, la stratification est plus marquée
    else:
        # Couche épilimnion : eau de surface claire et bien oxygénée
        if profondeur <= SEUIL_EPILIMNION and oxygene >= OXYGENE_MIN and clarte >= CLARTE_MIN:
            return "Épilimnion"
        
        # Couche métallimnion : transition avec oxygénation plus faible et moins de clarté
        elif profondeur <= SEUIL_METALIMNION and oxygene < OXYGENE_MIN and clarte < CLARTE_MIN:
            return "Métalimnion"
        
        # Couche hypolimnion : eau profonde et peu oxygénée
        elif profondeur > SEUIL_METALIMNION and densite > DENSITE_TRANSITION:
            return "Hypolimnion"
        else:
            return "Hypolimnion"

# Exemple d'utilisation
profondeur = 18       # en mètres
oxygene = 2           # en mg/L
clarte = 1.5          # en mètres
salinite = 1.5        # en g/L
saison = 'été'        # Saison ('été' ou 'hiver')

# Appel de la fonction pour déterminer la couche
couche = stratification_lac(profondeur, oxygene, clarte, salinite, saison)
print(f"La couche à cette profondeur est : {couche}")
