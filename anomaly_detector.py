import random
import time

import sklearn
from pandas import read_csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import sklearn.metrics
from sklearn.model_selection import train_test_split

# Sets random seed to increase repeatability
random.seed(23)

if __name__ == "__main__":

    # Load dataset
    my_dataset = read_csv("labelled_dataset.csv")
    label_obj = my_dataset["label"]
    data_obj = my_dataset.drop(columns=["label", "time", "datetime"])

    # Split dataset
    train_data, test_data, train_label, test_label = train_test_split(data_obj, label_obj, test_size=0.5)

    # Choose an algorithm as a classifier
    classifiers = RandomForestClassifier(n_estimators=200)

    # Training the algorithm
    classifiers = classifiers.fit(train_data, train_label)

    # Testing the trained model
    predicted_labels = classifiers.predict(test_data)

    # Computing metrics to understand how good an algorithm is
    accuracy = sklearn.metrics.accuracy_score(test_label, predicted_labels)
    mcc = sklearn.metrics.matthews_corrcoef(test_label, predicted_labels)
    tn, fp, fn, tp = confusion_matrix(test_label, predicted_labels).ravel()
    print("Accuracy is %.4f, MCC is %.4f, TP: %d, TN: %d, FN: %d, FP: %d" % (accuracy, mcc, tp, tn, fn, fp))        
