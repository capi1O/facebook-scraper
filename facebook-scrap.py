#!/usr/bin/env python

import os
import re
import bs4
import json
from commonutils import parse_arguments, output_result
		
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
			# sys.stderr.write("URL is not customized")
			pass
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


		
if __name__ == '__main__':

	# 0A. Parse command line options and arguments
	command, optionsDict, remainingArguments = parse_arguments(["user-search", "profile", "page"], ["v","h"], ["verbose","help"], ["o"], ["output"])
	# 0B. Grab option values or use default if none provided
	verbose = optionsDict.get("verbose", False)
	inputType = optionsDict.get("input", "stdin")
	outputType =  optionsDict.get("output", "stdout")
	# print "output_type : '" + output_type + "'"
	# if output_type not in ["stdout", "json", "csv"]:
	# 	assert False, "unhandled output : " + output_type
	# 0C. Get input data (from stdin)
	inputData = remainingArguments #if inputType = "stdin"

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
						sys.stderr.write("error while reading file '" + htmlFileName + "'")
						pass
	elif command is "profile scraping ":
		#TODO
		print "profile scraping not implemented yet"
	elif command is "page":
		#TODO
		print "profile scraping not implemented yet"

	# 2. Output the results in desired format
	output_result(results, outputType)
	

