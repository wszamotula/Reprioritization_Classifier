import pickle
import os

def statsMain():
    directory = ''
    main_bug_pickle = 'bugsFile'

    #Load Bugs from pickled file
    with open(os.path.join(directory,main_bug_pickle),'rb') as f:
        allBugs = pickle.load(f)

    #Run statistical analysis on bugs
    getNumPriorityChange(allBugs)

    return


def getNumPriorityChange(allBugs):
    totalBugCounter=0
    changedPriorityBugCounter=0
    for bugID in allBugs.bugs.keys():
        totalBugCounter=totalBugCounter+1
        priorityChanged = 0
        for currHistory in allBugs.bugs[bugID].histories:
            for currChange in currHistory.changes:
                if (currChange.field_name=="priority") and ("P" in  currChange.removed):
                    priorityChanged = 1
                    print "[ "+str(bugID)+"] OLD: "+currChange.removed
                    print "[ "+str(bugID)+"] NEW: "+currChange.added
        if priorityChanged == 1:
            changedPriorityBugCounter = changedPriorityBugCounter + 1
    print("TOTAL BUG: "+str(totalBugCounter))
    print("CHANGED PRIORTY BUG: "+str(changedPriorityBugCounter))
    return

if __name__ == "__main__":
    statsMain()
