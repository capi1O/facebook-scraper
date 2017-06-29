#!/usr/bin/env python

import json
import getopt, sys
import os
import threading
import Queue
import time
import urlparse
import pickle
import robobrowser
from urllib import quote
import re

def parse_arguments(sys_args):
	try:
		opts, non_opts_args = getopt.gnu_getopt(sys_args, "hj:c:o:v:e:p", ["help", "json=", "csv=", "output=", "verbose", "email=", "password="])
		
		# defaults
		input_type = ""
		output_type = "stdin"
		verbose = False
		fb_email = ""
		fb_password = ""
		
		input_file = False
		input_data = ""
		
		for option, arg in opts:
			if option in ("-h", "--help"):
				print "help needed"
			elif option in ("-j", "--json"):
				print "JSON file provided"
				input_file = True
				input_type = "json"
				input_data = arg
			elif option in ("-c", "--csv"):
				print "CSV file provided"
				input_file = True
				input_type = "csv"
				input_data = arg
			elif option in ("-o", "--output"):
				output_type = arg
			elif option in ("-v", "--verbose"):
				verbose = True
			elif option in ("-e", "--email"):
				fb_email = arg
			elif option in ("-p", "--password"):
				fb_password = arg
			else:
				assert False, "unhandled option : " + option
		# if no JSON or CSV options provided, get non-option arguments if provided (names)
		if input_file == False:
			print "no input file provided, reading all non-option arguments as strings : '" + ", ".join(map(str, non_opts_args)) + "'"
			input_type = "strings"
			input_data = non_opts_args
		return [input_type, input_data, output_type, verbose, fb_email, fb_password]
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit(2)

def get_input_names(input_type, input_data = []):
	input_names=[]
	if input_type == "strings":
		input_names = input_data
	elif input_type == "json":
		# json_file_path = os.getcwd() + '/' + input_data
		# print json_file_path
		with open(input_data) as json_data:
			people_json = json.load(json_data)
		for person in people_json:
			input_names.append(person['name'])
	elif input_type == "csv":
		#TODO : loads CSV file
		pass
	else:
		assert False, "unhandled input type : " + input_type
	return input_names

def get_fb_cookies():
	# Check if user token from previous session
	cookies_file = 'cookies.pk'
	if os.path.exists(cookies_file):
		with open(cookies_file, 'rb') as fi:
			try:
				saved_cookies = pickle.load(fi)
				return saved_cookies
			except EOFError:
				print "No saved cookies in file : ", fi
				return None

def fb_log_browser(browser, fb_email, fb_password):
	# Load Facebook website
	url = 'https://m.facebook.com'
	browser.open(url)
	# Send credentials to login form
	login_form = browser.get_form(id='login_form')
	login_form['email'] = fb_email
	login_form['pass'] = fb_password
	browser.submit_form(login_form)
	# TODO : Check if correctly logged in
	if True:
		return True
	else:
		print "Error : could not login"
		return False

def find_matching_users_divs(browser, name):
	encoded_name = quote(name, safe='')
	print encoded_name
	try:
		url = 'https://m.facebook.com/search/people/?q=' + encoded_name + '&tsid&source=filter&isTrending=0'
		browser.open(url)
		results_div = browser.select('div#BrowseResultsContainer')
		user_div_match_string = r'^{"type":"xtracking","xt":"12.{\\"unit_id_click_type\\":\\"graph_search_results_item_in_module_tapped\\"'
		user_divs = browser.find_all(attrs={"data-gt": re.compile(user_div_match_string)})
		return user_divs
	except:
		print "Error while searching for users matching : " + name
		return None

def scrap_user_attributes(user_div):
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

def output_result(output_type, facebook_users):
	if output_type == "stdin":
		print json.dumps(facebook_users, indent=4, sort_keys=True, ensure_ascii=False, encoding="utf-8")
	elif output_type == "json":
		# json_file_path = os.getcwd() + '/' + "output.json"
		# print json_file_path
		with open("output.json", 'w+') as output_file:
			json.dump(facebook_users, output_file)
	elif output_type == "csv":
		#TODO : write to CSV file
		pass
	else:
		assert False, "unhandled output type : " + output_type

if __name__ == '__main__':

	# 0. Parse Arguments
	inputType, inputData, outputType, verbose, fbEmail, fbPassword = parse_arguments(sys.argv[1:])
		
	# 1. Get input names (strings, JSON file or csv file)
	searchedNames = get_input_names(inputType, inputData)
	
	fbBrowser = robobrowser.RoboBrowser(parser="html.parser")
	fbBrowser.session.headers['User-Agent'] = 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'

	# 2A. Try to reuse cookies (if any) from previous session
	fbCookies = get_fb_cookies()
	if fbCookies:
		print "Cookies found, no need to log in"
		fbBrowser.session.cookies = fbCookies
		#TODO : check if valid
		logged_in = True
		if not logged_in:
			# Clear cookies, if any saved
			try:
				os.remove('cookies.pk')
			except OSError:
				pass
	# 2B . Try to login using credentials
	else:
		if fb_log_browser(fbBrowser, fbEmail, fbPassword):
			# Save cookies for future session
			fb_cookies = fbBrowser.session.cookies
			if fb_cookies:
				cookies_file = 'cookies.pk'
				with open(cookies_file, 'wb+') as fi:
					pickle.dump(fb_cookies, fi)
			else:
				print "Error : could not get cookies"
		else:
			print "Access Denied - not logged in, try again"
			sys.exit(2)
	
	# 3 . Find matching Facebook users for each name provided
	searched_results = []
	for searchedName in searchedNames:
		matchingUsersDivs = find_matching_users_divs(fbBrowser, searchedName)
		searched_result = { "searched_user" : searchedName, "matching_users_divs" : matchingUsersDivs}
		searched_results.append(searched_result)
	
	# 4. Extract the attributes (FB id, name, customized URL and profile picture) for every found user
	for searched_result in searched_results:
		matching_users_attributes = []
		for matching_user_div in searched_result["matching_users_divs"]:
			matching_user_attributes = scrap_user_attributes(matching_user_div)
			matching_users_attributes.append(matching_user_attributes)
		searched_result.pop("matching_users_divs", None)
		searched_result["matching_users_attributes"] = matching_users_attributes
	
	# 5 . Output result in desired format
	output_result(outputType, searched_results)





