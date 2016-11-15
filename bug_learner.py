from buildBugs import buildBugObjects
from filter_bugs import filtered_snapshots, scikit_input
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import GaussianNB

def main():
    bugs = buildBugObjects()
    snapshots = filtered_snapshots(bugs)
    print('Percentage of bugs kept = {}'.format(len(snapshots.bugs) / len(bugs.bugs)))
    snapshot_strings, labels = scikit_input(bugs, snapshots)
    print('Percentage of snapshots with pri changes = {}'.format(labels.count(1)/len(snapshots.bugs)))

    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(snapshot_strings)

    transformer = TfidfTransformer()
    normalized_counts = transformer.fit_transform(counts).toarray()

    gnb = GaussianNB()
    gnb.fit(normalized_counts, labels)
    predictions = gnb.predict(normalized_counts)

    # TODO: Add cross validation to estimate accuracy? Would this be bad with only 1% true classifications?
    print("Number of mislabeled points out of a total {} points : {}".format(normalized_counts.shape[0], (labels != predictions).sum()))

    return

if __name__ == "__main__":
    main()