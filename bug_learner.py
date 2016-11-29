import sys
import os
import numpy
from buildBugs import buildBugObjects
from filter_bugs import filtered_snapshots, scikit_input
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score
import pickle


def main(newData=1):
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
    normalized_counts = transformer.fit_transform(counts) #.toarray()

    for idx, pri in enumerate(priorities):
        numpy.append(normalized_counts[idx], pri)

    # TODO: Should we switch to logistic regression to better cope with "rare disease" problem?
    gnb = GaussianNB()
    # gnb.fit(normalized_counts, labels)
    # predictions = gnb.predict(normalized_counts)
    bugs = None
    snapshots = None

    scores = cross_val_score(gnb, normalized_counts.toarray(), labels, cv=10)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    return

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()