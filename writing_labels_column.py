import csv

def aggiungi_colonna_csv(nome_file, nome_colonna, valori_colonna):
    """
    Aggiunge una colonna a un file CSV esistente.
    
    :param nome_file: Nome del file CSV da modificare.
    :param nome_colonna: Nome della nuova colonna da aggiungere.
    :param valori_colonna: Lista dei valori per la nuova colonna.
    """
    # Leggi il contenuto del file CSV
    with open(nome_file, mode='r', newline='', encoding='utf-8') as file_csv:
        lettore = list(csv.reader(file_csv))
        
        # Aggiungi il nome della colonna come intestazione
        if len(lettore) > 0:
            lettore[0].append(nome_colonna)
        else:
            # Se il file è vuoto, crea solo l'intestazione
            lettore.append([nome_colonna])
        
        # Aggiungi i valori della colonna
        for i, valore in enumerate(valori_colonna):
            if i + 1 < len(lettore):
                lettore[i + 1].append(valore)
            else:
                # Se ci sono più valori che righe, aggiungi nuove righe
                nuova_riga = [''] * (len(lettore[0]) - 1) + [valore]
                lettore.append(nuova_riga)

    # Scrivi il contenuto aggiornato nel file CSV
    with open(nome_file, mode='w', newline='', encoding='utf-8') as file_csv:
        scrittore = csv.writer(file_csv)
        scrittore.writerows(lettore)

# Esempio di utilizzo
nome_file_csv = "labelled_dataset.csv"
nome_nuova_colonna = "label"
dimensione_dataset = 39
valori = []

# Da modificare (classificazione usata per prova)
for i in range(dimensione_dataset):
    if i in range(15):
        valori.append("normal")
    elif i in range(16,30):
        valori.append("anomaly")
    else:
        valori.append("normal")


aggiungi_colonna_csv(nome_file_csv, nome_nuova_colonna, valori)
