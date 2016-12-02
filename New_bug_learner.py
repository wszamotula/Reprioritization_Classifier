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

def main():
    newData = False
    if newData:
        bugs = buildBugObjects()
    else:
        directory = 'bugs'
        filename = 'bugsFile'
        bugs = pickle.load(open(os.path.join(directory,filename), 'rb'))
        # TODO: Should we also pickle the snapshot data?

    snapshots = filtered_snapshots(bugs)
    snapshot_strings, priorities, labels = scikit_input(bugs, snapshots)

    print('Number of snapshots = '+str(len(snapshots.bugs)))
    print('Number of bugs = ' + str(len(bugs.bugs)))
    print('Number of pri changes = ' + str(labels.count(1)))
    print('Percentage of bugs kept = {}'.format(len(snapshots.bugs) / float(len(bugs.bugs))))
    print('Percentage of snapshots with pri changes = {}'.format(labels.count(1)/ float(len(snapshots.bugs))))

    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(snapshot_strings)

    transformer = TfidfTransformer()
    # TODO: Add the priority to the normalized counts (input to NB)
    normalized_counts = transformer.fit_transform(counts).toarray()


    FPR = []
    TPR = []

    for criterion in range(5,50,2):
        FPR1,TPR1 = LogisticRegression_CV(normalized_counts, labels, criterion)
        FPR.append(FPR1)
        TPR.append(TPR1)

    print(FPR,TPR)
    pl.plot(FPR, TPR)
    # show the plot on the screen
    pl.show()


    # TODO: Should we switch to logistic regression to better cope with "rare disease" problem?
    #gnb = GaussianNB()
    # gnb.fit(normalized_counts, labels)
    # predictions = gnb.predict(normalized_counts)

    #scores = cross_val_score(gnb, normalized_counts, labels, cv=10)
    #print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    return

if __name__ == "__main__":
    main()