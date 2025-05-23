import aiohttp
import asyncio
import json
import os

async def recupera_e_salva_sfide(session, season, lang, retries=3, delay=2):
    url = f"https://fortniteapi.io/v3/challenges?season={season}&lang={lang}"
    headers = {
        "Authorization": os.getenv('API_KEY')
    }

    for attempt in range(retries):
        try:
            print(f"Tentativo {attempt + 1}: Recupero dei dati delle sfide da {url}")
            async with session.get(url, headers=headers) as risposta:
                if risposta.status == 200:
                    print(f"Recupero riuscito per lingua {lang}")
                    dati = await risposta.json()

                    # Creazione della directory se non esiste
                    directory = "data"
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    # Salvataggio dei dati nel file JSON
                    file_path = f"{directory}/sfide_season{season}_{lang}.json"
                    with open(file_path, "w") as file:
                        json.dump(dati, file, indent=4)
                        print(f"Dati salvati nel file {file_path}")
                    return  # Esci dalla funzione se la richiesta ha successo

                elif risposta.status == 429:
                    retry_after = int(risposta.headers.get("Retry-After", 60))
                    print(f"Rate limit raggiunto. Attesa di {retry_after} secondi per lingua {lang}")
                    await asyncio.sleep(retry_after)
                else:
                    print(f"Errore {risposta.status}: Impossibile recuperare i dati per lingua {lang}")
                    await asyncio.sleep(delay)  # Attesa prima di riprovare

        except Exception as e:
            print(f"Errore durante il recupero: {e}")
            await asyncio.sleep(delay)  # Attesa prima di riprovare

    print(f"Impossibile recuperare i dati per lingua {lang} dopo {retries} tentativi")

async def main():
    season = '35'  # Sostituisci con la stagione corrente
    lista_lingue = ['es', 'it']

    async with aiohttp.ClientSession() as session:
        tasks = []
        for lang in lista_lingue:
            tasks.append(recupera_e_salva_sfide(session, season, lang))
        
        # Avvia tutte le richieste in parallelo
        await asyncio.gather(*tasks)

# Esegui il main loop
if __name__ == "__main__":
    asyncio.run(main())
