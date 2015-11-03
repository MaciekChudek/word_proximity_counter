#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#notes: 
	#If you want to do `per-sentence' analysis later, I recommend including your sentence delimiter character in the target_characters array, and making sure it also occurs at the beging and end of your file.
	
	#Currently just loops linearly through all the positions of characters to find the nearest to a position. Binary search would be more efficient.

#imports
#import glob # for getting filenames
import os, fnmatch # for getting filenames

directory_in_which_to_save_data = './data/' #the place where we keep our ancient texts, don't forget trailing slash
directory_of_ancient_texts = './texts/' #the place where we keep our ancient texts, don't forget trailing slash
filename_extension = '.txt' #the filename extension we've put on all our anicent texts (optional)

#ancient_text_files = glob.glob(directory_of_ancient_texts + '*' +filename_extension) #a list of the files containing the texts, doesn't recurseinto subdirectories.
ancient_text_files = dict(#a list of the files containing the texts, found recursively in subdirectories. Removes absolute path and extension.
	(
		#os.path.join(f.replace(filename_extension,'')), 
		os.path.join(dirpath.replace(directory_of_ancient_texts,''), f.replace(filename_extension,'')), 
		os.path.join(dirpath, f)
	)
    for dirpath, dirnames, files in os.walk(directory_of_ancient_texts)
    for f in fnmatch.filter(files, '*' + filename_extension))

output_filename = "database.csv" #the file we'll write our computed data to
database_header = "text, focal_character, position, other_character, forward, backward" #the csv table header
database_row = "{text}, {focal_character}, {position}, {other_character}, {forward}, {backward}" #the format of each database row
characters_to_ignore = (' ','：','「','」','，','\n','\r','#','@','；') # do you want to ignore spaces or line breaks? add any characters here that shouldn't be counted


# Lists of characters to trawl for

body_organs = ('心','肺','脈','肝','脾','腸','腎','胃','腹','耳','目','口','氣')
body_terms = ('身','形','體')
common_characters_left_list = ('君','父','兄','天','日','陰','東','先','生','入','內','無','大','上','多','人','鳥','魚','水','城','車','耳','目')
common_characters_right_list = ('臣','子','弟','地','月','陽','西','後','死','出','外','有','小','下','少','走','飛','游','流','門','輪','聽','見')
comparison_sets = { # a dictionary of sets of characters, only the nearest of which is relevant.
	'emo': ('安','好','情','乐','喜','急','忙','怀','恐','惊','愿','爱','怒','恶','苦','疾','怕','欢','感','忧','萧','恨','惧','怨','患','悦','哀','宽','虑','仇','惜','痛','遥','悲','怜','烦','畏','愁','慌','慕','戚','忌','悄','悔','嫌','焦','羞','闷','激','欣','恼','澹','厌','恤','寂','恚','愤','惨','惶','恋','骇','惭','恍','羡','怯','衷','悠','怼','惮','恳','忿','疼','畅','僖','忆','慨','妒','悼','恸','徊','忻','栗','禧','漠','怂','兢','嫉','怅','嗔','歆','憾','徘','懊','怡','瞿','竦','厄','恺','诧','逍','怖','怏','憎','窘','恻','悯','顼','愉','怿','惕','悸','愠','慑','懔'), 
	'cog': ('知','明','意','学','想','思','理','教','计','志','觉','记','图','疑','察','略','算','识','认','检','智','忘','误','惑','醒','验','慎','惺','悟','迷','晕','辨','聪','睿','敏','痴','拟','伺','慧','呆','混','搜','谟','猜','窍','勘','析','译','尖','铨','狡','懂','懋','揆','伶','揣','阐','忖','睬','俐'),
	'delim': ('《','》','。','？','！') 
	}
jobs = {#an array of variables for each the databases we'll construct
	'body' : { 
		'focal' : body_organs,
		'comparison' : body_terms,
		'compare_sets' : comparison_sets
		}#,
	#'common' : {
		#'focal' : common_characters_left_list,
		#'comparison' : common_characters_right_list,
		#'compare_sets' : {}
		#}
	}
