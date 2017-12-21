import json


class MenuList(object):

    def __init__(self, data):
        self.root_id = data
        self.children = []

    def add_child(self, obj):
        if type(obj) is list:
            self.children = list(set(self.children + obj))
        elif obj not in self.children:
            self.children.append(obj)

    def is_valid(self):
        return self.root_id in self.children

    def is_in_children(self, id):
        return id in self.children

    def is_mergeable(self, menulist):
        return self.is_in_children(menulist.root_id) or self.root_id == menulist.root_id or menulist.is_in_children(self.root_id)

    def merge_menulist(self, menulist):
        if self.is_mergeable(menulist):
            self.add_child(menulist.children)
            if menulist.is_in_children(self.root_id):
                self.root_id = menulist.root_id
        return self

    def get_format(self):
        data = {}
        data['root_id'] = self.root_id
        data['children'] = self.children
        return json.dumps(data)
