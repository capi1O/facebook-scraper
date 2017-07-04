#!/usr/bin/env python

import getopt, sys
import os
import json
from commonutils import output_result

def get_input_data(sys_args):
	# Get results from stdin as a python array
	input_data = json.loads(sys.stdin.readline())

	# Get Arguments
	try:
		opts, non_opts_args = getopt.gnu_getopt(sys_args, "hvo:c:", ["help", "verbose", "output=", "command="])
		
		# default optional arguments
		verbose = False
		input_type = "json"
		output_script = "facebook-scrap.py"
		output_script_command = "user-search"
		
		# keys
		mapping_name_key = "searched_user"
		mapping_data_key = "matching_users_divs_filenames"
		mapping_parsed_key = "matching_users_attributes"
		#TODO : use generic keys
		
		for option, arg in opts:
			if option in ("-h", "--help"):
				print "help needed"
				# TODO
			elif option in ("-v", "--verbose"):
				verbose = True
			elif option in ("-o", "--output"):
				output_script = arg
			elif option in ("-c", "--command"):
				output_script_command = arg
			else:
				assert False, "unhandled option : " + option
				
		if input_type is "json":
			# reading all (remaining) non-option arguments as strings 
			# print "remaining non-option arguments : '" + ", ".join(map(str, non_opts_args)) + "'"
			#non_opts_args
			pass
		return [input_data, output_script, output_script_command, mapping_name_key, mapping_data_key, mapping_parsed_key]
	except getopt.GetoptError as err:
		sys.stderr.write(err)
		usage()
		sys.exit(2)

if __name__ == '__main__':
		
	# 0. Get array as input from input script
	inputData, outputScript, outputScriptCommand, mappingNameKey, mappingDataKey, mappingParsedKey = get_input_data(sys.argv[1:])
	
	# 1. Get output script name
	for searchedItemResults in inputData:
		# get the name
		searchedItemName = searchedItemResults[mappingNameKey]
		# get the HTML files macthing this user
		searchedItemHtmlResults = searchedItemResults[mappingDataKey]
		# create the command to run the python script by flattening the array - scrap data from this HTML block
		python_command = "python " + outputScript + " " + outputScriptCommand + " -o stdout " + " ".join(map(str, searchedItemHtmlResults))
		# run the command get the data
		searchedItemParsedResults = os.popen(python_command).read()
		# add parsed data to results dictionnary
		searchedItemResults[mappingParsedKey] = json.loads(searchedItemParsedResults)
		# removes HTML files from the results dictionnary
		searchedItemResults.pop(mappingDataKey, None)
	
	# 2. Output results
	output_result(inputData, "pretty")