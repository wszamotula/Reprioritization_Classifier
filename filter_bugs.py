from datetime import datetime, timedelta
from bug_classes import Bugs, Bug, conv_dt

def main(bugs, age=7):
    """
    Filter a collection of bugs down to a collection of relevant snapshots
    :param bugs: Bugs
    :param age: int
    :return: Bugs
    """
    filtered_bugs = Bugs()
    # un-pickle bugs? Take bugs from previous step?

    for id, bug in bugs.bugs.items():
        if bug.resolution != 'FIXED':
            continue
        if datetime.today() - conv_dt(bug.creation_time) < timedelta(days=age):
            continue
        if len(bug.comments) < 5:
            continue

        snapshot = bug.bug_snapshot(age)
        if len(snapshot.comments) < 5:
            continue
        # Should we exclude bugs that were resolved at this point?
        if bug.resolution == 'FIXED':
            continue

        filtered_bugs.bugs[snapshot.id] = snapshot

    return filtered_bugs