# -*- coding: utf-8 -*-

# dependency class
class Dependency(object):
    def __init__(self, file, element, attribute, path):
        self.file = file
        self.element = element
        self.attribute = attribute
        self.path = path

    # convert object to dictionary
    def convert_to_dictionary(self):
        return dict(file=self.file, element=self.element, attribute=self.attribute, path=self.path)
