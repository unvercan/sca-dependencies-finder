# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 11:02:10 2018

@author: Ünver Can Ünlü
"""

# dependency class
class Dependency:
    def __init__(self, file, element, attribute, path):
        self.file = file
        self.element = element
        self.attribute = attribute
        self.path = path
        
    # convert object to dictionary
    def as_dict(self):
        return dict(file=self.file, element=self.element, attribute=self.attribute, path=self.path)
