#!/usr/bin/env python

import getopt, sys
import os
import re
import bs4
import json

def get_input_data(sys_args):
	input_data = []
	try:
		opts, non_opts_args = getopt.gnu_getopt(sys_args, "hvo:", ["help", "verbose", "output="])
		
		# take the first non-optional argument as the command name
		command = non_opts_args.pop(0)
		#TODO : handle error if 0 non-optional argument
		print "command : '" + command + "'"
		if command not in ["user-search", "profile", "page"]:
			assert False, "unhandled command : " + command
					
		# default optional arguments
		verbose = False
		input_type = "stdin"
		output_type = "stdout"
		
		for option, arg in opts:
			if option in ("-h", "--help"):
				print "help needed"
				# TODO
			elif option in ("-v", "--verbose"):
				verbose = True
			elif option in ("-o", "--output"):
				output_type = arg
				print "output_type : '" + output_type + "'"
				if output_type not in ["stdout", "json", "csv"]:
					assert False, "unhandled output : " + output_type
			else:
				assert False, "unhandled option : " + option

		if input_type is "stdin":
			# reading all (remaining) non-option arguments as strings 
			print "remaining non-option arguments : '" + ", ".join(map(str, non_opts_args)) + "'"
			input_data = non_opts_args
		return [command, input_data, output_type]
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit(2)
		
		
def scrap_user_attributes(user_div_html):
	# 0. Get the HTML data as soup
	user_div = bs4.BeautifulSoup(user_div_html, "html.parser").find("div")
	# 1. Get the FB UID
	data_gt_value = user_div["data-gt"]
	fb_uid_match_string = r'(?<=result_id\\":).*?(?=,\\"sid)'
	fb_uid = re.search(fb_uid_match_string, data_gt_value, flags=re.DOTALL).group(0)				
	# 2. Get the customized
	customized_url_link_match_string = r'{"unit_id_click_type":"graph_search_results_item_in_module_tapped"'
	link_matches = user_div.find_all("a", attrs={"data-sigil": re.compile("m-graph-search-result-page-click-target"), "data-store": re.compile(customized_url_link_match_string)})
	for link_match in link_matches:
		href_value = link_match["href"]
		fb_customized_url_match_string = r'(?<=\/).*?(?=\?refid=)'
		try:
			fb_customized_url = re.search(fb_customized_url_match_string, href_value, flags=re.DOTALL).group(0)
		except AttributeError:
			print "URL is not customized"
	# 3. Get the FB name
	i_matches = user_div.find_all("i")
	for i_match in i_matches:
		if i_match.has_attr('aria-label'):
			fb_name = i_match["aria-label"]
			# 4. Get the pic URL
			style_value = i_match["style"]
			picture_url_match_string = r'(?<=url\(").*?(?="\) no-repeat)'
			picture_url = re.search(picture_url_match_string, style_value, flags=re.DOTALL).group(0)
	user_attributes = {}
	try:
		if fb_name is not None:
			user_attributes['fb_name'] = fb_name
	except NameError:
		pass
	try:
	 	if fb_uid is not None:
			user_attributes['fb_uid'] = fb_uid
	except NameError:
		pass
	try:
		if fb_customized_url is not None:
			user_attributes['fb_customized_url'] = fb_customized_url
	except NameError:
		pass
	try:
		if picture_url is not None:
			user_attributes['picture_url'] = picture_url
	except NameError:
		pass
	return user_attributes

def output_result(output_type, results):
	if output_type == "stdout":
		print json.dumps(results)
	elif output_type == "pretty":
		print json.dumps(results, indent=4, sort_keys=True, ensure_ascii=False, encoding="utf-8")
	elif output_type == "json":
		with open("output.json", 'w+') as output_file:
			json.dump(results, output_file)
	elif output_type == "csv":
		#TODO : write to CSV file
		pass
	else:
		assert False, "unhandled output type : " + output_type
		
if __name__ == '__main__':

	# 0. Get input data (from stdin)
	command, inputData, outputType = get_input_data(sys.argv[1:])
	
	results = []
	# 1A. Extract the attributes (FB id, name, customized URL and profile picture) for every HTML user data
	if command == "user-search":
		for htmlFileName in inputData:
			if os.path.exists(htmlFileName):
				with open(htmlFileName, 'r') as htmlFile:
					try:
						userAttributes = scrap_user_attributes(htmlFile.read())
						results.append(userAttributes)
					except EOFError:
						print "error while reading file '" + htmlFileName + "'"
						pass
	elif command is "profile scraping ":
		#TODO
		print "profile scraping not implemented yet"
	elif command is "page":
		#TODO
		print "profile scraping not implemented yet"

	# 2. Output the results in desired format
	output_result(outputType, results)
	

