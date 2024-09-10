import requests
import json
import time
import os

# Funzione per recuperare i dati delle sfide da fortniteapi.io
def recupera_e_salva_sfide(season, lang):
    url = f"https://fortniteapi.io/v3/challenges?season={season}&lang={lang}"
    headers = {
        "Authorization": os.getenv('API_KEY')
    }
    
    print(f"Tentativo di recuperare i dati delle sfide da {url}")
    
    risposta = requests.get(url, headers=headers)
    if risposta.status_code == 200:
        print("Recupero riuscito")
        dati = risposta.json()
        
        # Creazione della directory se non esiste
        directory = "data"
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Salvataggio dei dati nel file JSON
        file_path = f"{directory}/sfide_season{season}_{lang}.json"
        with open(file_path, "w") as file:
            json.dump(dati, file, indent=4)
            print(f"Dati salvati nel file {file_path}")
    else:
        print(f"Impossibile recuperare i dati: {risposta.status_code}")
        print("Contenuto della risposta:", risposta.content)

# Lista delle lingue e stagione per cui recuperare i dati
lista_lingue = ['es', 'it']
season = '31'  # Sostituisci con la stagione corrente

# Recupera e salva i dati delle sfide per ogni lingua
for lingua in lista_lingue:
    recupera_e_salva_sfide(season, lang)
    time.sleep(2)  # Pausa per evitare il rate-limiting
