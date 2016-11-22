import os
from buildBugs import buildBugObjects
from filter_bugs import filtered_snapshots, scikit_input
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score
import pickle


def main():
    newData = True
    if newData:
        bugs = buildBugObjects()
    else:
        directory = 'bugs'
        filename = 'bugsFile'
        bugs = pickle.load(open(os.path.join(directory, filename), 'rb'))
        # TODO: Should we also pickle the snapshot data?

    snapshots = filtered_snapshots(bugs)
    snapshot_strings, priorities, labels = scikit_input(bugs, snapshots)

    print('Percentage of bugs kept = {}'.format(len(snapshots.bugs) / len(bugs.bugs)))
    print('Percentage of snapshots with pri changes = {}'.format(labels.count(1)/len(snapshots.bugs)))

    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(snapshot_strings)

    transformer = TfidfTransformer()
    normalized_counts = transformer.fit_transform(counts).toarray()

    for idx, pri in enumerate(priorities):
        normalized_counts[idx].append(pri)

    # TODO: Should we switch to logistic regression to better cope with "rare disease" problem?
    gnb = GaussianNB()
    # gnb.fit(normalized_counts, labels)
    # predictions = gnb.predict(normalized_counts)

    scores = cross_val_score(gnb, normalized_counts, labels, cv=10)
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

    return

if __name__ == "__main__":
    main()