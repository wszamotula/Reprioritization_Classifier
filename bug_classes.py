import copy
from datetime import datetime, timedelta


class Bugs:
    """Collection of bugs"""

    def __init__(self):
        self.bugs = []

    def append(self, bug):
        """
        Add a new bug to the collection
        :type bug: bug
        """
        self.bugs.append(bug)
        return


class Bug:
    """Details on a bug"""
    # TODO: We might want to change all these time fields to python time objects

    def __init__(self):
        self.actual_time = 0.0
        self.alias = []
        self.assigned_to = ''
        # assigned_to_detail = '' user object
        self.blocks = []
        self.id = 0
        self.cc = []
        # cc_detail = [] user object
        self.classification = ''
        self.component = ''
        self.comments = []
        self.creation_time = datetime.now()
        self.creator = ''
        # creator_detail = '' user object
        self.deadline = ''
        self.depends_on = []
        self.dupe_of = 0
        self.estimated_time = 0.0
        # flags = [] flag object
        self.groups = []
        self.histories = []
        self.is_cc_accessible = None
        self.is_confirmed = None
        self.is_open = None
        self.is_creator_accessible = None
        self.keywords = []
        self.last_change_time = ''
        self.op_sys = ''
        self.platform = ''
        self.priority = ''
        self.product = ''
        self.qa_contact = ''
        # qa_contact_detail = '' user object
        self.remaining_time = 0.0
        self.resolution = ''
        self.see_also = []
        self.severity = ''
        self.status = ''
        self.summary = ''
        self.target_milestone = ''
        self.update_token = ''
        self.url = ''
        self.version = ''
        self.whiteboard = ''

    def bug_snapshot(self, age=7):
        """
        revert changes to create snapshot at age
        :type age: int
        """
        snapshot = copy.deepcopy(self)
        new_comments = []

        for history in self.histories:
            # Assuming histories are ordered most recent first
            # TODO: Verify that this assumption is correct
            if history.when - self.creation_time < timedelta(days=age):
                break
            for change in history.changes:
                snapshot.revert_change(change)

        for comment in self.comments:
            if comment.creation_time - self.creation_time < timedelta(days=age):
                new_comments.append(copy.deepcopy(comment))
        snapshot.comments = new_comments

        return snapshot

    def revert_change(change):
        """
        Revert a single change made to a bug
        :type change: change
        """
        # TODO: Make sure this works for list types as well
        exec('self.' + change.field_name + ' = ' + change.removed)
        return


class History:
    """history of a change to a particular bug"""

    def __init__(self):
        self.when = datetime.now()
        self.who = ''
        self.changes = []


class Change:
    """a change made to a particular bug"""

    def __init__(self):
        self.field_name = ''
        self.removed = ''
        self.added = ''
        self.attachment_id = 0


class Comment:
    """A comment linked to a bug"""

    def __init__(self):
        self.attachment_id = ''
        self.author = ''
        self.bug_id = 0
        self.creation_time = datetime.now()
        self.creator = ''
        self.id = 0
        self.is_private = None
        self.raw_text = ''
        self.tags = []
        self.text = ''
        self.time = ''