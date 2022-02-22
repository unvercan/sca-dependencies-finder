# -*- coding: utf-8 -*-

# dependencies result class
class DependenciesResult(object):
    def __init__(self, category, dependencies):
        self.category = category
        self.dependencies = dependencies

    # convert object to dictionary
    def convert_to_dictionary(self):
        return dict(type=self.category, dependencies=self.dependencies)
