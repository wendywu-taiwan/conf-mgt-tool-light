class SyncUpAction:
    def __init__(self, action_list):
        if any("create" in s for s in action_list):
            self.create_ruleset = True
        else:
            self.create_ruleset = False

        if any("update" in s for s in action_list):
            self.update_ruleset = True
        else:
            self.update_ruleset = False

        if any("delete" in s for s in action_list):
            self.delete_ruleset = True
        else:
            self.delete_ruleset = False
