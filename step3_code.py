import subprocess
from time import sleep
import joblib

# Main Function
if __name__ == "__main__":

    # The classifier selected after training is loaded from the file
    classifier = joblib.load("classifier.z")
    print("%s" % (classifier.__class__.__name__))

    # Il while serve a far rimanere il classifier in ascolto a runtime
    while True:
        sleep(1)
        break

    # Da usare quandoil detector riconosce un'anomaly 
    # subprocess.run('start cmd /k "echo Anomaly Detected!"', shell=True)