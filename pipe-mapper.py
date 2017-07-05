#!/usr/bin/env python

import os
import json, sys
from commonutils import verbose_print, parse_arguments, output_result

if __name__ == '__main__':
	# 0.A. Get results from stdin as a python array
	try:
		inputData = json.loads(sys.stdin.readline())
	except ValueError as value_error:
		sys.stderr.write("Error : incorrect input, could not decode JSON"), value_error
		sys.exit(2)
	# 0.B. Parse command line options and arguments
	command, optionsDict, remainingArguments = parse_arguments(["map"], ["v","h"], ["verbose","help"], ["o","c"], ["output","command"])
	# 0C. Grab option values or use default if none provided
	helpOpt = optionsDict.get("help", False)
	# jsonInput = optionsDict["json"] : None
	outputScript = optionsDict.get("output", "facebook-scrap.py")
	outputScriptCommand = optionsDict.get("command", "user-search")
	# keys
	mappingNameKey = optionsDict.get("mapping_name_key", "searched_user")
	mappingDataKey = optionsDict.get("mapping_data_key", "matching_users_divs_filenames")
	mappingParsedKey = optionsDict.get("mapping_parsed_key", "matching_users_attributes")
	
	# 1A. Execute script for each one of the items in the array dict of each item of the input
	if command is "map":
		verbose_print("mapping input to " + outputScript + "...")
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