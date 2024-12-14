import numpy as np
import matplotlib.pyplot as plt
import Fonction_MAET as FM
import random


# nb aléatoire selon une distrib. normale
def random_normal(esperance, ecart_type):

    return random.gauss(esperance, ecart_type)


def rechauffement_climatique(temp_init, facteur_rechauffement, annee):

    temp_init_ajust = temp_init + facteur_rechauffement * annee
    
    return temp_init_ajust


def deltaT(jour):

    delta_T_max = 13
    delta_T_min = 4
    jour_changement_delta_T = 172

    delta_T = (delta_T_max + delta_T_min)/ 2 + (delta_T_max - delta_T_min)/2 * np.cos((2 * np.pi / 365) * (jour - jour_changement_delta_T) - np.pi / 6)

    return delta_T


def evenements_extremes(temp_init, annees=365, nb_even1=24, nb_even2=3):
   
    jours = list(range(annees))

    even1_jours = random.sample(jours, nb_even1)

    even2_jours = random.sample([jour for jour in jours if jour not in even1_jours], nb_even2)

    temp_ajust = temp_init.copy()

    for start in even1_jours:
        amplitude = random.uniform(1, 3)
        effet = random.choice([1, -1]) * amplitude

        for i in range(3):
            jour = (start + i) % annees
            temp_ajust[jour] += effet
    
    for start in even2_jours:
        amplitude = random.uniform(3, 5)
        effet = random.choice([1, -1]) * amplitude

        for i in range(4):
            day = (start + i) % annees
            temp_ajust[day] += effet

    return temp_ajust


def inertie_thermique(temp_init, moyenne_temp, jours=365, facteur_inertie=0.1):

    temp_ajust = temp_init.copy()

    for jour in range(jours):

        temp_ajust[jour] = temp_ajust[jour] * (1 - facteur_inertie) + facteur_inertie * moyenne_temp

    return temp_ajust


def courants_marins(temp_init, jours=365, facteur_courant=0.2):
    
    temp_ajust = temp_init.copy()

    for jour in range(jours):

        temp_ajust[jour] += np.random.uniform(-0.5, 0.5) * facteur_courant

    return temp_ajust


