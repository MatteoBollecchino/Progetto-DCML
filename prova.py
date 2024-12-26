import csv

def elimina_colonna(file_input, file_output, nome_colonna):
    # Legge il file di input
    with open(file_input, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        # Ottiene i nomi delle colonne esistenti
        colonne = reader.fieldnames
        
        # Verifica che la colonna da eliminare esista
        if nome_colonna not in colonne:
            print(f"Errore: la colonna '{nome_colonna}' non esiste nel file CSV.")
            return
        
        # Scrive il file di output senza la colonna specificata
        with open(file_output, mode='w', newline='', encoding='utf-8') as outfile:
            # Nuova lista di colonne senza la colonna da eliminare
            nuove_colonne = [col for col in colonne if col != nome_colonna]
            
            writer = csv.DictWriter(outfile, fieldnames=nuove_colonne)
            writer.writeheader()
            for row in reader:
                # Scrive solo le colonne rimanenti
                nuova_riga = {col: row[col] for col in nuove_colonne}
                writer.writerow(nuova_riga)
    
    print(f"Colonna '{nome_colonna}' eliminata con successo. File salvato come '{file_output}'.")

# Esempio di utilizzo
file_input = "labelled_dataset.csv"
file_output = "labelled_dataset.csv"
nome_colonna = 'label'

elimina_colonna(file_input, file_output, nome_colonna)
