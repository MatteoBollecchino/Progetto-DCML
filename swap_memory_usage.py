import time

def genera_carico_swap(dim_totale_gb=4, incremento_mb=100, pausa_sec=1):
    """
    Genera un carico sulla swap memory allocando memoria oltre la capacità della RAM.
    
    :param dim_totale_gb: Dimensione totale della memoria da allocare (in GB).
    :param incremento_mb: Incremento della memoria allocata ad ogni iterazione (in MB).
    :param pausa_sec: Pausa tra ogni incremento in secondi.
    """
    blocco_dimensione = incremento_mb * 1024 * 1024  # Dimensione del blocco in byte
    totale_byte = dim_totale_gb * 1024 * 1024 * 1024  # Dimensione totale in byte

    print(f"Avvio allocazione di {dim_totale_gb} GB di memoria...")
    memoria = []
    try:
        for i in range(0, totale_byte, blocco_dimensione):
            # Alloca memoria creando blocchi di stringhe
            blocco = " " * blocco_dimensione
            memoria.append(blocco)  # Mantieni il blocco in memoria
            print(f"Allocati {len(memoria) * incremento_mb} MB di memoria.")
            time.sleep(pausa_sec)  # Pausa per osservare l'incremento
    except MemoryError:
        print("Memoria esaurita! La RAM e la swap sono al limite.")
    finally:
        print(f"Allocati in totale {len(memoria) * incremento_mb} MB di memoria.")
        input("Premi Invio per rilasciare la memoria...")
        # Libera tutta la memoria allocata
        memoria.clear()

if __name__ == "__main__":
    genera_carico_swap(dim_totale_gb=8, incremento_mb=100, pausa_sec=0.5)
