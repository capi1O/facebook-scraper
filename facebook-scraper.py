#!/usr/bin/env python

from facepy import GraphAPI
import json
import getopt, sys
import os

# 0. Get input data (name, JSON file or csv file)
try:
	opts, args = getopt.getopt(sys.argv[1:], "hjc:v", ["help", "json=", "csv="])
except getopt.GetoptError as err:
	print(err) # will print something like "option -a not recognized"
	usage()
	sys.exit(2)
input_file = False
verbose = False
names=[]
for option, arg in opts:
	if option in ("-h", "--help"):
		print "help needed"
	elif option in ("-j", "--json"):
		print "JSON file provided"
		input_file = True
		# json_file_path = os.getcwd() + '/' + arg
		# print json_file_path
		with open(arg) as json_data:
			people_json = json.load(json_data)
		for person in people_json:
			names.append(person['name'])
	elif option in ("-c", "--csv"):
		print "CSV file provided"
		input_file = True
	    #TODO : loads CSV file 
	elif option == "-v":
		verbose = True
	else:
		assert False, "unhandled option"
# if no JSON or CSV options provided, get non-option arguments if provided (names)
if input_file == False:
	print "no file provided, reading non-option arguments as names"
	print args
	names=args

# 1. Get Facebook access token (using Facebook app fassbk-scraper)
user_token = "place-your-token-here"
# init facepy graph API
graph = GraphAPI(user_token)

# 2. Get Facebook users matching name(s) provided
for name in names:
	encoded_name = name.encode('utf8')
	print encoded_name
	result = graph.get('search?q={' + encoded_name + '}&type=user')
	data = result['data'] #decode('utf8')
	print json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False, encoding="utf-8")
