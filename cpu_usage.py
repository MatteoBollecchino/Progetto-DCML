import multiprocessing
import time

def lavoro_intenso():
    """
    Funzione che simula un carico intenso sulla CPU.
    Esegue calcoli infiniti per mantenere il core occupato.
    """
    while True:
        _ = sum(i * i for i in range(10**6))  # Calcolo intensivo

def genera_carico_cpu(num_processi=None):
    """
    Avvia più processi per generare un carico significativo sulla CPU.
    
    :param num_processi: Numero di processi da avviare (equivale ai core da occupare).
                        Se None, utilizza il numero massimo di core disponibili.
    """
    if num_processi is None:
        num_processi = multiprocessing.cpu_count()  # Numero massimo di core

    print(f"Generando carico CPU su {num_processi} core...")
    processi = []
    for _ in range(num_processi):
        processo = multiprocessing.Process(target=lavoro_intenso)
        processo.start()
        processi.append(processo)
    
    try:
        # Mantieni il programma attivo per osservare l'uso della CPU
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interruzione ricevuta. Arresto dei processi...")
        for processo in processi:
            processo.terminate()
        for processo in processi:
            processo.join()

if __name__ == "__main__":
    genera_carico_cpu()
