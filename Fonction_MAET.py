# Calcul Mean Annuel Epilimnetic Temperature

def MAET(coord):
    
    p1 = (750 / (90 - (coord.lat**0.85)))**1.29
    p2 = 0.1 * (coord.alt**0.5)
    p3 = 0.25 * ((coord.cont**0.9) + 500)**0.52

    maet = 44 - p1 - p2 -p3
    maet_rect = round(maet, 5)
    coord.temp = maet_rect

    print(f"La température moyenne annuelle à l'épilimnion à {coord.endroit} est {coord.temp} °C.")

    return maet_rect


class lieu:

    def __init__(self, nom, lat, alt, cont, temp = None):
    
        self.endroit = nom
        self.lat = lat
        self.alt = alt
        self.cont = cont
        self.temp = temp


# Morges

lat_morges = 46.503533903991766
alt_morges = 371.90
cont_morges = 0.01570

morges = lieu("Morges", lat_morges, alt_morges, cont_morges)


# Eaux_vives

lat_eaux_vives = 46.2110157511242656
alt_eaux_vives = 371.90
cont_eaux_vives = 0.14770

eaux_vives = lieu("Eaux-vives", lat_eaux_vives, alt_eaux_vives, cont_eaux_vives)


# Possibilté de rajouter d'autres lieux


# Tous les endroits

liste_lieux = [morges, eaux_vives]

liste_moy_temp_annuelle = []

for endroit in liste_lieux:

    liste_moy_temp_annuelle.append(MAET(endroit))

print(liste_moy_temp_annuelle)