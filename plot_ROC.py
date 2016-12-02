import sys
import os
import numpy
from buildBugs import buildBugObjects
from filter_bugs import filtered_snapshots, scikit_input
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import GaussianNB,MultinomialNB
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.model_selection import StratifiedKFold
from scipy import interp
import matplotlib.pyplot as plt
import pickle


def main(newData=1):
    newData = 0 #Use existing data
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
    mnb = MultinomialNB()
    # gnb.fit(normalized_counts, labels)
    # predictions = gnb.predict(normalized_counts)
    bugs = None
    snapshots = None

    scores = cross_val_score(mnb, normalized_counts.toarray(), labels, cv=10)
    
    
    
    #predictions=cross_val_predict(gnb, normalized_counts.toarray(), labels, cv=10)
    #print(predictions)

    #precision,recall,thresh=precision_recall_curve(labels,predictions)

    print("the len of the scores is "+str(len(scores)))
    #print("the len of the predictions is"+str(len(predictions)))
    print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    
    # Run classifier with cross-validation and plot ROC curves
    cv = StratifiedKFold(n_splits=10)
    classifier = MultinomialNB()
    
    X = normalized_counts.toarray()
    y = labels
    print("total pos label" +str(sum(y)))
    print("The number of elements in X is "+str(len(X)))
    print("The number of elements in y is "+str(len(y)))
    
    #print X
    #print y

    mean_tpr = 0.0
    mean_fpr = numpy.linspace(0, 1, 100)

    #colors = cycle(['cyan', 'indigo', 'seagreen', 'yellow', 'blue', 'darkorange'])
    lw = 2

    i = 0

    all_probas = []
    all_labels = []
    #confirmed that this is going through 10 loops as expected
    #confirmed that probas is only returning 1 or 0 rather than other confidences
    for (train, test) in cv.split(X, y):
        classifier.fit(X[train], [y[j] for j in train])
        probas_=classifier.predict_proba(X[test])

        all_probas.extend(probas_[:, 1])
        all_labels.extend([y[m] for m in test])

        #print probas_[:100]
        fpr, tpr, thresholds = roc_curve([y[k] for k in test], probas_[:, 1])
        mean_tpr += interp(mean_fpr, fpr, tpr)
        mean_tpr[0] = 0.0
        roc_auc = auc(fpr, tpr)
        #plt.plot(fpr, tpr, lw=lw,label='ROC fold %d (area = %0.2f)' % (i, roc_auc))
        i += 1

    #print all_labels
    #print all_probas

    psb_precision,psb_recall,psb_thresholds = precision_recall_curve(all_labels,all_probas)
    psb_fpr,psb_tpr,psb_thresh_auc = roc_curve(all_labels,all_probas)
    psb_roc_auc_score = roc_auc_score(all_labels,all_probas)

    plt.plot([0, 1], [0, 1], linestyle='--', lw=lw, color='k')



    mean_tpr /= float(cv.get_n_splits(X, y))
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    plt.plot(mean_fpr, mean_tpr, color='g', linestyle='--',label='Mean ROC (area = %0.2f)' % mean_auc, lw=lw)

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('EXAMPLE CODE AVG CURVES Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()


    AUPRC = auc(psb_recall,psb_precision)
    plt.plot(psb_recall,psb_precision,label ='auprc = '+str(AUPRC))
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('COMBINE DATASETS Precision Recall Curve')
    plt.legend(loc="lower right")
    plt.show()

    plt.plot(psb_fpr,psb_tpr)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('COMBINE DATASETS ROC Curve')
    plt.legend(loc="lower right")
    plt.show()

    print("out of bag ROC:"+psb_roc_auc_score)
    print("avergae of curves: "+ mean_auc)
    print("area under P-R curve"+AUPRC)
    return

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