for lieu in FM.liste_lieux:

    # Données initales avec réchauffement climatique

    temp_init = lieu.temp
    periode = 365
    phase = 4 * np.pi / 3
    temps = np.linspace(0, 365, 365)
    R = 0.05  # facteur réchauffement climatique
    nb_annees = 100

    graphes = []


    fig1, ax1 = plt.subplots(figsize=(10, 6))

    for annee in range(nb_annees):

        temp_init_ajust = rechauffement_climatique(temp_init, R, annee)
        temp = []

        for jour in temps:

            dT = deltaT(jour)
            temp.append(temp_init_ajust + dT * np.sin((2 * np.pi / periode) * jour + phase))

        if annee % 25 == 0 or annee == 0 or annee == nb_annees - 1:
            ax1.plot(temps, temp, label=f"Année {2024 + annee}")


    ax1.set_title(f"Température annuelle du Léman à la surface à {lieu.endroit}")
    ax1.set_xlabel("Temps (jours)")
    ax1.set_ylabel("Température (°C)")
    ax1.legend()
    ax1.grid()

    graphes.append((fig1,ax1))


    # Avec bruit

    # Paramètres de bruit à ajuster
    
    facteur_bruit_journalier = 0.5
    facteur_bruit_annee= 0.2

    fig2, ax2 = plt.subplots(figsize=(10, 6))

    for annee in range(nb_annees):

        temp_init_ajust = rechauffement_climatique(temp_init, R, annee) + random_normal(0, facteur_bruit_annee)
        temp_bruit = [0] * len(temps)
        
        for i, jour in enumerate(temps):

            dT = deltaT(jour)
            bruit_journalier = random_normal(0, facteur_bruit_journalier)
            temp_bruit[i] = temp_init_ajust + dT * np.sin((2 * np.pi / periode) * jour + phase) + bruit_journalier

        if annee % 25 == 0 or annee == 0 or annee == nb_annees - 1:
            plt.plot(temps, temp_bruit, label=f"Année {2024 + annee}")


    ax2.set_title(f"Température annuelle du Léman à la surface à {lieu.endroit} (avec bruit)")
    ax2.set_xlabel("Temps (jours)")
    ax2.set_ylabel("Température (°C)")
    ax2.legend()
    ax2.grid()

    graphes.append((fig2,ax2))


    # Avec évènements extrêmes

    fig3, ax3 = plt.subplots(figsize=(10, 6))

    for annee in range(nb_annees):

        temp_init_ajust = rechauffement_climatique(temp_init, R, annee) + random_normal(0, facteur_bruit_annee)
        temp_bruit = [0] * len(temps)
        
        for i, jour in enumerate(temps):

            dT = deltaT(jour)
            bruit_journalier = random_normal(0, facteur_bruit_journalier)
            temp_bruit[i] = temp_init_ajust + dT * np.sin((2 * np.pi / periode) * jour + phase) + bruit_journalier
            temp_bruit_extreme = evenements_extremes(temp_bruit)

        if annee % 200 == 0 or annee == 0 or annee == nb_annees - 1:
            ax3.plot(temps, temp_bruit_extreme, label=f"Année {2024 + annee}")


    ax3.set_title(f"Température annuelle du Léman à la surface à {lieu.endroit} (avec bruit et évènements extrêmes)")
    ax3.set_xlabel("Temps (jours)")
    ax3.set_ylabel("Température (°C)")
    ax3.legend()
    ax3.grid()

    graphes.append((fig3,ax3))


    # Avec inertie thermique (lissage)

    fig4, ax4 = plt.subplots(figsize=(10, 6))

    for annee in range(nb_annees):

        temp_init_ajust = rechauffement_climatique(temp_init, R, annee) + random_normal(0, facteur_bruit_annee)
        temp_bruit = [0] * len(temps)
        
        for i, jour in enumerate(temps):

            dT = deltaT(jour)
            bruit_journalier = random_normal(0, facteur_bruit_journalier)
            temp_bruit[i] = temp_init_ajust + dT * np.sin((2 * np.pi / periode) * jour + phase) + bruit_journalier
            temp_bruit_extreme = evenements_extremes(temp_bruit)
            temp_bruit_extreme_inertie = inertie_thermique(temp_bruit_extreme, temp_init_ajust)

        if annee % 200 == 0 or annee == 0 or annee == nb_annees - 1:
            ax4.plot(temps, temp_bruit_extreme_inertie, label=f"Année {2024 + annee}")


    ax4.set_title(f"Température annuelle du Léman à la surface à {lieu.endroit} (avec bruit, évènements extrêmes et inertie)")
    ax4.set_xlabel("Temps (jours)")
    ax4.set_ylabel("Température (°C)")
    ax4.legend()
    ax4.grid()

    graphes.append((fig4,ax4))


    # Avec courants marins (n'apporte pas grand chose + la fonction courants marins prend bcp de temps)

    fig5, ax5 = plt.subplots(figsize=(10, 6))

    for annee in range(nb_annees):

        temp_init_ajust = rechauffement_climatique(temp_init, R, annee) + random_normal(0, facteur_bruit_annee)
        temp_bruit = [0] * len(temps)
        
        for i, jour in enumerate(temps):

            dT = deltaT(jour)
            bruit_journalier = random_normal(0, facteur_bruit_journalier)
            temp_bruit[i] = temp_init_ajust + dT * np.sin((2 * np.pi / periode) * jour + phase) + bruit_journalier
            temp_bruit_extreme = evenements_extremes(temp_bruit)
            temp_bruit_extreme_inertie = inertie_thermique(temp_bruit_extreme, temp_init_ajust)
            temp_bruit_extreme_inertie_courants = courants_marins(temp_bruit_extreme_inertie)

        if annee % 200 == 0 or annee == 0 or annee == nb_annees - 1:
            ax5.plot(temps, temp_bruit_extreme_inertie_courants, label=f"Année {2024 + annee}")


    ax5.set_title(f"Température annuelle du Léman à la surface à {lieu.endroit} (avec bruit, évènements extrêmes, inertie et courants)")
    ax5.set_xlabel("Temps (jours)")
    ax5.set_ylabel("Température (°C)")
    ax5.legend()
    ax5.grid()

    graphes.append((fig5,ax5))

   
    for fig,ax in graphes:
        plt.show()