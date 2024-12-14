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


def inertie_thermique(temp_init, moyenne_temp, jours=365, facteur_inertie=0.1): # va lisser et "aplatir" (modestement) la courbe

    temp_ajust = temp_init.copy()

    for jour in range(jours):

        temp_ajust[jour] = temp_ajust[jour] * (1 - facteur_inertie) + facteur_inertie * moyenne_temp

    return temp_ajust


def courants_marins(temp_init, jours=365, facteur_courant=0.4): # facteur élevé pour voir une diff et encore c'est très peu visible, normalement 0.2
    
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
    facteur_bruit_journalier = 0.5
    facteur_bruit_annee= 0.2

    graphes = []

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    fig5, ax5 = plt.subplots(figsize=(10, 6))


    for annee in range(nb_annees):

        temp_init_re = rechauffement_climatique(temp_init, R, annee)
        temp_re = [0] * len(temps)

        temp_init_re_bruit = temp_init_re + random_normal(0, facteur_bruit_annee)
        temp_re_bruit = temp_re.copy()

        temp_re_bruit_extreme = temp_re.copy()

        temp_re_bruit_extreme_inertie = temp_re.copy()

        temp_re_bruit_extreme_inertie_courants = temp_re.copy()

        for i, jour in enumerate(temps):

            dT = deltaT(jour)
            temp_re[i] = temp_init_re + dT * np.sin((2 * np.pi / periode) * jour + phase)

            bruit_journalier = random_normal(0, facteur_bruit_journalier)
            temp_re_bruit[i] = temp_init_re_bruit + dT * np.sin((2 * np.pi / periode) * jour + phase) + bruit_journalier

            temp_re_bruit_extreme = evenements_extremes(temp_re_bruit)

            temp_re_bruit_extreme_inertie = inertie_thermique(temp_re_bruit_extreme, temp_init_re_bruit)

            temp_re_bruit_extreme_inertie_courants = courants_marins(temp_re_bruit_extreme_inertie)


        if annee % 25 == 0 or annee == 0 or annee == nb_annees - 1:
                
                ax1.plot(temps, temp_re, label=f"Année {2024 + annee}")
                ax2.plot(temps, temp_re_bruit, label=f"Année {2024 + annee}")

        if annee % 200 == 0 or annee == 0 or annee == nb_annees - 1:

            ax3.plot(temps, temp_re_bruit_extreme, label=f"Année {2024 + annee}")
            ax4.plot(temps, temp_re_bruit_extreme_inertie, label=f"Année {2024 + annee}")
            ax5.plot(temps, temp_re_bruit_extreme_inertie_courants, label=f"Année {2024 + annee}")


    graphes.append((fig1,ax1))
    graphes.append((fig2,ax2))
    graphes.append((fig3,ax3))
    graphes.append((fig4,ax4))
    graphes.append((fig5,ax5))


    titres = [
        "Température annuelle du Léman à la surface à {lieu.endroit}",
        "Température annuelle du Léman à la surface à {lieu.endroit} (avec bruit)",
        "Température annuelle du Léman à la surface à {lieu.endroit} (avec bruit et évènements extrêmes)",
        "Température annuelle du Léman à la surface à {lieu.endroit} (avec bruit, évènements extrêmes et inertie)",
        "Température annuelle du Léman à la surface à {lieu.endroit} (avec bruit, évènements extrêmes, inertie et courants)"
    ]


    for idx, (fig, ax) in enumerate(graphes):
        ax.set_title(titres[idx].format(lieu=lieu))
        ax.set_xlabel("Temps (jours)")
        ax.set_ylabel("Température (°C)")
        ax.legend()
        ax.grid()


for fig,ax in graphes:
    plt.show()