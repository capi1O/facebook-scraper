#!/usr/bin/env python

import os
import re
import bs4
import json
from commonutils import *

def scrap_user_attributes(user_div_html):
	verbose_print("parsing " + user_div_html)
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
			verbose_print("URL for Facebook user " + fb_uid + " is not customized")
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

	# 1. Parse command line options and arguments
	acceptableNonArgOptions = [ ["v", "verbose"], ["h", "help"] ]
	inputOptionsDict = {
		"option_name" : ["i", "input"], 
		"acceptable_values" : ["inline","inline-json","json","inline-csv","csv"] 
	}
	formatOptionsDict = {
		"option_name" : ["f", "format"], 
		"acceptable_values" : ["url","raw-html","html-file"] 
	}
	outputOptionsDict = {
		"option_name" : ["o", "output"], 
		"acceptable_values" : ["raw","pretty","json","csv"] 
	}
	acceptableArgOptions = [inputOptionsDict, formatOptionsDict, outputOptionsDict]
	command, optionsDict, remainingArguments = parse_arguments(["user-search", "profile", "page"], acceptableNonArgOptions, acceptableArgOptions)
	
	# 2. Grab option values or use default if none provided
	inputType = optionsDict.get("input", "inline")
	inputFormat = optionsDict.get("format", "html-file")
	outputFormat = optionsDict.get("output", "raw")
	
	# 3. Get input data (from stdin or command line arguments)
	inputData, groupKeys = get_input_data(inputType, inputFormat, remainingArguments, "searched_user", "matching_users_divs_filenames")
	array_dim = get_array_dim(inputData)
	
	# 4. Perform command (for every item in input data)
	# 4A. Scrap Facebook search result (extract Facebook UID, name, customized URL and profile picture)
	if command == "user-search":
		results = []
		# Single dim array
		if array_dim == 1:
			# Check if input array contains only strings
			if not is_string(get_array_type(inputData)):
				assert False, "invalid data of type" + str(get_array_type(inputData)) + " contained in array : " + str(inputData)
			verbose_print("loaded " + str(len(inputData)) + " data blocks")
			results = super_map(inputData, scrap_user_attributes)
		# Doule-dim array - map
		elif array_dim == 2:
			# Check if number of grouped data blocks matches the number of group keys
			if len(inputData) != len(groupKeys) > 0:
				assert False, "mismatch between number of grouped data blocks matches : " + str(len(inputData)) + " and number of group keys : " + str(len(groupKeys))
			# Check if input subarrays contain only strings
			subarray_types = super_map(inputData, get_array_type)
			subarray_check = super_map(subarray_types, is_string)
			if False in subarray_check:
				errorIndex = subarray_check.index(False)
				assert False, "invalid data of type" + subarray_types[errorIndex] + " contained in subarray : " + str(inputData[errorIndex])
			results = super_submap(inputData, scrap_user_attributes)
		else:
			assert False, "unsupported array dimension : " + str(array_dim)
	# 4B. scrap Facebook profile
	elif command is "profile":
		#TODO
		print "profile scraping not implemented yet"
	# 4C. scrap Facebook page
	elif command is "page":
		#TODO
		print "profile scraping not implemented yet"

	# 5. Output the results in desired format
	if array_dim == 1:
		output_results(results, outputFormat)
	elif array_dim == 2:
		output_grouped_results(groupKeys, results, outputFormat)
	else:
		assert False, "unsupported array dimension : " + str(array_dim)