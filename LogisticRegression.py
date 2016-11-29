import sklearn.linear_model as lm
from sklearn import svm
import numpy as np
from sklearn.model_selection import KFold


def LogisticRegression_CV(normalized_counts, labels, criterion):
    precision = []
    recall = []
    kf = KFold(n_splits=10)
    for train, test in kf.split(normalized_counts):
        Train_normalized_counts = [normalized_counts[i] for i in list(train)]
        Train_labels = [labels[i] for i in list(train)]
        Test_normalized_counts = [normalized_counts[i] for i in list(test)]
        Test_labels = [labels[i] for i in list(test)]

        LogisticReg = lm.LogisticRegression()
        LogisticReg.fit(Train_normalized_counts, Train_labels)

        T = LogisticReg.predict_proba(Test_normalized_counts)

        Predict_Label1 = []
        for term in T:
            if (term[1] > criterion):
                Predict_Label1.append(1)
            else:
                Predict_Label1.append(0)
        j2 = [i for i in Predict_Label1 if i == 1]
        print('The number of labels (>' + str(criterion) + ') as 1 = ' + str(len(j2)))

        a11 = 0
        a12 = 0
        a21 = 0
        a22 = 0

        for i in range(0, len(Test_labels)):
            if ((Test_labels[i] == 0) and (Predict_Label1[i] == 0)):
                a11 = a11 + 1
            if ((Test_labels[i] == 1) and (Predict_Label1[i] == 0)):
                a12 = a12 + 1
            if ((Test_labels[i] == 0) and (Predict_Label1[i] == 1)):
                a21 = a21 + 1
            if ((Test_labels[i] == 1) and (Predict_Label1[i] == 1)):
                a22 = a22 + 1
        print('TN = ' + str(a11))
        print('FN = ' + str(a12))
        print('FP = ' + str(a21))
        print('TP = ' + str(a22))
        if((a22+a21) != 0):
            precision.append(a22 / float(a22 + a21))
        if((a22+a12) != 0):
            recall.append(a22 / float(a22 + a12))
    average_precision = sum(precision) / float(len(precision))
    print('Average Precision is ' + str(average_precision))
    average_recall = sum(recall) / float(len(recall))
    print('Average Recall is ' + str(average_recall))
