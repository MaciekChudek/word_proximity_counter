#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from characterLocatorVariables import *

def set_vars(job_vars): #sets global variables for a given run. Cludgy amendment to old single-run script.
	global focal_characters
	global comparison_characters 
	global comparison_sets
	global all_basic_characters
	global all_comparions_and_sets
	global all_set_characters
	
	focal_characters = job_vars['focal']
	comparison_characters = job_vars['comparison']
	comparison_sets = job_vars['compare_sets']
	
	#set up some combined sets
	all_basic_characters = focal_characters + comparison_characters
	all_comparions_and_sets = comparison_characters + tuple([k for k in comparison_sets.keys() ]) + tuple(['any_comparison'])
	all_set_characters = tuple( [item for sublist in [v for k, v in comparison_sets.items() ] for item in sublist] ) #probably not the most elegant way to merge lists and dicts in python, but it does the trick


def construct_database(job_name):
	output_file = open(directory_in_which_to_save_data+job_name+"_"+output_filename, mode='w', buffering=1, encoding='utf-8') #truncate the database if it exists, use line buffering, utf-8 encoding
	print(database_header, file=output_file) #initialise the database header
	n = len(ancient_text_files)
	i=0
	for text_name, file_name in ancient_text_files.items():
		i = i+1
		print_progress(i,n)
		with open(file_name, encoding='utf-8') as f:
			character_positions = getCharacterPositions(f)
			f.close() #we don't need to text now that we know the positions of all the relevant characters			
			append_to_database(output_file, text_name, character_positions) #append the data to our database
	output_file.close()

def print_progress(i,n):
	progress = '\r Progress: ' + str(i) + '/' + str(n) + ' files processed \r'
	#sys.stdout.write(progress)
	#sys.stdout.flush()
	print(progress, end='')


def getCharacterPositions(openedFile): #Constructs, for each targetCharacter, a monotonically ordered list of the positions at which it occurs in this file.
	j = 0 #an iterator to keep track of our potition in the file
	character_positions = {} # a dictionary, so that we can look up each target character's list
	for i in all_basic_characters:
		character_positions[i] = [];	#now we have an empty list of potential locations for each focal and comparison character
	for i in comparison_sets.keys():
		character_positions[i] = [];	#and one list for each comparison set
	while True:
		c = openedFile.read(1) #we read the entire file one character at at time		
		if not c: #we've hit the end of the file
			break
		if (c in characters_to_ignore):
			continue #only continue (i.e., increment the count, etc) if we aren't ignoring this character
		j = j+1
		if(c in all_basic_characters): #if the current character is one of our target characters, we add its position to our list
			character_positions[c].append(j);
			continue #don't process sets if focal found
		found = False #assuming mutually exclusive sets, no need to keep looping through characters once we find a match
		for set_name, set_values in comparison_sets.items():
			if (not found and c in set_values):
				character_positions[set_name].append(j);	# we append the location to the set, ignoring which particular character it is
				found = True
		character_positions['any_comparison'] =  construct_set([character_positions[y] for y in comparison_characters])
	return character_positions;

def append_to_database(output_file, text_name, character_positions):
	for focal_char in focal_characters:		
		for pos in character_positions[focal_char]:
			for other_char in all_comparions_and_sets:
				if focal_char != other_char: #no point comparing a character with itself
					other_positions = character_positions[other_char]
					print_row(output_file, text_name, focal_char,pos,other_char,other_positions)
			other_focals = [x for x in focal_characters if x is not focal_char]
			other_focals_pos = construct_set([character_positions[y] for y in other_focals])
			print_row(output_file, text_name, focal_char,pos,'any_focal',other_focals_pos)
			

def construct_set(subsets):
		#merge the subsets into one list and sort it
		return(sorted([val for subset in subsets for val in subset]))
		

def print_row(output_file, text_name, focal_char,pos,other_char, other_positions):
	before_and_after_postions = get_nearest_positions(pos,other_positions) #returns the nearest ``other_characters'' to this focal position; ordered: nearest_before, then nearest_after					
	print(database_row.format(text=text_name, focal_character=focal_char, position=pos, other_character=other_char, forward=before_and_after_postions[0], backward=before_and_after_postions[1]), file=output_file) #save count

def get_nearest_positions(focal_pos,char_positions): #IMPORANT NOTE: relies on monotonic ordering, which is assured by how we create the lists
	if len(char_positions) == 0:
		return (-1,-1) #a special case, no characters
	for i in range(len(char_positions)):
		if (char_positions[i] > focal_pos): #we've hit the first instance of an ``other character'' that occurs after the focal postion
			if i == 0: #a specail case, there are no instance before
				return (-1, char_positions[i]- focal_pos)
			else:
				return (focal_pos - char_positions[i-1], char_positions[i] - focal_pos) #otherwise we count the distances			
	return(focal_pos - char_positions[len(char_positions)-1], -1) #special case, the loop ended so there werne't any instances after the focal postion
