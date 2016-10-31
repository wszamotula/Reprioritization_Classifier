class bugs:
    'Collection of bugs'

    def __init__(self):
        bugs = []

class bug:
    'Details on a bug'

    def __init__(self):
        actual_time = 0.0
        alias = []
        assigned_to = ''
        # assigned_to_detail = '' user object
        blocks = []
        bug_id = 0
        cc = []
        # cc_detail = [] user object
        classification = ''
        component = ''
        creation_time = ''
        creator = ''
        # creator_detail = '' user object
        deadline = ''
        depends_on = []
        dupe_of = 0
        estimated_time = 0.0
        # flags = [] flag object
        groups = []
        histories = []
        is_cc_accessible = False
        is_confirmed = False
        is_open = False
        is_creator_accessible = False
        keywords = []
        last_change_time = ''
        op_sys = ''
        platform = ''
        priority = ''
        product = ''
        qa_contact = ''
        # qa_contact_detail = '' user object
        remaining_time = 0.0
        resolution = ''
        see_also = []
        severity = ''
        status = ''
        summary = ''
        target_milestone = ''
        update_token = ''
        url = ''
        version = ''
        whiteboard = ''

    def bug_snapshot(self, age=7):
        snapshot = bug()
        # revert changes to create snapshot at age
        return snapshot

class history:
    'history of a change for a particular bug'

    def __init__(self):
        when = ''
        who = ''
        changes = []


class change:
    'a change made to a particular bug'

    def __init(self):
        field_name = ''
        removed = ''
        added = ''
        attachment_id = 0