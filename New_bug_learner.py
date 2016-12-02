import os
from buildBugs import buildBugObjects
from filter_bugs import filtered_snapshots, scikit_input
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import GaussianNB
import pickle
import sklearn.linear_model as lm
from sklearn import svm
import numpy as np
from sklearn.model_selection import KFold
from LogisticRegression import LogisticRegression_CV
import matplotlib.pyplot as plt
import pylab as pl

def main(newData=0):
    if newData == 1:
        bugs = buildBugObjects()
        snapshots = filtered_snapshots(bugs)
    else:
        directory = 'bugs'
        bug_file = 'bugsFile'
        snapshot_file = 'snapshotFile'
        bugs = pickle.load(open(os.path.join(directory, bug_file), 'rb'))
        snapshots = pickle.load(open(os.path.join(directory, snapshot_file), 'rb'))

    snapshot_strings, priorities, labels = scikit_input(bugs, snapshots)

    print('Percentage of bugs kept = {}'.format(float(len(snapshots.bugs)) / float(len(bugs.bugs))))
    print('Percentage of snapshots with pri changes = {}'.format(float(labels.count(1)) / float(len(snapshots.bugs))))

    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(snapshot_strings)

    transformer = TfidfTransformer()
    normalized_counts = transformer.fit_transform(counts) .toarray()

    #Logistic Regression and plot of ROC, Precison vs Recall

    FPR = []
    TPR = []
    Precision = []
    Recall = []

    for criterion in range(5,50,2):
        FPR1,TPR1,Precision1,Recall1 = LogisticRegression_CV(normalized_counts, labels, criterion)
        FPR.append(FPR1)
        TPR.append(TPR1)
        Precision.append(Precision1)
        Recall.append(Recall1)


    print(FPR,TPR)
    pl.plot(FPR, TPR)
    # show the plot on the screen
    pl.xlabel('False Positive Rate')
    pl.ylabel('True Positive Rate')
    pl.title('Logistic Regression ROC Curve')
    pl.show()


    print(Precision,Recall)
    pl.plot(Precision, Recall)
    # show the plot on the screen
    pl.xlabel('Precision')
    pl.ylabel('Recall')
    pl.title('Logistic Regression Precision vs Recall')
    pl.show()

    return

if __name__ == "__main__":
    main()