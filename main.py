import requests
import json
import time
import os

def recupera_e_salva(url):
    print("Tentativo di recuperare", url)

    headers = {
        "Authorization": os.getenv('API_KEY')
    }
    
    risposta = requests.get(url, headers=headers)
    if risposta.status_code == 200:
        print("Recupero riuscito")
        return risposta.json()
    else:
        print(f"Impossibile recuperare l'API Fortnite: {risposta.status_code}")
        print("Contenuto della risposta:", risposta.content)
        return None

lista_lingue = ['es', 'it']
da_recuperare = [{
    "url": "https://fortniteapi.io/v2/items/list?fields=images,displayAssets,name,id,gameplayTags,rarity,type,series",
    "path": "tutti_gli_oggetti"
},{
    "url": "https://fortniteapi.io/v2/items/list?fields=name,id,gameplayTags,rarity,type",
    "path": "oggetti_piu_piccoli"
}]

for lingua in lista_lingue:
    for dir in da_recuperare:
        dati = recupera_e_salva(dir["url"] + f'&lang={lingua}')
        directory = "data"

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(f"{directory}/" + dir["path"] + f'_{lingua}.json', "w") as file:
            json.dump(dati, file, indent=4)
            print("Dati salvati nel file")

        time.sleep(2)
