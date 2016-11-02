class bugs:
    'Collection of bugs'

    def __init__(self):
        self.bugs = []


    def append(self, bug):
        """
        Add a new bug to the collection
        :type bug: bug
        """
        self.bugs.append(bug)
        return


class bug:
    'Details on a bug'

    def __init__(self):
        self.actual_time = 0.0
        self.alias = []
        self.assigned_to = ''
        # assigned_to_detail = '' user object
        self.blocks = []
        self.bug_id = 0
        self.cc = []
        # cc_detail = [] user object
        self.classification = ''
        self.component = ''
        self.creation_time = ''
        self.creator = ''
        # creator_detail = '' user object
        self.deadline = ''
        self.depends_on = []
        self.dupe_of = 0
        self.estimated_time = 0.0
        # flags = [] flag object
        self.groups = []
        self.histories = []
        self.is_cc_accessible = False
        self.is_confirmed = False
        self.is_open = False
        self.is_creator_accessible = False
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
        snapshot = bug()
        # Loop through histories of the bug (assuming histories are stored most recent first)
        # If change occurred less than age days after bug was created, break loop
        # For each change in the history, revert change
        return snapshot

    def revert_change(self, change):
        """
        Revert a single change made to a bug
        :type change: change
        """
        # TODO: Make sure this works for array types as well
        exec('self.' + change.field_name + ' = ' + change.removed)
        return

class history:
    'history of a change for a particular bug'

    def __init__(self):
        self.when = ''
        self.who = ''
        self.changes = []


class change:
    'a change made to a particular bug'

    def __init(self):
        self.field_name = ''
        self.removed = ''
        self.added = ''
        self.attachment_id = 0