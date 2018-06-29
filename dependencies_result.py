# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 11:02:10 2018

@author: Ünver Can Ünlü
"""

# dependencies result class
class DependenciesResult:
    def __init__(self, type, dependencies):
        self.type = type
        self.dependencies = dependencies
    
    # convert object to dictionary
    def as_dict(self):
        return dict(type=self.type, dependencies=self.dependencies)
