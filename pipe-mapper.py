#!/usr/bin/env python

import os
import json, sys
from commonutils import verbose_print, parse_arguments, output_result

def get_last_line(output):
	last_line = output.readline()
	for line in output:
		print(line) # will print if input script has -v option set
		last_line = line
	return last_line

def decode_json(json_line):
	try:
		return json.loads(json_line)
	except ValueError as value_error:
		sys.stderr.write("Error : could not decode JSON from line : " + json_line), value_error
		sys.exit(2)

if __name__ == '__main__':
	
	# 1. Get output from piped script from stdin
	lastInputLine = get_last_line(sys.stdin)
	inputData = decode_json(lastInputLine)
	
	# 2. Parse command line options and arguments (script to call is all non-opt arguments)
	command, optionsDict, remainingArguments = parse_arguments(["map"], ["v","h"], ["verbose","help"], ["o",], ["output",]) # handle all facebook-scrap.py options
	outputScriptCall = " ".join(remainingArguments)
	
	# 3. Set output to stdout so it can be processed
	outputScriptCall += " --output=stdout"
	
	# 4. Grab option values and pass them to output script (override any specified output for the output script)
	for long_opt, arg in optionsDict.iteritems():
		if long_opt != "output":
			if type(arg) == type(True):
				if arg:
					outputScriptCall += " --" + long_opt
			else:
				outputScriptCall += " --" + long_opt + "=" + arg
	
	# 5. Execute script for each one of the items in the array dict of each item of the input
	verbose_print("mapping input to " + outputScriptCall + "...")
	# TODO : use generic mapping
	mappingNameKey = "searched_user"
	mappingDataKey = "matching_users_divs_filenames"
	mappingParsedKey = "matching_users_attributes"
	for searchedItemResults in inputData:
		# get the name
		searchedItemName = searchedItemResults[mappingNameKey]
		# get the HTML files macthing this user
		searchedItemHtmlResults = searchedItemResults[mappingDataKey]
		# create the command to run the python script by flattening the array - scrap data from this HTML block
		python_command = "python " + outputScriptCall + " " + " ".join(map(str, searchedItemHtmlResults))
		# run the command get the data
		# searchedItemParsedResults = os.popen(python_command).readlines()
		searchedItemParsedResults = get_last_line(os.popen(python_command))
		# add parsed data to results dictionnary
		# searchedItemResults[mappingParsedKey] = json.loads(searchedItemParsedResults)
		searchedItemResults[mappingParsedKey] = decode_json(searchedItemParsedResults)
		# removes HTML files from the results dictionnary
		searchedItemResults.pop(mappingDataKey, None)
	
	# 6. Output results
	output_result(inputData, "pretty")