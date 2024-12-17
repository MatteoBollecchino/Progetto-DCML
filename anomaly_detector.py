import random
import time

import sklearn
from pandas import read_csv
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, VotingClassifier
from sklearn.metrics import confusion_matrix
import sklearn.metrics
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

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
    classifiers = [VotingClassifier(estimators=[('lda', LinearDiscriminantAnalysis()),
                                                ('nb', GaussianNB()),
                                                ('dt', DecisionTreeClassifier())]),
                   DecisionTreeClassifier(),
                   KNeighborsClassifier(n_neighbors=11),
                   RandomForestClassifier(n_estimators=10),
                   RandomForestClassifier(n_estimators=3),
                   GradientBoostingClassifier()]

    # Declarating list to contain the MCC values for each classifier
    mcc_list = []

    for clf in classifiers:
        # Training an algorithm
        clf = clf.fit(train_data, train_label)

        # Testing the trained model
        predicted_labels = clf.predict(test_data)

        # Computing metrics to understand how good an algorithm is
        accuracy = sklearn.metrics.accuracy_score(test_label, predicted_labels)
        mcc = sklearn.metrics.matthews_corrcoef(test_label, predicted_labels)

        mcc_list.append(mcc)

        tn, fp, fn, tp = confusion_matrix(test_label, predicted_labels).ravel()
        print("%s: Accuracy is %.4f, MCC is %.4f, TP: %d, TN: %d, FN: %d, FP: %d" % 
              (clf.__class__.__name__, accuracy, mcc, tp, tn, fn, fp))   

    # Finding the index of the classifier with the best MCC
    max_mcc_index = mcc_list.index(max(mcc_list))   

    final_classifier = classifiers[max_mcc_index] 


