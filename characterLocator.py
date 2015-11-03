#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys #let's just make sure we're in the right directory
root_dir = '/home/maciek/Work/projects/researching/Xin_2/version3'
os.chdir(root_dir)
sys.path.append(root_dir + '/characterLocator')

from characterLocatorVariables import *
from characterLocatorFunctions import *


#and now we actually run the script...
for job_name, job_vars in jobs.items():
	set_vars(job_vars)
	construct_database(job_name) 
