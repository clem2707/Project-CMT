import numpy as np
import matplotlib.pyplot as plt

# Paramètres du modèle
depth = 310  # Profondeur maximale du lac (m)
n_depth = 100  # Nombre de points de profondeur
n_time = 500  # Nombre de pas de temps
dt = 3600  # Intervalle de temps (en secondes, 1 heure)
dz = depth / n_depth  # Discrétisation de la profondeur

# Propriétés de l'eau
alpha = 1e-6  # Diffusivité thermique (en m²/s)

# Initialisation de la température
T = np.ones(n_depth) * 5  # Température initiale de 5°C sur tout le lac (hypolimnion)
T[0] = 15  # Température initiale de la surface (épilimnion)

# Fonction pour mettre à jour la température selon l'équation de diffusion thermique
def diffusion_step(T, alpha, dz, dt):
    # Création d'une nouvelle température T_new
    T_new = T.copy()
    
    # Appliquer l'équation de diffusion thermique (discrétisation centrée)
    for i in range(1, n_depth-1):  # Ne pas toucher aux bords (épilimnion et hypolimnion)
        T_new[i] = T[i] + alpha * dt / dz**2 * (T[i+1] - 2*T[i] + T[i-1])
    
    return T_new

# Simulation de la température sur plusieurs jours
for t in range(n_time):
    T = diffusion_step(T, alpha, dz, dt)
    
    # Mise à jour de la température de surface (épilimnion) en fonction de la température de l'air
    T[0] = 15  # Température de surface (à adapter selon les conditions météorologiques)
    
    # Mise à jour de l'hypolimnion (on suppose qu'il ne change pas)
    T[-1] = 5  # Température de l'hypolimnion stable

    # Affichage de la température à chaque 100 pas de temps
    if t % 100 == 0:
        plt.plot(np.linspace(0, depth, n_depth), T, label=f'Temps {t * dt / 86400:.1f} jours')

# Affichage du graphique
plt.xlabel("Profondeur (m)")
plt.ylabel("Température (°C)")
plt.title("Modélisation de la température du Lac Léman (1D)")
plt.legend()
plt.show()
