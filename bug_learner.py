from buildBugs import buildBugObjects
from filter_bugs import filtered_snapshots, scikit_input
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

def main():
    bugs = buildBugObjects()
    snapshots = filtered_snapshots(bugs)
    snapshot_strings, output = scikit_input(bugs, bugs)

    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(snapshot_strings)

    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(counts)

    return

if __name__ == "__main__":
    main()