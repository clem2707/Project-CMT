import pandas as pd
import os

def process_csv_files(folder_path, target_date, output_csv):
    # Liste pour stocker les résultats
    results = []

    # Coordonnées fixes (exemple de valeurs)
    x_coord = 46.2044
    y_coord = 6.1432

    # Parcourir chaque fichier dans le dossier
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            
            # Lire le fichier CSV
            df = pd.read_csv(file_path, quotechar='"')
            
            # Enlever les guillemets inversés des noms de colonnes
            df.columns = df.columns.str.replace('`', '')
            
            # Convertir la colonne 'date' au format datetime
            df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', errors='coerce')
            
            # Filtrer le DataFrame pour la date cible
            target_df = df[df['date'] == target_date]
            
            if not target_df.empty:
                # Obtenir la température pour la date cible
                temperature = target_df['temperature'].values[0]
                
                # Ajouter le résultat à la liste
                results.append({
                    'file_name': file_name,
                    'x_coord': x_coord,
                    'y_coord': y_coord,
                    'temperature': temperature
                })

    # Créer un DataFrame à partir des résultats
    results_df = pd.DataFrame(results)
    
    # Sauvegarder les résultats dans un fichier CSV
    results_df.to_csv(output_csv, index=False)

# Exemple d'utilisation
folder_path = "temperature_data"  # Remplacez par le chemin vers votre dossier contenant les fichiers CSV
target_date = pd.to_datetime("01/03/2025 03:00")  # Remplacez par votre date et heure cible
output_csv = "prediction.csv"  # Remplacez par le nom du fichier CSV de sortie

process_csv_files(folder_path, target_date, output_csv)

print(f"Les résultats ont été sauvegardés dans {output_csv}.")