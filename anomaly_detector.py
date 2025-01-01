import joblib
import sys

from pandas import read_csv
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, matthews_corrcoef
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

# Main Function
if __name__ == "__main__":

    # Load dataset from the selected file
    my_dataset = read_csv("labelled_dataset.csv")
    label_obj = my_dataset["label"]
    data_obj = my_dataset.drop(columns=["label", "time", "total_virtual_memory", "swap_total_memory",
                                        "power_plugged", "cpu_min_frequency", "cpu_max_frequency"])

    # Split the dataset
    train_data, test_data, train_label, test_label = train_test_split(data_obj, label_obj, test_size=0.7)

    # Choose an algorithm as a classifier
    classifiers = [VotingClassifier(estimators=[('lda', LinearDiscriminantAnalysis()),
                                                ('nb', GaussianNB()),
                                                ('dt', DecisionTreeClassifier())]),
                   DecisionTreeClassifier(),
                   KNeighborsClassifier(n_neighbors=15),
                   RandomForestClassifier(n_estimators=200),
                   RandomForestClassifier(n_estimators=50)]

    # Declarating list to contain the MCC value for each classifier
    mcc_list = []

    with open("metrics_result.txt", "w+", newline="") as file:
        # stdout is redirected to the file indicated
        sys.stdout = file

        print("Metrics Results \n")
        for clf in classifiers:
            # Training an algorithm
            clf = clf.fit(train_data, train_label)

            # Testing the trained model
            predicted_labels = clf.predict(test_data)

            # Computing metrics to understand how good an algorithm is
            accuracy = accuracy_score(test_label, predicted_labels)
            mcc = matthews_corrcoef(test_label, predicted_labels)
            f1score_weighted = f1_score(test_label, predicted_labels, average="weighted")

            mcc_list.append(mcc)

            tn, fp, fn, tp = confusion_matrix(test_label, predicted_labels).ravel()
            classifier_name = clf.__class__.__name__
            print("%s: Accuracy: %.4f, MCC: %.4f, F1-score weighted: %.4f, TP: %d, TN: %d, FN: %d, FP: %d" % (
                classifier_name, accuracy, mcc, f1score_weighted, tp, tn, fn, fp)) 

        # Finding the index of the classifier with the best MCC
        max_mcc_index = mcc_list.index(max(mcc_list))  

        final_classifier = classifiers[max_mcc_index] 
        print("\nFinal classifier: " ,final_classifier.__class__.__name__)

    # stdout is restored to the terminal
    sys.stdout = sys.__stdout__
    
    # Save the selected model in a specific file
    joblib.dump(final_classifier,"classifier2.z")

