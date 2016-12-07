import json
import os
from bug_classes import Bug, Bugs, History, Change, Comment
import pickle
from collections import defaultdict

def buildBugObjects():
    print_Counter=0
    directory = 'bugs'
    main_bug_directory = 'main_bug_file'
    main_bug_file_prefix = 'main_bug_file'
    history_prefix = 'history_'
    comment_prefix = 'comment_'
    output_file = 'bugsFile'
    num_Files = 4
    fileNameArr = []
    jsonDictArr = []
    subdir_Arr = ['Part1','Part2','Part3','Part4','Part5']
    DEBUG = False
    resolutionDict = defaultdict(int)
    priorityDict = defaultdict(int)
    commentTotalDict = defaultdict(int)
    severityDict = defaultdict(int)

    #build list of files
    for idx in range(num_Files):
        fileNameArr.append(os.path.join(main_bug_directory,main_bug_file_prefix+str(idx+1)+".txt"))

    print fileNameArr
    #create collection of bugs
    allBugs = Bugs()

    #open main JSON file containing all bugs
    for currFileName in fileNameArr:
        with open(os.path.join(directory,currFileName)) as f:
            print "reading file "+currFileName
            read_data = f.read()
            curr_json_dict = json.loads(read_data)
            jsonDictArr.append(curr_json_dict)

    #get string name all the members of the classes                                                                           
    members = [attr for attr in dir(Bug()) if not callable(attr) and not attr.startswith("__")]
    comment_members = [attr for attr in dir(Comment()) if not callable(attr) and not attr.startswith("__")]
    history_members = [attr for attr in dir(History()) if not callable(attr) and not attr.startswith("__")]
    change_members = [attr for attr in dir(Change()) if not callable(attr) and not attr.startswith("__")]

    #loop over all the bugs
    for currJSONDict in jsonDictArr:
        for curr_bug_dict in currJSONDict['bugs']:
            curr_bug = Bug()
            #loop over all member names and determine if populated if so set
            for member in members:
                if member in curr_bug_dict.keys():
                    setattr(curr_bug,member,curr_bug_dict[member])
    
            #if we could not set the bug id there is a problem and we should not add bug to collection
            #change break to continue
            curr_bug_id = curr_bug.id
            if not curr_bug_id > 0:
                continue

            #handle potential duplicates of bugs
            if curr_bug_id in allBugs.bugs.keys():
                continue

            #open the associated comment file if it exists
            gotComment = 0
            for curr_directory in subdir_Arr:
                comment_fname = os.path.join(directory,curr_directory,comment_prefix+str(curr_bug_id)+'.txt')
                if os.path.isfile(comment_fname) and (gotComment == 0):
                    gotComment = 1
                    with open(comment_fname) as f:
                        comment_read_data = f.read()
                        comment_json_dict = json.loads(comment_read_data)
                    for curr_comment_dict in  comment_json_dict['bugs'][str(curr_bug_id)]['comments']:
                        curr_comment = Comment()
                        for comment_member in comment_members:
                            if comment_member in curr_comment_dict.keys():
                                setattr(curr_comment,comment_member,curr_comment_dict[comment_member])                        
                        curr_bug.comments.append(curr_comment)

            #open the associated history file if it exists
            gotHistory = 0
            for curr_directory in subdir_Arr:
                history_fname = os.path.join(directory,curr_directory,history_prefix+str(curr_bug_id)+'.txt')
                if os.path.isfile(history_fname) and (gotHistory==0):
                    gotHistory=1
                    with open(history_fname) as f:
                        history_read_data = f.read()
                        history_json_dict = json.loads(history_read_data)
                    for curr_history_dict in history_json_dict['bugs'][0]['history']:
                        curr_history = History()
                        if 'when' in curr_history_dict.keys():
                            curr_history.when = curr_history_dict['when']
                        if 'who' in curr_history_dict.keys():
                            curr_history.who = curr_history_dict['who']
                        if 'changes' in curr_history_dict.keys():
                            for curr_change_dict in curr_history_dict['changes']:
                                curr_change = Change()
                                for change_member in change_members:
                                    if change_member in curr_change_dict.keys():
                                        setattr(curr_change,change_member,curr_change_dict[change_member])
                                curr_history.changes.append(curr_change)
                        curr_bug.histories.append(curr_history)

            allBugs.bugs[curr_bug.id] = curr_bug
            if curr_bug.resolution != '':
                resolutionDict[curr_bug.resolution] = resolutionDict[curr_bug.resolution] + 1
            else:
                resolutionDict['NULL'] = resolutionDict['NULL'] + 1
                if print_Counter < 5:
                    print("ID: "+str(curr_bug.id))
                    print_Counter = print_Counter + 1

            #track priority totals
            if curr_bug.priority != '':
                priorityDict[curr_bug.priority] = priorityDict[curr_bug.priority] + 1
            else:
                priorityDict['NULL'] = priorityDict['NULL']+1
            #track comment totals
            commentTotalDict[len(curr_bug.comments)] = commentTotalDict[len(curr_bug.comments)]+1
            #track severity totals
            if curr_bug.severity != '':
                severityDict[curr_bug.severity] = severityDict[curr_bug.severity] + 1
            else:
                severityDict['NULL'] = severityDict['NULL']+1


            if DEBUG == True:
                print('Added bug {}'.format(curr_bug_id))

    #Pickle Bugs
        print("Total bugs after parsing file:"+str(len(allBugs.bugs.keys())))
        with open(os.path.join(directory,output_file),'wb') as f:
            pickle.dump(allBugs,f)
    
    for key in resolutionDict.keys():
        print(key + ": "+str(resolutionDict[key]))

    for key in priorityDict.keys():
        print(key + ": "+str(priorityDict[key]))    

    for key in commentTotalDict.keys():
        print(str(key) + ": "+str(commentTotalDict[key]))

    for key in severityDict.keys():
        print(str(key) + ": "+str(severityDict[key]))    

    ##DEBUGGING SCRIPT TO PRINT FIRST BUG
    if DEBUG == True:
        for member in members:
            print(member+": "+str(getattr(allBugs.bugs[656504],member)))
        # print("PRINTING COMMENTS")
        # for curr_comment in allBugs.bugs[656504].comments:
        #     print("------")
        #     for comment_member in comment_members:
        #         print(comment_member + ": " +str(getattr(curr_comment,comment_member)))
        print("PRINTING HISTORY")
        for curr_history in allBugs.bugs[656504].histories:
            print("-------")
            print("who: " + str(curr_history.who))
            print("when: "+ str(curr_history.when))
            for curr_change in curr_history.changes:
                for change_member in change_members:
                    print(change_member+": " +str(getattr(curr_change,change_member)))

        snapshot = allBugs.bugs[656504].bug_snapshot()
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        for member in members:
            print(member+": "+str(getattr(snapshot,member)))

    return allBugs

if __name__ == "__main__":
    buildBugObjects()
