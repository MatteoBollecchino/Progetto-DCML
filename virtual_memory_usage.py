import mmap
import os
import time

def genera_carico_memoria_virtuale(dim_virtuale_gb=4, incremento_mb=100, pausa_sec=1):
    """
    Genera un carico sulla memoria virtuale allocando grandi quantità di memoria.
    
    :param dim_virtuale_gb: Dimensione totale della memoria virtuale da allocare in GB.
    :param incremento_mb: Incremento della memoria allocata ad ogni iterazione in MB.
    :param pausa_sec: Pausa tra ogni allocazione in secondi.
    """
    blocco_dimensione = incremento_mb * 1024 * 1024  # Dimensione del blocco in byte
    totale_byte = dim_virtuale_gb * 1024 * 1024 * 1024  # Dimensione totale in byte

    print(f"Avvio allocazione di {dim_virtuale_gb} GB nella memoria virtuale...")
    memoria = []
    try:
        for i in range(0, totale_byte, blocco_dimensione):
            # Crea una mappa di memoria (memoria virtuale)
            mappa = mmap.mmap(-1, blocco_dimensione)
            memoria.append(mappa)  # Mantieni il riferimento per non liberare la memoria
            print(f"Allocati {len(memoria) * incremento_mb} MB di memoria virtuale.")
            time.sleep(pausa_sec)  # Pausa per osservare l'incremento
    except MemoryError:
        print("Memoria virtuale esaurita! Limite raggiunto.")
    finally:
        print(f"Allocati in totale {len(memoria) * incremento_mb} MB di memoria virtuale.")
        input("Premi Invio per rilasciare la memoria...")
        # Libera tutta la memoria virtuale allocata
        for mappa in memoria:
            mappa.close()

if __name__ == "__main__":
    genera_carico_memoria_virtuale(dim_virtuale_gb=4, incremento_mb=100, pausa_sec=0.5)
