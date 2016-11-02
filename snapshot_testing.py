from classes import *
from datetime import datetime, date, time

def main():
    new_bug = bug()
    new_bug.actual_time = 3.5
    new_bug.creation_time = datetime(2016, 10, 1, 12, 30)
    new_bug.priority = 'P3'

    change1 = change()
    change1.field_name = 'actual_time'
    change1.removed = '0.0'
    change1.added = '3.5'

    history1 = history()
    history1.changes.append(change1)
    history1.when = datetime(2016, 10, 30, 12, 30)

    change2 = change()
    change2.field_name = 'priority'
    change2.removed = 'P1'
    change2.added = 'P3'

    history2 = history()
    history2.changes.append(change2)
    history2.when = datetime(2016, 10, 5, 12, 30)

    new_bug.histories.append(history1)
    new_bug.histories.append(history2)

    snapshot = new_bug.bug_snapshot()
    print(snapshot.priority)

    return

if __name__ == "__main__":
    main()