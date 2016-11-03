from bug_classes import *
from datetime import datetime


def main():
    new_bug = Bug()
    new_bug.actual_time = 3.5
    new_bug.creation_time = datetime(2016, 10, 1, 12, 30)
    new_bug.priority = 'P3'

    change1 = Change()
    change1.field_name = 'actual_time'
    change1.removed = '0.0'
    change1.added = '3.5'

    history1 = History()
    history1.changes.append(change1)
    history1.when = datetime(2016, 10, 30, 12, 30)

    change2 = Change()
    change2.field_name = 'priority'
    change2.removed = 'P1'
    change2.added = 'P3'

    history2 = History()
    history2.changes.append(change2)
    history2.when = datetime(2016, 10, 5, 12, 30)

    new_bug.histories.append(history1)
    new_bug.histories.append(history2)

    comment1 = Comment()
    comment1.creation_time = datetime(2016, 10, 30, 12, 30)
    comment1.text = 'I should not stay'

    comment2 = Comment()
    comment2.creation_time = datetime(2016, 10, 5, 12, 30)
    comment2.text = 'I should stay'

    new_bug.comments.append(comment1)
    new_bug.comments.append(comment2)

    snapshot = new_bug.bug_snapshot()
    print('Actual time of snapshot: {}'.format(snapshot.actual_time))
    print('Number of comments in snapshot: {}'.format(len(snapshot.comments)))

    return


if __name__ == "__main__":
    main()
