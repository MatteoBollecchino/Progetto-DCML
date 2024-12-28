import joblib
import sklearn

from pandas import read_csv
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, VotingClassifier
from sklearn.metrics import confusion_matrix, f1_score
import sklearn.metrics
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

def write_to_txt(filename, classifier_name, accuracy, mcc, first_time):
    if first_time:
        file = open(filename,  'w+', newline="") 
        file.write("Metrics Results \n\n")
    else:
        file = open(filename,  'a', newline="")

    file.writelines([str(classifier_name), ": ", "Accuracy is ", str(accuracy), "MCC is ", str(mcc),"\n"])

    file.close() 

# Main Function
if __name__ == "__main__":

    # Load dataset
    my_dataset = read_csv("labelled_dataset.csv")
    label_obj = my_dataset["label"]
    data_obj = my_dataset.drop(columns=["label", "time", "total_virtual_memory", "swap_total_memory",
                                        "power_plugged", "cpu_min_frequency", "cpu_max_frequency"])

    # Split dataset
    train_data, test_data, train_label, test_label = train_test_split(data_obj, label_obj, test_size=0.7)

    # Choose an algorithm as a classifier
    classifiers = [VotingClassifier(estimators=[('lda', LinearDiscriminantAnalysis()),
                                                ('nb', GaussianNB()),
                                                ('dt', DecisionTreeClassifier())]),
                   DecisionTreeClassifier(),
                   KNeighborsClassifier(n_neighbors=15),
                   RandomForestClassifier(n_estimators=200),
                   RandomForestClassifier(n_estimators=50),
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
        f1score = f1_score(test_label, predicted_labels, average=None)

        mcc_list.append(mcc)

        tn, fp, fn, tp = confusion_matrix(test_label, predicted_labels).ravel()
        classifier_name = clf.__class__.__name__
        # da modificare in formato con le virgole
        print("%s: Accuracy is %.4f, MCC is %.4f, TP: %d, TN: %d, FN: %d, FP: %d" % 
              (classifier_name, accuracy, mcc, tp, tn, fn, fp)) 

        # Da testare
        # All the information written on the terminal is also saved in a text file
        write_to_txt("metrics_result.txt",classifier_name, accuracy, mcc, first_time)
        first_time = False  

    # Finding the index of the classifier with the best MCC
    max_mcc_index = mcc_list.index(max(mcc_list))  

    final_classifier = classifiers[max_mcc_index] 
    print("Final classifier: %s" % (final_classifier.__class__.__name__)) 

    # Save the selected model in a file
    # joblib.dump(final_classifier,"classifier1.z")


