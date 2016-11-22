import json
import os
from bug_classes import Bug, Bugs, History, Change, Comment
import pickle

def buildBugObjects():
    directory = 'bugs'
    main_bug_file_prefix = 'main_bug_file'
    history_prefix = 'history_'
    comment_prefix = 'comment_'
    output_file = 'bugsFile'
    num_Files = 4
    fileNameArr = []
    jsonDictArr = []
    DEBUG = False

    #build list of files
    for idx in range(num_Files):
        fileNameArr.append(main_bug_file_prefix+str(idx)+".txt")

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
            curr_bug_id = curr_bug.id
            if not curr_bug_id > 0:
                break

            #open the associated comment file if it exists
            comment_fname = os.path.join(directory,comment_prefix+str(curr_bug_id)+'.txt')
            if os.path.isfile(comment_fname):
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
            history_fname = os.path.join(directory,history_prefix+str(curr_bug_id)+'.txt')
            if os.path.isfile(history_fname):
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
            if DEBUG == True:
                print('Added bug {}'.format(curr_bug_id))

    #Pickle Bugs
        print("Total bugs after parsing file:"+str(len(allBugs.bugs.keys())))
        with open(os.path.join(directory,output_file),'wb') as f:
            pickle.dump(allBugs,f)

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

    #return allBugs
    return

if __name__ == "__main__":
    buildBugObjects()
