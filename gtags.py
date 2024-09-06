import requests
import json
import time
import os

# Funzione per ottenere tutti i gameplayTags da fortniteapi.io
def get_all_gameplay_tags(lang):
    url = f"https://fortniteapi.io/v2/items/list?fields=name,id,gameplayTags,rarity,type&lang={lang}"
    headers = {
        "Authorization": os.getenv('API_KEY')
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return {item["id"]: item.get("gameplayTags", []) for item in data.get("items", [])}
    else:
        print(f"Error {response.status_code} durante la richiesta di gameplayTags")
        return {}

# Funzione per recuperare i dati dei cosmetici da fortnite-api.com
def recupera_e_arricchisci(url, gameplay_tags_data):
    print(f"Tentativo di recuperare i dati da {url}")
    
    risposta = requests.get(url)
    if risposta.status_code == 200:
        print("Recupero riuscito")
        dati = risposta.json()
        items = dati.get("data", [])

        arricchiti = []
        # Arricchimento dei dati con i gameplayTags
        for item in items:
            item_id = item.get("id", "")
            if item_id:
                # Aggiungi i gameplayTags solo se presenti
                gameplay_tags = gameplay_tags_data.get(item_id, [])
                if gameplay_tags:
                    item["gameplayTags"] = gameplay_tags
                arricchiti.append(item)
            else:
                print("ID del cosmetico mancante.")
        
        return {"data": arricchiti}  # Ritorna i cosmetici arricchiti
    else:
        print(f"Impossibile recuperare i dati: {risposta.status_code}")
        return None

# Lista delle lingue e URL da cui recuperare i dati
lista_lingue = ['es', 'it']
url_base = "https://fortnite-api.com/v2/cosmetics/br?language="

# Recupera tutti i gameplayTags una sola volta per ogni lingua
for lingua in lista_lingue:
    gameplay_tags_data = get_all_gameplay_tags(lingua)
    
    url = url_base + lingua
    dati = recupera_e_arricchisci(url, gameplay_tags_data)
    directory = "data"

    if not os.path.exists(directory):
        os.makedirs(directory)

    if dati is not None:
        file_path = f"{directory}/items_{lingua}.json"
        with open(file_path, "w") as file:
            json.dump(dati, file, indent=4)
            print(f"Dati salvati nel file {file_path}")
    
    time.sleep(2)
