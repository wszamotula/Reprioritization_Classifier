from datetime import datetime, timedelta
from bug_classes import Bugs, Bug, conv_dt


def filtered_snapshots(bugs):
    """
    Filter a collection of bugs down to a collection of relevant snapshots for
    :param bugs: Bugs
    :param age: int
    :return: Bugs
    """
    filtered_snapshots = Bugs()
    # un-pickle bugs? Take bugs from previous step?

    for id, bug in bugs.bugs.items():
        # if conv_dt(bug.last_change_time) > cutoff_datetime:
        #    continue
        if len(bug.comments) < 5:
            continue
        # if bug.status != 'RESOLVED':
        #    continue

        snapshot = bug.bug_snapshot()
        # We might want to try modifying the comment or age numberss
        if len(snapshot.comments) < 3:
            continue
        if bug.resolution != '':
            continue

        filtered_snapshots.bugs[snapshot.id] = snapshot
        print('Added snapshot {}'.format(snapshot.id))

    return filtered_snapshots


def scikit_input(bugs, snapshots):
    text = []
    priorities = []
    target = []

    for id, snapshot in snapshots.bugs.items():
        priorities.append(snapshot.priority)
        target.append(int(bugs.bugs[id].priority != snapshot.priority))

        bug_string = snapshot.summary
        for comment in snapshot.comments:
            bug_string += ' ' + comment.text
        text.append(bug_string)

    return text, priorities, target